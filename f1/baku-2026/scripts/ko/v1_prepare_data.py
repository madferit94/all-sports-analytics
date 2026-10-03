"""V1: 원본 보존 → 구조 검증 → 조인 검증 → 분석 기본 표 저장.

실행: python scripts/ko/v1_prepare_data.py
기본 실행은 저장된 자료를 사용하며 --fetch-missing으로 부족한 자료를 받습니다.
최종 비교 랩 선정이나 페이스 결론을 계산하는 단계는 아닙니다.
"""
from pathlib import Path
from datetime import datetime, timezone
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError
import argparse
import hashlib
import json
import time
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / 'data' / 'raw'
PROCESSED = ROOT / 'data' / 'processed'
SESSION = 11377
RAW.mkdir(parents=True, exist_ok=True)
PROCESSED.mkdir(parents=True, exist_ok=True)


def load_or_fetch(endpoint, params, fetch_missing=False):
    """기존 원본을 재사용하고 요청한 경우에만 없는 자료를 다운로드합니다."""
    query = urlencode(params, safe=':')
    name = endpoint + '_' + query.replace('&', '_').replace('=', '-') + '.json'
    path = RAW / name
    url = 'https://api.openf1.org/v1/' + endpoint + '?' + query
    fetched_at = None
    if not path.exists():
        if not fetch_missing:
            raise FileNotFoundError(f'Missing snapshot: {path.name}. Use --fetch-missing to download.')
        req = Request(url, headers={'User-Agent': 'F1LearningAnalysis/1.0'})
        with urlopen(req, timeout=60) as response:
            body = response.read()
        parsed = json.loads(body)
        if not isinstance(parsed, list):
            raise ValueError(f'{endpoint}: response is not a list: {parsed}')
        # API에서 받은 바이트를 그대로 보존합니다.
        path.write_bytes(body)
        fetched_at = datetime.now(timezone.utc).isoformat()
        time.sleep(2.2)  # 무료 요청 한도를 넘지 않도록 순서대로 요청합니다.
    data = json.loads(path.read_bytes())
    assert isinstance(data, list) and len(data), f'{endpoint}: empty response'
    record = dict(endpoint=endpoint, file=str(path.relative_to(ROOT)), url=url,
                  rows=len(data), sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                  retrieved_at_utc=fetched_at,
                  file_modified_utc=datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat(),
                  provenance='downloaded_this_run' if fetched_at else 'existing_snapshot_preserved')
    print(endpoint, len(data), record['provenance'], flush=True)
    return pd.DataFrame(data), record


def save_csv(frame, name):
    """한글 Excel에서도 읽을 수 있도록 UTF-8 BOM으로 CSV를 저장합니다."""
    frame.to_csv(PROCESSED / name, index=False, encoding='utf-8-sig')


