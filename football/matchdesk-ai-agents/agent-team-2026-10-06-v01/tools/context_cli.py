"""Portable auxiliary data validation; no network or model credentials."""
import argparse,csv,json,re,math
from datetime import datetime,date
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def validate_records(records):
    contract=json.loads((ROOT/'context-data-contract.json').read_text(encoding='utf-8'))
    dataset=ROOT.parent/'source-unified-2026-10-06-v01'
    teams=set();matches={}
    for name in ['completed_matches.csv','scheduled_matches.csv']:
        with (dataset/name).open(encoding='utf-8-sig') as f:
            for r in csv.DictReader(f):matches[r['match_key']]=r;teams.update([r['home_team_key'],r['away_team_key']])
    errors=[];ids=set()
    def error(i,msg):errors.append({'record':i,'issue':msg})
    def stamp(value):
        try:return datetime.fromisoformat(value.replace('Z','+00:00')).utcoffset() is not None
        except (ValueError,TypeError,AttributeError):return False
    def day(value):
        try:date.fromisoformat(value);return True
        except (ValueError,TypeError):return False
    for i,r in enumerate(records):
        if not isinstance(r,dict):error(i,'RECORD_NOT_OBJECT');continue
        for k in contract['required']:
            if k not in r:error(i,'MISSING_'+k)
        if not r.get('record_id') or r['record_id'] in ids:error(i,'INVALID_OR_DUPLICATE_ID')
        ids.add(r.get('record_id'))
        kind=r.get('kind');status=r.get('collection_status')
        if kind not in contract['kinds']:error(i,'UNKNOWN_KIND');continue
        if status not in contract['collection_statuses']:error(i,'INVALID_COLLECTION_STATUS')
        if r.get('team_key') not in teams:error(i,'UNKNOWN_TEAM')
        if r.get('fact_status') not in contract['fact_statuses']:error(i,'INVALID_FACT_STATUS')
        if not stamp(r.get('observed_at')):error(i,'OBSERVATION_TIME_REQUIRES_OFFSET')
        if status in ['MISSING','BLOCKED']:
            if not r.get('reason'):error(i,'MISSING_DATA_REQUIRES_REASON')
            if any(r.get(k) is not None for k in contract['kinds'][kind]):error(i,'MISSING_DATA_MUST_NOT_CONTAIN_VALUES')
            continue
        if not re.match(r'^https?://[^\s]+$',r.get('source_url') or ''):error(i,'SOURCE_URL_REQUIRED')
        for k in contract['kinds'][kind]:
            if r.get(k) is None:error(i,'MISSING_VALUE_'+k)
        if 'match_key' in contract['kinds'][kind]:
            m=matches.get(r.get('match_key'))
            if not m:error(i,'UNKNOWN_MATCH')
            elif r.get('team_key') not in [m['home_team_key'],m['away_team_key']]:error(i,'TEAM_MATCH_REFERENCE_MISMATCH')
        for k in ['valuation_date','effective_date']:
            if k in r and r[k] is not None and not day(r[k]):error(i,'INVALID_'+k)
        if kind=='formation':
            if not re.match(r'^\d+(?:-\d+){2,4}$',r.get('formation') or '') or sum(int(x) for x in (r.get('formation') or '0').split('-') if x.isdigit())!=10:error(i,'INVALID_OUTFIELD_FORMATION')
            if r.get('formation_type') not in ['NOMINAL_START','PREDICTED']:error(i,'INVALID_FORMATION_TYPE')
        if kind=='lineup':
            ps=r.get('players');lt=r.get('lineup_type')
            if not isinstance(ps,list):error(i,'PLAYERS_MUST_BE_LIST');continue
            if any(not isinstance(p,dict) or not p.get('name') or not isinstance(p.get('starter'),bool) for p in ps):error(i,'INVALID_PLAYER_ENTRY');continue
            names=[p['name'].strip().casefold() for p in ps]
            if len(names)!=len(set(names)):error(i,'DUPLICATE_PLAYER')
            if lt not in ['CONFIRMED','PREDICTED']:error(i,'INVALID_LINEUP_TYPE')
            if lt=='CONFIRMED' and (sum(p['starter'] for p in ps)!=11 or r.get('fact_status')!='CONFIRMED'):error(i,'CONFIRMED_XI_REQUIRES_ELEVEN_STARTERS')
            if lt=='PREDICTED' and r.get('fact_status')!='PREDICTED':error(i,'PREDICTED_LINEUP_CANNOT_BE_CONFIRMED')
        if kind=='market_value':
            if not isinstance(r.get('amount'),(int,float)) or isinstance(r.get('amount'),bool) or not math.isfinite(r.get('amount',float('nan'))) or r.get('amount',-1)<0:error(i,'INVALID_VALUE_AMOUNT')
            if not re.match(r'^[A-Z]{3}$',r.get('currency') or ''):error(i,'CURRENCY_CODE_REQUIRED')
            if r.get('valuation_scope') not in ['SQUAD','PLAYER'] or r.get('fact_status')!='ESTIMATED':error(i,'MARKET_VALUE_MUST_BE_ESTIMATE')
        if kind=='news' and not stamp(r.get('published_at')):error(i,'PUBLICATION_TIME_REQUIRES_OFFSET')
    return {'records':len(records),'passed':not errors,'errors':errors,'provider_truth_certified':False}
def main():
    p=argparse.ArgumentParser();p.add_argument('command',choices=['validate']);p.add_argument('input');a=p.parse_args()
    records=json.loads(Path(a.input).read_text(encoding='utf-8'));records=records.get('records',[]) if isinstance(records,dict) else records
    result=validate_records(records);print(json.dumps(result,ensure_ascii=True,indent=2));return 0 if result['passed'] else 1
if __name__=='__main__':raise SystemExit(main())
