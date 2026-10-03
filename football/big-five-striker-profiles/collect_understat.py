"""Collect the 2025/26 Big Five striker research snapshot from Understat.

Standard library only. Run: python3 collect_understat.py
Raw responses are cached; re-running resumes downloads and rebuilds derived CSVs.
This is a collection/validation pipeline, not an assertion of player ability.
"""
from __future__ import annotations

import csv
import gzip
import hashlib
import json
import math
import threading
import time
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "processed"
SEASON = "2025"
LEAGUES = {"EPL": 380, "La_liga": 380, "Bundesliga": 306,
           "Serie_A": 380, "Ligue_1": 306}
MIN_MINUTES = 900
MIN_KNOWN_POSITION_SHARE = 0.5
MIN_CF_SHARE = 0.5
FLOAT_TOLERANCE = 0.0001
LOCK = threading.Lock()
NEXT_REQUEST = 0.0


def now():
    return datetime.now(timezone.utc).isoformat()


def save_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")
    temporary.replace(path)


def fetch_json(endpoint, path, referer):
    """Use the site's read-only JSON endpoint; retain original decoded JSON bytes."""
    global NEXT_REQUEST
    if path.exists():
        return json.loads(path.read_bytes())
    url = "https://understat.com/" + endpoint
    for attempt in range(5):
        with LOCK:
            pause = max(0.0, NEXT_REQUEST - time.monotonic())
            NEXT_REQUEST = max(time.monotonic(), NEXT_REQUEST) + 0.6
        if pause:
            time.sleep(pause)
        request = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0",
            "Referer": referer,
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "application/json",
        })
        try:
            with urllib.request.urlopen(request, timeout=45) as response:
                body = response.read()
                headers = dict(response.headers)
                status = response.status
            if body[:2] == b"\x1f\x8b":
                body = gzip.decompress(body)
            data = json.loads(body)
            if not isinstance(data, dict):
                raise ValueError("Expected a JSON object")
            path.parent.mkdir(parents=True, exist_ok=True)
            temp = path.with_suffix(".tmp")
            temp.write_bytes(body)
            temp.replace(path)
            save_json(path.with_suffix(".meta.json"), {
                "url": url, "referer": referer, "retrieved_at_utc": now(),
                "http_status": status, "response_headers": headers,
                "sha256_decoded_json": hashlib.sha256(body).hexdigest(),
                "bytes_decoded_json": len(body),
            })
            return data
        except urllib.error.HTTPError as error:
            # Do not try to circumvent access denials.
            if error.code in (401, 403, 404):
                raise
            if attempt == 4:
                raise
            delay = max(2 ** (attempt + 1), int(error.headers.get("Retry-After", "0")))
            time.sleep(min(delay, 60))
        except (OSError, ValueError):
            if attempt == 4:
                raise
            time.sleep(2 ** (attempt + 1))


def write_csv(name, rows, fields=None):
    OUT.mkdir(parents=True, exist_ok=True)
    if fields is None:
        fields = list(dict.fromkeys(k for row in rows for k in row))
    with (OUT / name).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="raise")
        writer.writeheader()
        writer.writerows(rows)


def f(value):
    return float(value)


def ratio(numerator, denominator):
    return numerator / denominator if denominator else None


def broad_candidate(player):
    tokens = set(player["position"].split())
    # S-only players have no known starting position: retain them for review.
    return "F" in tokens or tokens == {"S"}