def main(fetch_missing=False):
    sources = {}; manifest = []
    endpoints = ['drivers', 'laps', 'stints', 'pit', 'race_control', 'session_result',
                 'sessions', 'position', 'intervals', 'weather', 'starting_grid']
    for endpoint in endpoints:
        try:
            frame, item = load_or_fetch(endpoint, {'session_key': SESSION}, fetch_missing)
        except (HTTPError, FileNotFoundError) as error:
            if endpoint != 'starting_grid':
                raise
            manifest.append({'endpoint':endpoint,'status':'not_available_in_request',
                             'http_status':getattr(error, 'code', None),
                             'note':'optional endpoint unavailable or absent from the saved snapshot; no grid inferred','url':f'https://api.openf1.org/v1/starting_grid?session_key={SESSION}'})
            print('starting_grid not available; no substitute inferred', flush=True)
            continue
        sources[endpoint] = frame
        manifest.append(item)

    # 이동 영상에 필요한 시간 차이·위치 부분 자료도 원본으로 보존합니다.
    replay_requests = [
        ('intervals', {'session_key': SESSION, 'driver_number': 3}),
        ('position', {'session_key': SESSION, 'driver_number': 63}),
        *[('location', {'session_key': SESSION, 'driver_number': number,
                       'date>': '2026-09-26T11:54:12',
                       'date<': '2026-09-26T12:03:16'}) for number in [63, 3]],
    ]
    for endpoint, params in replay_requests:
        _, item = load_or_fetch(endpoint, params, fetch_missing)
        manifest.append(item)

    # 1. 원본 구조 확인: 행 수, 자료형, 결측치, 완전 중복을 남깁니다.
    audits = {}
    for name, df in sources.items():
        audits[name] = {'rows': len(df), 'columns': list(df.columns),
                        'dtypes': df.dtypes.astype(str).to_dict(),
                        'null_counts': df.isna().sum().astype(int).to_dict(),
                        'exact_duplicate_rows': int(df.astype(str).duplicated().sum())}
        # list 등 중첩 필드는 JSON 문자열로 보존하여 한 셀에 들어가게 합니다.
        flat = df.copy()
        for col in flat:
            flat[col] = flat[col].map(lambda v: json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else v)
        save_csv(flat, name + '.csv')

    # 2. 결과와 드라이버 연결: 한 행은 한 드라이버이며 JOIN은 1:1입니다.
    driver = sources['drivers'][['session_key', 'driver_number', 'full_name', 'name_acronym', 'team_name', 'team_colour']]
    results = sources['session_result'].merge(driver, on=['session_key', 'driver_number'], how='left', validate='one_to_one', indicator=True)
    assert results['_merge'].eq('both').all()
    results = results.drop(columns='_merge')
    top10 = results[results.position.between(1, 10)].sort_values('position')
    assert len(top10) == 10 and top10.driver_number.nunique() == 10
    save_csv(top10, 'top10_drivers.csv')

    # 3. 랩 분석 기본 표: (session_key, driver_number, lap_number)가 유일키입니다.
    laps = sources['laps'].copy()
    keys = ['session_key', 'driver_number', 'lap_number']
    assert not laps.duplicated(keys).any(), 'duplicate driver-lap key'
    n_before = len(laps)
    base = laps.merge(driver, on=['session_key', 'driver_number'], how='left', validate='many_to_one', indicator=True)
    unmatched_names = int(base['_merge'].ne('both').sum())
    assert unmatched_names == 0
    base = base.drop(columns='_merge')
    base['lap_start_utc'] = pd.to_datetime(base.date_start, format='ISO8601', utc=True, errors='coerce')
    base['lap_end_est_utc'] = base.lap_start_utc + pd.to_timedelta(base.lap_duration, unit='s')
    base['is_final_top10'] = base.driver_number.isin(top10.driver_number)
    base['is_main_pair'] = base.driver_number.isin([63, 3])

    # 타이어 구간 JOIN: lap_start <= lap_number <= lap_end 범위로 연결합니다.
    # 구간 JOIN은 행이 늘어날 수 있어 일치한 구간 개수도 저장합니다.
    stint_fields = []
    for row in base.itertuples():
        candidates = sources['stints']
        m = candidates[(candidates.driver_number == row.driver_number) &
                       (candidates.lap_start <= row.lap_number) & (candidates.lap_end >= row.lap_number)]
        record = {'stint_match_count': len(m), 'stint_number': None, 'compound': None,
                  'tyre_age_start_lap_est': None}
        if len(m) == 1:
            s = m.iloc[0]
            record.update(stint_number=s.stint_number, compound=s.compound,
                          tyre_age_start_lap_est=s.tyre_age_at_start + row.lap_number - s.lap_start)
        stint_fields.append(record)
    base = pd.concat([base.reset_index(drop=True), pd.DataFrame(stint_fields)], axis=1)
    pit_keys = set(zip(sources['pit'].driver_number, sources['pit'].lap_number))
    base['has_pit_lane_record'] = [(d, n) in pit_keys for d, n in zip(base.driver_number, base.lap_number)]
    base['race_control_review'] = 'PENDING_TIME_INTERVAL_REVIEW'
    # 조건을 정하기 전에 clean lap=참으로 처리하지 않습니다.
    base['pace_eligible'] = pd.NA
    base['eligibility_note'] = 'Finalize after checking temporal overlap with race-control periods'
    assert len(base) == n_before
    base = base.sort_values(['driver_number', 'lap_number'])
    save_csv(base, 'analysis_lap_base.csv')
    save_csv(base[base.is_main_pair], 'russell_verstappen_lap_base.csv')
    save_csv(base[base.is_final_top10], 'top10_lap_base.csv')

    # 4. 경기 중 공지만 따로 저장하되, 경기 전후 원본 공지는 삭제하지 않습니다.
    events = sources['race_control'].copy()
    events['event_time_utc'] = pd.to_datetime(events.date, format='ISO8601', utc=True)
    t_start = events.loc[events.message.eq('SESSION STARTED'), 'event_time_utc'].min()
    t_end = events.loc[events.message.eq('SESSION FINISHED'), 'event_time_utc'].max()
    assert pd.notna(t_start) and pd.notna(t_end) and t_start < t_end
    events['within_race'] = events.event_time_utc.between(t_start, t_end)
    save_csv(events, 'race_control_events.csv')
    race_events = events[events.within_race].copy().sort_values('event_time_utc')
    save_csv(race_events, 'race_control_during_race.csv')
    key = race_events[(race_events.category.isin(['SafetyCar','SessionStatus'])) |
                      race_events.flag.eq('RED') |
                      race_events.message.str.contains('ALL CARS THROUGH THE PIT LANE', na=False)]
    save_csv(key, 'key_race_events.csv')

    # 안전차 복귀 예고는 종료 시각이 아닙니다. 여기서는 경계 후보만 저장합니다.
    rus_laps = base[base.driver_number.eq(63)]
    deployments = race_events[race_events.message.eq('SAFETY CAR DEPLOYED')]
    notices = race_events[race_events.message.eq('SAFETY CAR IN THIS LAP')]
    periods = []
    for row in deployments.itertuples():
        notice = notices[notices.event_time_utc > row.event_time_utc].iloc[0]
        next_lap = rus_laps[rus_laps.lap_number.eq(int(notice.lap_number) + 1)].iloc[0]
        periods.append({'deployment_utc':row.event_time_utc, 'deployment_notice_lap':row.lap_number,
                        'in_this_lap_notice_utc':notice.event_time_utc,
                        'candidate_restart_lap':int(notice.lap_number)+1,
                        'candidate_boundary_utc':next_lap.lap_start_utc,
                        'status':'REQUIRES_RESTART_VERIFICATION',
                        'meaning':'Candidate boundary; not a verified Safety Car withdrawal time'})
    save_csv(pd.DataFrame(periods), 'safety_car_boundary_candidates.csv')

    # 5. 검증 결과: 날짜, ID, 조인, 누락을 사용자에게 보여줍니다.
    counts = base.groupby('driver_number').size()
    report = {'session_key':SESSION, 'meeting_key':1295, 'race_start_utc':str(t_start), 'race_finish_utc':str(t_end),
              'drivers':len(driver), 'raw_laps':n_before, 'joined_laps':len(base),
              'driver_lap_duplicate_keys':int(base.duplicated(keys).sum()),
              'unmatched_driver_names':unmatched_names,
              'stint_unmatched_laps':int(base.stint_match_count.eq(0).sum()),
              'stint_ambiguous_laps':int(base.stint_match_count.gt(1).sum()),
              'missing_lap_duration_all':int(base.lap_duration.isna().sum()),
              'missing_lap_duration_main_pair':int(base[base.is_main_pair].lap_duration.isna().sum()),
              'missing_lap_start_all':int(base.lap_start_utc.isna().sum()),
              'nonpositive_lap_duration':int(base.lap_duration.le(0).sum()),
              'main_pair_laps':int(base.is_main_pair.sum()), 'top10_laps':int(base.is_final_top10.sum()),
              'all_race_control_rows':len(events),'during_race_control_rows':len(race_events),
              'sc_deployments':len(deployments),'red_flags_during_race':int(race_events.flag.eq('RED').sum()),
              'main_pair_numbers':{'Russell':63,'Verstappen':3},
              'lap_count_by_driver':{str(k):int(v) for k,v in counts.items()},
              'pace_eligibility_status':'NOT_YET_FINALIZED',
              'starting_grid_available':'starting_grid' in sources,
              'sources':audits}
    (PROCESSED/'data_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    # 매 실행 기록에 구분된 시각을 남깁니다. 기존 manifest를 덮어쓰지 않습니다.
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    (PROCESSED/f'source_manifest_{stamp}.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k not in ['sources','lap_count_by_driver']},ensure_ascii=False,indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fetch-missing', action='store_true')
    main(fetch_missing=parser.parse_args().fetch_missing)
