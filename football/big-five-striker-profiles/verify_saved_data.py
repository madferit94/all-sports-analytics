"""Verify the public CSV snapshot; optionally verify locally preserved raw files."""
import argparse
import csv
import hashlib
import json
import math
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / 'data' / 'processed'


def read(name):
    with (DATA / name).open(encoding='utf-8-sig', newline='') as stream:
        return list(csv.DictReader(stream))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify-raw', action='store_true',
                        help='Also require original raw responses and verify their hashes.')
    args = parser.parse_args()
    fixtures = read('league_matches.csv')
    players = read('all_players_league_season.csv')
    appearances = read('player_match_records.csv')
    events = read('shot_events.csv')
    audit = read('forward_candidate_audit.csv')
    scatter = read('striker_scatter_ready.csv')
    exceptions = read('reconciliation_exceptions.csv')
    fixture_map = {r['match_id']: r for r in fixtures}
    appearance_keys = {(r['player_id'], r['id']) for r in appearances}
    player_keys = {(r['league'], r['id']) for r in players}
    require(len(fixture_map) == len(fixtures) == 1752, 'Fixture coverage or duplicate IDs')
    require(len(appearance_keys) == len(appearances), 'Duplicate appearances')
    require(len(player_keys) == len(players), 'Duplicate league-player keys')
    require(len({r['id'] for r in events}) == len(events), 'Duplicate event IDs')
    for row in appearances:
        require(row['id'] in fixture_map, 'Unmatched appearance fixture')
        require(row['league'] == fixture_map[row['id']]['league'], 'Appearance league mismatch')
        require((row['league'], row['player_id']) in player_keys, 'Unmatched appearance player')
        require(row['season'] == '2025', 'Unexpected appearance season')
    event_counts = Counter()
    own_goals = 0
    for row in events:
        require((row['player_id'], row['match_id']) in appearance_keys, 'Unmatched event appearance')
        require(row['league'] == fixture_map[row['match_id']]['league'], 'Event league mismatch')
        require(row['season'] == '2025', 'Unexpected event season')
        require(all(0 <= float(row[c]) <= 1 for c in ('xG', 'X', 'Y')), 'Invalid event range')
        is_own_goal = row['result'] == 'OwnGoal'
        require((row['counts_as_attempt'] == 'False') == is_own_goal, 'OwnGoal flag mismatch')
        require((row['is_penalty'] == 'True') == (row['situation'] == 'Penalty'), 'Penalty flag mismatch')
        own_goals += is_own_goal
        if not is_own_goal:
            event_counts[(row['league'], row['player_id'])] += 1
    expected_keys = set()
    for row in audit:
        key = (row['league'], row['player_id'])
        require(key in player_keys, 'Unmatched candidate player')
        require(int(row['shots']) == int(row['penalty_attempts']) + int(row['non_penalty_shots']), 'Shot partition mismatch')
        require(event_counts[key] == int(row['shots']), 'Saved event count mismatch')
        if int(row['non_penalty_shots']) and int(row['minutes']):
            require(math.isclose(float(row['npshots_per90']) * float(row['npxg_per_shot']), float(row['npxg_per90']), abs_tol=1e-12), 'Axis identity mismatch')
        if (row['role_classification'] == 'central_forward_candidate'
                and int(row['minutes']) >= 900 and int(row['non_penalty_shots']) > 0
                and row['qc_pass'] == 'True'):
            expected_keys.add(key)
    actual_keys = {(r['league'], r['player_id']) for r in scatter}
    require(len(actual_keys) == len(scatter), 'Duplicate scatter keys')
    require(expected_keys == actual_keys, 'Saved scatter selection mismatch')
    require(len(exceptions) == sum(r['qc_pass'] != 'True' for r in audit), 'Exceptions count mismatch')
    verified_raw_files = 0
    if args.verify_raw:
        manifest = json.loads((ROOT / 'raw_manifest.json').read_text())
        for item in manifest:
            path = ROOT / item['path']
            data = path.read_bytes()
            require(hashlib.sha256(data).hexdigest() == item['sha256'], 'Raw hash mismatch')
            metadata = json.loads(path.with_suffix('.meta.json').read_text())
            require(metadata['sha256_decoded_json'] == item['sha256'], 'Original retrieval hash mismatch')
            verified_raw_files += 1
    checks = ['unique keys', 'foreign-key joins', 'season scope', 'event ranges',
              'penalty and OwnGoal flags', 'shot partition', 'axis identity',
              'saved cohort selection']
    if args.verify_raw:
        checks.append('raw and retrieval-metadata hashes')
    summary = {
        'status': 'pass', 'fixtures': len(fixtures), 'player_league_rows': len(players),
        'appearances': len(appearances), 'shot_events': len(events), 'own_goal_events': own_goals,
        'candidate_league_rows': len(audit), 'scatter_rows': len(scatter),
        'scatter_unique_players': len({r['player_id'] for r in scatter}),
        'reconciliation_exceptions': len(exceptions), 'verified_raw_files': verified_raw_files,
        'raw_check_status': 'pass' if args.verify_raw else 'not_requested',
        'checks': checks,
    }
    report = 'saved_data_verification.json' if args.verify_raw else 'csv_verification.json'
    (ROOT / report).write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