def main():
    started = now()
    league_data = {}
    all_players = []
    fixtures = []
    match_league = {}
    fixture_teams = {}
    candidates = []
    league_qc = []
    for league, expected in LEAGUES.items():
        data = fetch_json(f"getLeagueData/{league}/{SEASON}",
                          RAW / "leagues" / f"{league}_{SEASON}.json",
                          f"https://understat.com/league/{league}/{SEASON}")
        league_data[league] = data
        assert len(data["dates"]) == expected, (league, "unexpected fixture count")
        assert all(match["isResult"] is True for match in data["dates"]), (league, "unfinished")
        assert len({str(p['id']) for p in data['players']}) == len(data['players'])
        for match in data["dates"]:
            mid = str(match["id"])
            assert mid not in match_league, (mid, "duplicate match")
            match_league[mid] = league
            fixture_teams[mid] = {"h": match["h"]["title"], "a": match["a"]["title"]}
            fixtures.append({"league": league, "season": SEASON, "match_id": mid,
                             "date": match["datetime"], "home_team": match["h"]["title"],
                             "away_team": match["a"]["title"],
                             "home_goals": match["goals"]["h"], "away_goals": match["goals"]["a"],
                             "home_xg": match["xG"]["h"], "away_xg": match["xG"]["a"],
                             "source_url": f"https://understat.com/match/{mid}"})
        for p in data["players"]:
            row = {"league": league, "season": SEASON, **p,
                   "detail_in_scope": broad_candidate(p)}
            all_players.append(row)
            if broad_candidate(p):
                candidates.append((league, p))
        league_qc.append({"league": league, "matches": len(data["dates"]),
                          "players": len(data["players"]),
                          "broad_candidate_rows": sum(broad_candidate(p) for p in data["players"]),
                          "date_min": min(m['datetime'] for m in data['dates']),
                          "date_max": max(m['datetime'] for m in data['dates'])})
        print(f"{league}: {len(data['players'])} players; {league_qc[-1]['broad_candidate_rows']} candidate rows", flush=True)
    write_csv("all_players_league_season.csv", all_players)
    write_csv("league_matches.csv", fixtures)
    ids = sorted({str(p["id"]) for _, p in candidates}, key=int)
    save_json(ROOT / "collection_status.json", {"started": started, "phase": "player_details", "target_players": len(ids)})
    print(f"DETAIL DOWNLOAD: {len(ids)} unique players, two workers, 0.6s request spacing", flush=True)
    details = {}
    failures = []

    def collect_player(pid):
        return pid, fetch_json(f"getPlayerData/{pid}", RAW / "players" / f"{pid}.json",
                               f"https://understat.com/player/{pid}")

    with ThreadPoolExecutor(max_workers=2) as pool:
        tasks = {pool.submit(collect_player, pid): pid for pid in ids}
        for index, future in enumerate(as_completed(tasks), 1):
            pid = tasks[future]
            try:
                _, details[pid] = future.result()
            except Exception as error:
                failures.append({"player_id": pid, "error": repr(error)})
            if index % 25 == 0 or index == len(ids):
                print(f"Downloaded {index}/{len(ids)}; failures={len(failures)}", flush=True)
                save_json(ROOT / "collection_status.json", {"started": started, "updated": now(),
                          "phase": "player_details", "target_players": len(ids),
                          "processed_players": index, "failures": failures})
    save_json(ROOT / "download_failures.json", failures)
    if failures:
        raise RuntimeError(f"{len(failures)} downloads failed; rerun to resume cached collection")

    player_matches, shots, positions, audit = [], [], [], []
    match_by_key, shots_by_key = defaultdict(list), defaultdict(list)
    seen_matches, seen_shots = set(), set()
    source_duplicate_matches = []
    duplicate_counts = Counter()
    for pid, data in sorted(details.items(), key=lambda item: int(item[0])):
        assert str(data["player"]["id"]) == pid
        canonical_matches = {}
        for match in sorted(data['matches'], key=lambda m: int(m['roster_id'])):
            mid = str(match["id"])
            if mid not in match_league:
                continue
            if mid in canonical_matches:
                first = canonical_matches[mid]
                assert {k: v for k, v in first.items() if k != 'roster_id'} == {k: v for k, v in match.items() if k != 'roster_id'}, (pid, mid, 'conflicting duplicate')
                source_duplicate_matches.append({
                    'league': match_league[mid], 'player_id': pid,
                    'player_name': data['player']['name'], 'match_id': mid,
                    'retained_roster_id': first['roster_id'], 'duplicate_roster_id': match['roster_id'],
                    'identical_except_roster_id': True, 'duplicate_minutes': match['time'],
                })
                duplicate_counts[(match_league[mid], pid)] += 1
                continue
            canonical_matches[mid] = match
        for mid, match in canonical_matches.items():
            assert str(match["season"]) == SEASON
            key = (pid, mid)
            assert key not in seen_matches, (key, "duplicate player match")
            seen_matches.add(key)
            league = match_league[mid]
            row = {"league": league, "player_id": pid, "player_name": data['player']['name'], **match}
            player_matches.append(row)
            match_by_key[(league, pid)].append(match)
        for shot in data["shots"]:
            mid = str(shot["match_id"])
            if mid not in match_league:
                continue
            assert str(shot["season"]) == SEASON
            assert str(shot["player_id"]) == pid
            sid = str(shot["id"])
            assert sid not in seen_shots, (sid, "duplicate shot")
            seen_shots.add(sid)
            assert (pid, mid) in seen_matches, (pid, mid, "shot missing player match")
            assert 0 <= f(shot["xG"]) <= 1
            assert 0 <= f(shot["X"]) <= 1 and 0 <= f(shot["Y"]) <= 1
            league = match_league[mid]
            row = {"league": league, **shot, "is_penalty": shot["situation"] == "Penalty",
                   "counts_as_attempt": shot['result'] != 'OwnGoal',
                   "team": fixture_teams[mid][shot["h_a"]]}
            shots.append(row)
            shots_by_key[(league, pid)].append(shot)

    for league, p in candidates:
        pid = str(p["id"])
        matches = match_by_key[(league, pid)]
        all_shot_events = shots_by_key[(league, pid)]
        # Understat includes zero-xG OwnGoal entries in the event list, but
        # excludes these entries from a player's attacking shot totals.
        player_shots = [s for s in all_shot_events if s['result'] != 'OwnGoal']
        penalties = [s for s in player_shots if s["situation"] == "Penalty"]
        non_penalties = [s for s in player_shots if s["situation"] != "Penalty"]
        pos_minutes = Counter()
        pos_games = Counter()
        for m in matches:
            pos_minutes[m['position']] += int(m['time'])
            pos_games[m['position']] += 1
        for position, minutes in sorted(pos_minutes.items()):
            positions.append({"league": league, "player_id": pid, "player_name": p['player_name'],
                              "season": SEASON, "position": position, "assigned_minutes": minutes,
                              "appearances": pos_games[position]})
        minutes = int(p["time"])
        known = sum(v for k, v in pos_minutes.items() if k != "Sub")
        cf = pos_minutes.get("FW", 0)
        known_share = ratio(known, minutes)
        cf_share = ratio(cf, known)
        primary = max((k for k in pos_minutes if k != 'Sub'), key=lambda k: pos_minutes[k], default="Unknown")
        if known_share is None or known_share < MIN_KNOWN_POSITION_SHARE:
            classification = "insufficient_known_position"
        elif cf_share is not None and cf_share >= MIN_CF_SHARE:
            classification = "central_forward_candidate"
        else:
            classification = "other_forward_or_mixed_role"
        checks = {
            "no_source_duplicate_appearances": duplicate_counts[(league, pid)] == 0,
            "appearances_match": len(matches) == int(p['games']),
            "minutes_match": sum(int(m['time']) for m in matches) == minutes,
            "shots_match": len(player_shots) == int(p['shots']) == sum(int(m['shots']) for m in matches),
            "xg_match": math.isclose(sum(f(s['xG']) for s in player_shots), f(p['xG']), abs_tol=FLOAT_TOLERANCE),
            "npxg_match": math.isclose(sum(f(s['xG']) for s in non_penalties), f(p['npxG']), abs_tol=FLOAT_TOLERANCE),
            "goals_match": sum(s['result'] == 'Goal' for s in player_shots) == int(p['goals']),
            "npg_match": sum(s['result'] == 'Goal' for s in non_penalties) == int(p['npg']),
            "position_minutes_match": sum(pos_minutes.values()) == minutes,
        }
        audit.append({"league": league, "season": SEASON, "player_id": pid,
                      "player_name": p['player_name'], "team": p['team_title'],
                      "source_position_group": p['position'], "minutes": minutes,
                      "appearances": int(p['games']), "goals": int(p['goals']), "non_penalty_goals": int(p['npg']),
                      "source_duplicate_appearance_rows": duplicate_counts[(league, pid)],
                      "unique_appearance_count": len(matches),
                      "unique_appearance_minutes": sum(int(m['time']) for m in matches),
                      "shots": int(p['shots']),
                      "own_goal_event_count": len(all_shot_events) - len(player_shots),
                      "penalty_attempts": len(penalties),
                      "non_penalty_shots": len(non_penalties), "xg": f(p['xG']), "npxg": f(p['npxG']),
                      "shot_sum_xg": sum(f(s['xG']) for s in player_shots),
                      "shot_sum_npxg": sum(f(s['xG']) for s in non_penalties),
                      "npshots_per90": ratio(len(non_penalties) * 90, minutes),
                      "npxg_per_shot": ratio(sum(f(s['xG']) for s in non_penalties), len(non_penalties)),
                      "npxg_per90": ratio(sum(f(s['xG']) for s in non_penalties) * 90, minutes),
                      "primary_known_position": primary, "cf_assigned_minutes": cf,
                      "known_position_minutes": known, "sub_position_minutes": pos_minutes.get('Sub', 0),
                      "known_position_share": known_share, "cf_share_known_position": cf_share,
                      "role_classification": classification,
                      "eligible_900_minutes": minutes >= MIN_MINUTES,
                      **checks, "qc_pass": all(checks.values()),
                      "source_url": f"https://understat.com/player/{pid}"})
    audit.sort(key=lambda row: (row['league'], -row['minutes'], row['player_id']))
    write_csv("forward_candidate_audit.csv", audit)
    write_csv("player_match_records.csv", player_matches)
    write_csv("shot_events.csv", shots)
    write_csv("position_summary.csv", positions)
    write_csv("source_duplicate_appearances.csv", source_duplicate_matches,
              ['league', 'player_id', 'player_name', 'match_id', 'retained_roster_id',
               'duplicate_roster_id', 'identical_except_roster_id', 'duplicate_minutes'])
    errors = [row for row in audit if not row['qc_pass']]
    write_csv("reconciliation_exceptions.csv", errors, list(audit[0]))
    eligible = [row for row in audit if row['role_classification'] == 'central_forward_candidate'
                and row['eligible_900_minutes'] and row['non_penalty_shots'] > 0 and row['qc_pass']]
    write_csv("striker_scatter_ready.csv", eligible, list(audit[0]))
    sensitivity = []
    for threshold in (450, 600, 900, 1200, 1500):
        for league in LEAGUES:
            selected = [r for r in audit if r['league'] == league and r['minutes'] >= threshold
                        and r['role_classification'] == 'central_forward_candidate'
                        and r['non_penalty_shots'] > 0 and r['qc_pass']]
            sensitivity.append({"league": league, "minimum_minutes": threshold, "eligible_rows": len(selected)})
    write_csv("minutes_threshold_counts.csv", sensitivity)
    for item in league_qc:
        league = item['league']
        item['detail_rows'] = sum(r['league'] == league for r in audit)
        item['shot_events'] = sum(r['league'] == league for r in shots)
        item['scatter_ready_rows'] = sum(r['league'] == league for r in eligible)
        item['reconciliation_failures'] = sum(r['league'] == league for r in errors)
    write_csv("league_coverage.csv", league_qc)
    manifest = []
    for path in sorted(RAW.rglob('*.json')):
        if path.name.endswith('.meta.json'):
            continue
        body = path.read_bytes()
        manifest.append({"path": str(path.relative_to(ROOT)), "bytes": len(body),
                         "sha256": hashlib.sha256(body).hexdigest()})
    save_json(ROOT / "raw_manifest.json", manifest)
    validation = {
        "started_utc": started, "finished_utc": now(), "season": "2025/26",
        "source": "Understat", "match_count": len(fixtures),
        "all_player_league_rows": len(all_players), "detailed_unique_players": len(details),
        "forward_candidate_league_rows": len(audit), "player_match_rows": len(player_matches),
        "shot_rows": len(shots), "own_goal_event_rows": sum(not s['counts_as_attempt'] for s in shots),
        "reconciliation_failed_rows": len(errors),
        "source_duplicate_appearance_rows": len(source_duplicate_matches),
        "scatter_ready_rows": len(eligible), "scatter_unique_players": len({r['player_id'] for r in eligible}),
        "download_failures": failures, "league_coverage": league_qc,
        "classification_counts": dict(Counter(r['role_classification'] for r in audit)),
        "shot_situations": dict(Counter(r['situation'] for r in shots)),
        "position_codes": dict(Counter(m['position'] for m in player_matches)),
        "float_tolerance": FLOAT_TOLERANCE,
        "row_unit": "player x league x season; transfers within one league aggregated; transfers across leagues separate",
        "detail_scope": "All league-summary players flagged F, plus S-only players, without a minutes cutoff. Other players retain summaries only.",
        "role_rule": "FW >= 50% of non-Sub assigned minutes; non-Sub assigned minutes >= 50% of total. Candidate label, not confirmed tactical role.",
        "important_limits": [
            "Understat positions describe recorded match positions, not verified time-resolved tactical roles.",
            "Sub minutes have unknown tactical position and are never imputed as FW.",
            "Player shots and per90 metrics include all appearances within the league season, not only FW-coded matches.",
            "Internal reconciliation does not independently verify Understat's source accuracy or xG calibration.",
            "Raw player responses include historical seasons; derived tables use only matches in the five 2025/26 league match lists.",
        ],
    }
    save_json(ROOT / "validation.json", validation)
    save_json(ROOT / "collection_status.json", {"phase": "complete", "finished": now(),
              "qc": "pass" if not errors else "exceptions_excluded", "scatter_ready_rows": len(eligible)})
    print(json.dumps(validation, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
