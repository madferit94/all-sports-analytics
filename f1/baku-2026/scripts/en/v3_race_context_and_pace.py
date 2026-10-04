"""V3: follow race context, select candidate lap pairs, and compare pace.

Read saved OpenF1 snapshots only. All SC ends are candidate boundaries.
This tutorial does not finalize race-control review or causal conclusions.
"""
from pathlib import Path
import hashlib
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager

ROOT = Path(__file__).resolve().parents[2]
LANGUAGE = 'en'
LABELS = {'gap_title': 'Russell–Verstappen published timing gap', 'gap_subtitle': 'Baku 2026 | official timing samples; shaded SC ends are candidate boundaries', 'gap_note': 'Source: OpenF1 session 11377. Missing gaps remain unfilled. Top markers show pit-lane event time only.\nMarker height is not a timing gap; lane activity does not confirm a tyre change.', 'pit_63': 'RUS pit-lane record', 'pit_3': 'VER pit-lane record', 'elapsed_minutes': 'Minutes since first leader lap started', 'gap_seconds': 'VER gap to RUS (seconds)', 'pace_title': 'Candidate paired lap-time differences', 'pace_subtitle': 'Same-lap VER minus RUS | positive = Russell faster | provisional temporal exclusions', 'pace_note': 'SC, pit, candidate restart and yellow-overlap laps excluded for both drivers.\nNo fuel/traffic correction. Final restart and flag-conflict review remains pending.', 'BEFORE_FIRST_SC': 'Before first SC', 'AFTER_SECOND_RESTART': 'After second candidate restart', 'median': 'median', 'insufficient': 'Too few pairs to summarize', 'lap_number': 'Race lap', 'paired_difference': 'VER minus RUS lap time (seconds)', 'tyre_title': 'Main-pair tyre-stint context', 'tyre_subtitle': 'Stint bounds and tyre age at each stint start; age is measured in laps', 'tyre_note': 'Source: OpenF1 stints. A new stint does not automatically mean fresh tyres.\nTyre context alone cannot identify an independent tyre or degradation effect.', 'MEDIUM': 'Medium', 'SOFT': 'Soft', 'age': 'start age', 'pending': 'PROVISIONAL: verify restart boundaries and race-control review items before final pace claims.', 'learning_notes': 'Read in order: 1. Timing gap and race events. 2. Candidate paired pace. 3. Tyre context.\nA positive VER-minus-RUS difference means Russell was quicker in that lap.\nThe median is the middle paired difference; IQR describes the middle 50% spread.\nCandidate exclusions are auditable, but SC boundaries and conflicting flags remain provisional.\nYellow intervals conservatively cover any sector; overlap does not prove either car was directly affected.\nSensitivity checks vary yellow filtering and interval bounds; they are not proof all boundary choices are correct.\nNo causal tyre effect, fuel-corrected pace, or counterfactual winner is estimated.'}
SESSION = 11377
PAIR = [63, 3]
MINIMUM_PAIRS = 5
TIMING_TOLERANCE_SECONDS = 1.0
GAP_TOLERANCE_SECONDS = 8.0
BLUE, GOLD, PINK = '#3569A8', '#B18B32', '#BB6588'


def load_and_validate(root):
    """Read originals and verify keys, joins, timing, and driver identity."""
    sources, manifest = {}, []
    for endpoint in ['laps', 'drivers', 'stints', 'pit', 'race_control',
                     'session_result', 'intervals', 'position', 'sessions']:
        path = root / 'data/raw' / f'{endpoint}_session_key-{SESSION}.json'
        body = path.read_bytes()
        records = json.loads(body)
        assert isinstance(records, list) and records, f'Empty source: {endpoint}'
        frame = pd.DataFrame(records)
        assert frame.session_key.eq(SESSION).all(), f'Wrong session: {endpoint}'
        sources[endpoint] = frame
        manifest.append({'file':str(path.relative_to(root)), 'rows':len(frame),
                         'sha256':hashlib.sha256(body).hexdigest(),
                         'url':f'https://api.openf1.org/v1/{endpoint}?session_key={SESSION}'})
    laps, drivers = sources['laps'], sources['drivers']
    assert not laps.duplicated(['session_key', 'driver_number', 'lap_number']).any()
    assert not drivers.duplicated(['session_key', 'driver_number']).any()
    results = sources['session_result'].merge(
        drivers[['session_key', 'driver_number', 'full_name', 'name_acronym', 'team_name']],
        on=['session_key','driver_number'], validate='one_to_one', how='left', indicator=True)
    assert results['_merge'].eq('both').all()
    top10 = results[results.position.between(1,10)].sort_values('position').drop(columns='_merge')
    assert len(top10) == 10
    positions = sources['position'].query('driver_number == 63')
    assert len(positions) and positions.position.eq(1).all(), 'Gap is not always to Russell'
    pair = laps[laps.driver_number.isin(PAIR)].copy()
    assert len(pair) == 102 and pair.groupby('driver_number').size().eq(51).all()
    assert pair.lap_duration.notna().all() and pair.lap_duration.gt(0).all()
    assert pair.is_pit_out_lap.notna().all(), 'Missing pit-out status needs review'
    pair = pair.sort_values(['driver_number', 'lap_number']).reset_index(drop=True)
    pair['start_utc'] = pd.to_datetime(pair.date_start, format='ISO8601', utc=True)
    pair['end_est_utc'] = pair.start_utc + pd.to_timedelta(pair.lap_duration, unit='s')
    # Compare the estimated end with the next observed start before interval filtering.
    next_start = pair.groupby('driver_number').start_utc.shift(-1)
    pair['end_to_next_start_seconds'] = (next_start-pair.end_est_utc).dt.total_seconds()
    pair['timing_consistent'] = pair.end_to_next_start_seconds.abs().le(TIMING_TOLERANCE_SECONDS) | next_start.isna()
    pit_keys = set(zip(sources['pit'].driver_number, sources['pit'].lap_number))
    pair['has_pit_record'] = [(d,n) in pit_keys for d,n in zip(pair.driver_number,pair.lap_number)]
    # A tyre stint is a lap range; check that exactly one range matches each lap.
    tyre_rows = []
    for lap in pair.itertuples():
        stints = sources['stints']
        matches = stints[(stints.driver_number.eq(lap.driver_number)) &
                         (stints.lap_start.le(lap.lap_number)) & (stints.lap_end.ge(lap.lap_number))]
        item = {'stint_matches':len(matches), 'compound':None, 'tyre_age_start_lap_est':np.nan}
        if len(matches) == 1:
            stint = matches.iloc[0]
            item.update(compound=stint.compound,
                        tyre_age_start_lap_est=stint.tyre_age_at_start+lap.lap_number-stint.lap_start)
        tyre_rows.append(item)
    pair = pd.concat([pair, pd.DataFrame(tyre_rows)], axis=1)
    events = sources['race_control'].copy()
    events['time_utc'] = pd.to_datetime(events.date, format='ISO8601', utc=True)
    race_start = events.loc[events.message.eq('SESSION STARTED'), 'time_utc'].min()
    race_finish = events.loc[events.message.eq('SESSION FINISHED'), 'time_utc'].max()
    assert pd.notna(race_start) and pd.notna(race_finish) and race_start < race_finish
    events = events[events.time_utc.between(race_start, race_finish)].sort_values('time_utc').copy()
    # This case study implements SC periods only; never silently ignore a VSC or RED.
    unsupported = events.flag.eq('RED') | events.message.str.contains('VIRTUAL SAFETY CAR', na=False)
    if unsupported.any():
        raise ValueError('VSC/RED found: implement and review those periods before comparing pace')
    gaps = sources['intervals'].query('driver_number == 3').copy()
    gaps['time_utc'] = pd.to_datetime(gaps.date, format='ISO8601', utc=True)
    gaps['gap_seconds'] = pd.to_numeric(gaps.gap_to_leader, errors='coerce')
    gaps = gaps.sort_values('time_utc')
    assert not gaps.time_utc.duplicated().any()
    report = {'session_key':SESSION, 'raw_laps':len(laps), 'pair_laps':len(pair),
              'drivers':len(drivers), 'top10_drivers':len(top10),
              'duplicate_pair_keys':int(pair.duplicated(['driver_number','lap_number']).sum()),
              'missing_pair_duration':int(pair.lap_duration.isna().sum()),
              'timing_inconsistent_pair_laps':int((~pair.timing_consistent).sum()),
              'max_end_to_next_start_error_seconds':float(pair.end_to_next_start_seconds.abs().max()),
              'missing_numeric_gap_samples':int(gaps.gap_seconds.isna().sum()),
              'race_start_utc':race_start.isoformat(), 'race_finish_utc':race_finish.isoformat(),
              'sources':manifest}
    return sources, pair, events, gaps, top10, report


def build_candidate_periods(pair, events):
    """Build provisional SC bounds and conservative yellow-flag intervals."""
    deployments = events[events.message.eq('SAFETY CAR DEPLOYED')]
    notices = events[events.message.eq('SAFETY CAR IN THIS LAP')]
    assert len(deployments) == 2, 'Review this race if its SC pattern changes'
    periods, reviews = [], []
    starts = deployments.time_utc.tolist()
    race_finish = events.loc[events.message.eq('SESSION FINISHED'), 'time_utc'].max()
    for number, row in enumerate(deployments.itertuples(), 1):
        next_deployment = starts[number] if number < len(starts) else race_finish
        candidate_notices = notices[(notices.time_utc > row.time_utc) & (notices.time_utc < next_deployment)]
        assert len(candidate_notices) == 1
        notice = candidate_notices.iloc[0]
        restart_lap = int(notice.lap_number)+1
        boundary = pair[(pair.driver_number.eq(63)) & (pair.lap_number.eq(restart_lap))].start_utc.iloc[0]
        assert row.time_utc < notice.time_utc < boundary
        periods.append({'kind':'SC', 'id':f'SC{number}', 'start_utc':row.time_utc,
                        'end_utc':boundary, 'restart_lap':restart_lap,
                        'status':'CANDIDATE_RESTART_BOUNDARY', 'sector':np.nan})
    sector_events = events[(events.scope.eq('Sector')) &
                           (events.flag.isin(['YELLOW','DOUBLE YELLOW','CLEAR']))]
    # Process equal-time flags as a group; source row order cannot resolve conflicts.
    for sector, sector_rows in sector_events.groupby('sector'):
        active_start, ambiguous = None, False
        for time_utc, group in sector_rows.groupby('time_utc', sort=True):
            flags = set(group.flag)
            yellow = bool(flags & {'YELLOW','DOUBLE YELLOW'})
            clear = 'CLEAR' in flags
            if yellow and clear:
                reviews.append({'time_utc':time_utc,'sector':sector,'issue':'SIMULTANEOUS_YELLOW_CLEAR'})
                # Conservative candidate: keep yellow active until a later clear-only group.
                active_start = time_utc if active_start is None else active_start
                ambiguous = True
            elif yellow:
                active_start = time_utc if active_start is None else active_start
            elif clear and active_start is not None:
                periods.append({'kind':'YELLOW','id':f'SECTOR_{int(sector)}',
                                'start_utc':active_start,'end_utc':time_utc,'restart_lap':np.nan,
                                'status':'AMBIGUOUS_START' if ambiguous else 'NOTICE_INTERVAL', 'sector':sector})
                active_start, ambiguous = None, False
            elif clear:
                reviews.append({'time_utc':time_utc,'sector':sector,'issue':'CLEAR_WITHOUT_ACTIVE_YELLOW'})
        if active_start is not None:
            periods.append({'kind':'YELLOW','id':f'SECTOR_{int(sector)}',
                            'start_utc':active_start,'end_utc':race_finish,'restart_lap':np.nan,
                            'status':'NO_CLEAR_BEFORE_SESSION_END','sector':sector})
            reviews.append({'time_utc':active_start,'sector':sector,'issue':'NO_CLEAR_BEFORE_SESSION_END'})
    periods = pd.DataFrame(periods).sort_values(['start_utc','kind']).reset_index(drop=True)
    assert (periods.end_utc > periods.start_utc).all()
    return periods, pd.DataFrame(reviews, columns=['time_utc','sector','issue'])


def select_candidate_pairs(pair, periods, exclude_yellow=True, boundary_margin_seconds=0):
    """Apply rules to both drivers and keep a pair only if both laps qualify."""
    tagged = pair.copy()
    sc = periods[periods.kind.eq('SC')]
    padding = pd.Timedelta(seconds=boundary_margin_seconds)
    first_sc = sc.start_utc.min()-padding
    last_restart = sc.end_utc.max()+padding
    restart_laps = set(sc.restart_lap.astype(int))
    reason_rows, phases = [], []
    for lap in tagged.itertuples():
        reasons = []
        if lap.lap_number == 1: reasons.append('LAP_1')
        if lap.has_pit_record: reasons.append('PIT_LANE_RECORD')
        if bool(lap.is_pit_out_lap): reasons.append('PIT_OUT_LAP')
        if lap.lap_number in restart_laps: reasons.append('CANDIDATE_RESTART_LAP')
        if not lap.timing_consistent: reasons.append('TIMING_END_START_MISMATCH')
        if lap.stint_matches != 1: reasons.append('STINT_CONTEXT_UNRESOLVED')
        for interval in periods.itertuples():
            if interval.kind == 'YELLOW' and not exclude_yellow: continue
            start, end = interval.start_utc-padding, interval.end_utc+padding
            # Half-open intervals: touching a boundary alone does not count as overlap.
            if start < end and lap.start_utc < end and lap.end_est_utc > start:
                reasons.append('SC_TIME_OVERLAP' if interval.kind == 'SC' else 'YELLOW_TIME_OVERLAP')
        phase = ('BEFORE_FIRST_SC' if lap.end_est_utc <= first_sc else
                 'AFTER_SECOND_RESTART' if lap.start_utc >= last_restart else 'BETWEEN_OR_DURING_SC')
        phases.append(phase)
        reason_rows.append('|'.join(sorted(set(reasons))))
    tagged['phase'] = phases
    tagged['exclusion_reasons'] = reason_rows
    tagged['candidate_eligible'] = tagged.exclusion_reasons.eq('')
    fields = ['lap_number','lap_duration','candidate_eligible','exclusion_reasons','phase',
              'compound','tyre_age_start_lap_est','start_utc','end_est_utc']
    rus = tagged[tagged.driver_number.eq(63)][fields]
    ver = tagged[tagged.driver_number.eq(3)][fields]
    paired = rus.merge(ver, on='lap_number', suffixes=('_RUS','_VER'), validate='one_to_one', how='outer', indicator=True)
    assert len(paired) == 51 and paired['_merge'].eq('both').all()
    paired = paired.drop(columns='_merge')
    paired['delta_VER_minus_RUS_seconds'] = paired.lap_duration_VER-paired.lap_duration_RUS
    paired['phase'] = np.where(paired.phase_RUS.eq(paired.phase_VER),paired.phase_RUS,'PHASE_MISMATCH')
    paired['candidate_pair_eligible'] = paired.candidate_eligible_RUS & paired.candidate_eligible_VER & paired.phase.ne('PHASE_MISMATCH')
    paired['analysis_status'] = 'PROVISIONAL_RACE_CONTROL_REVIEW_PENDING'
    return tagged, paired


def summarize_pace(paired):
    """Summarize paired differences, never a difference of separate medians."""
    rows = []
    for phase in ['BEFORE_FIRST_SC','AFTER_SECOND_RESTART']:
        sample = paired[paired.candidate_pair_eligible & paired.phase.eq(phase)]
        delta = sample.delta_VER_minus_RUS_seconds
        enough = len(delta) >= MINIMUM_PAIRS
        rows.append({'phase':phase,'n_pairs':len(sample),'lap_numbers':','.join(sample.lap_number.astype(str)),
                     'median_delta_seconds':float(delta.median()) if enough else np.nan,
                     'q25_delta_seconds':float(delta.quantile(.25)) if enough else np.nan,
                     'q75_delta_seconds':float(delta.quantile(.75)) if enough else np.nan,
                     'iqr_delta_seconds':float(delta.quantile(.75)-delta.quantile(.25)) if enough else np.nan,
                     'summary_available':enough,'analysis_status':'PROVISIONAL_RACE_CONTROL_REVIEW_PENDING'})
    return pd.DataFrame(rows)


def sensitivity_check(pair, periods):
    """Change yellow handling and expand/shrink time bounds by one second."""
    rows = []
    for exclude_yellow in [True,False]:
        for margin in [-1,0,1]:
            _, paired = select_candidate_pairs(pair,periods,exclude_yellow,margin)
            summary = summarize_pace(paired)
            summary['exclude_yellow'] = exclude_yellow
            summary['boundary_margin_seconds'] = margin
            rows.append(summary)
    return pd.concat(rows,ignore_index=True)


def plot_results(root, sources, pair, gaps, periods, paired, summary):
    """Export three explanatory figures with visible provisional-status notes."""
    out = root/'outputs'/LANGUAGE/'v3'
    out.mkdir(parents=True,exist_ok=True)
    available = {item.name for item in font_manager.fontManager.ttflist}
    korean_fonts = ['Apple SD Gothic Neo','AppleGothic','Malgun Gothic','NanumGothic','Noto Sans CJK KR','Noto Sans CJK JP']
    family = 'DejaVu Sans' if LANGUAGE == 'en' else next((f for f in korean_fonts if f in available),None)
    if family is None: raise RuntimeError('Install a Korean font; see README.ko.md')
    plt.rcParams.update({'font.family':family,'font.size':11,'axes.unicode_minus':False})
    def format_axes(ax):
        ax.spines[['top','right']].set_visible(False)
        ax.grid(axis='y',color='#DADDE1',linewidth=.6)
        ax.set_axisbelow(True)
    def finish(fig, title, note, filename):
        fig.suptitle(title,fontsize=19,x=.08,ha='left',y=.97)
        fig.text(.08,.03,note,fontsize=9,color='#555555')
        fig.savefig(out/filename,dpi=160,bbox_inches='tight',facecolor='white')
        plt.close(fig)
    race_start = pair.start_utc.min()
    plot_gaps = gaps[gaps.time_utc.between(race_start,pair.end_est_utc.max())]
    fig,ax = plt.subplots(figsize=(12,6));fig.subplots_adjust(top=.79,bottom=.20,left=.08,right=.97)
    ax.plot((plot_gaps.time_utc-race_start).dt.total_seconds()/60,plot_gaps.gap_seconds,color=BLUE,lw=1.6)
    for number,period in enumerate(periods[periods.kind.eq('SC')].itertuples(),1):
        start=(period.start_utc-race_start).total_seconds()/60
        end=(period.end_utc-race_start).total_seconds()/60
        ax.axvspan(start,end,color=GOLD,alpha=.18,hatch='//')
        ax.text((start+end)/2,ax.get_ylim()[1]*.91,f'SC{number}',ha='center')
    for driver,marker,height in [(63,'v',1.02),(3,'o',1.08)]:
        pits = sources['pit'][sources['pit'].driver_number.eq(driver)]
        times = pd.to_datetime(pits.date,format='ISO8601',utc=True)
        # Separate marker rows encode event time only; stale gaps are not substituted.
        ax.scatter((times-race_start).dt.total_seconds()/60,np.full(len(times),height),
                   transform=ax.get_xaxis_transform(),clip_on=False,
                   marker=marker,facecolors='white',edgecolors='#333333',s=85,zorder=4,
                   linewidths=1.2,label=LABELS[f'pit_{driver}'])
    ax.set(xlabel=LABELS['elapsed_minutes'],ylabel=LABELS['gap_seconds'],ylim=(0,max(1,float(plot_gaps.gap_seconds.max())*1.12)))
    ax.legend(loc='upper left',frameon=False);format_axes(ax)
    fig.text(.08,.87,LABELS['gap_subtitle'],fontsize=11)
    finish(fig,LABELS['gap_title'],LABELS['gap_note'],'01_race_context.png')
    fig,axes=plt.subplots(1,2,figsize=(12,6),sharey=True);fig.subplots_adjust(top=.76,bottom=.24,left=.08,right=.97,wspace=.12)
    retained=paired[paired.candidate_pair_eligible & paired.phase.isin(summary.phase)]
    if len(retained):
        values=retained.delta_VER_minus_RUS_seconds
        padding=max(.05,float(values.max()-values.min())*.13)
        limits=(min(0,float(values.min()))-padding,max(0,float(values.max()))+padding)
    else:limits=(-1,1)
    for ax,row in zip(axes,summary.itertuples()):
        sample=paired[paired.candidate_pair_eligible & paired.phase.eq(row.phase)]
        ax.axhline(0,color='#555555',lw=1)
        if row.summary_available:
            ax.scatter(sample.lap_number,sample.delta_VER_minus_RUS_seconds,color=BLUE,s=35)
            ax.axhline(row.median_delta_seconds,color=BLUE,ls='--',lw=1.3)
            ax.set_title(f"{LABELS[row.phase]}\nn={row.n_pairs} | {LABELS['median']} {row.median_delta_seconds:+.3f}s",fontsize=12)
        else:
            ax.set_title(f"{LABELS[row.phase]} | n={row.n_pairs}")
            ax.text(.5,.5,LABELS['insufficient'],transform=ax.transAxes,ha='center')
        ax.set(xlabel=LABELS['lap_number'],ylim=limits);format_axes(ax)
    axes[0].set_ylabel(LABELS['paired_difference'])
    fig.text(.08,.87,LABELS['pace_subtitle'],fontsize=11)
    finish(fig,LABELS['pace_title'],LABELS['pace_note'],'02_candidate_paired_pace.png')
    fig,ax=plt.subplots(figsize=(12,4));fig.subplots_adjust(top=.72,bottom=.28,left=.10,right=.97)
    for y,driver in [(1,63),(0,3)]:
        for stint in sources['stints'].query('driver_number == @driver').itertuples():
            colour=GOLD if stint.compound=='MEDIUM' else PINK
            ax.broken_barh([(stint.lap_start-.5,stint.lap_end-stint.lap_start+1)],(y-.25,.5),
                          facecolors=colour,edgecolors='white',linewidth=1.5)
            label=f"{LABELS[stint.compound]}\n{LABELS['age']} {stint.tyre_age_at_start}"
            ax.text((stint.lap_start+stint.lap_end)/2,y,label,ha='center',va='center',fontsize=9)
    ax.set(xlim=(.5,51.5),ylim=(-.6,1.6),xlabel=LABELS['lap_number'],yticks=[0,1],yticklabels=['VER','RUS'])
    ax.spines[['top','right','left']].set_visible(False)
    fig.text(.08,.82,LABELS['tyre_subtitle'],fontsize=11)
    finish(fig,LABELS['tyre_title'],LABELS['tyre_note'],'03_tyre_context.png')
    return out


def save_results(root,sources,pair,events,gaps,top10,audit,periods,reviews,tagged,paired,summary,sensitivity):
    """Keep calculation tables shared across languages; export language-specific notes."""
    common=root/'data/processed/v3';common.mkdir(parents=True,exist_ok=True)
    key_events=events[(events.category.eq('SafetyCar')) | events.message.str.contains('ALL CARS THROUGH THE PIT LANE',na=False)]
    # Attach only the latest past gap to each event; stale or missing samples stay blank.
    event_timing=pd.merge_asof(key_events.sort_values('time_utc'),
        gaps[['time_utc','gap_seconds']].rename(columns={'time_utc':'gap_sample_utc'}),
        left_on='time_utc',right_on='gap_sample_utc',direction='backward',
        tolerance=pd.Timedelta(seconds=GAP_TOLERANCE_SECONDS))
    event_timing['gap_sample_age_seconds']=(event_timing.time_utc-event_timing.gap_sample_utc).dt.total_seconds()
    assert event_timing.gap_sample_age_seconds.dropna().between(0,GAP_TOLERANCE_SECONDS).all()
    for name,frame in {'key_events_with_gap':event_timing,'candidate_flag_periods':periods,
                       'race_control_review_items':reviews,'driver_lap_exclusions':tagged,
                       'paired_lap_audit':paired,'candidate_pace_summary':summary,
                       'sensitivity_summary':sensitivity,'top10_context':top10,
                       'main_pair_stints':sources['stints'][sources['stints'].driver_number.isin(PAIR)]}.items():
        frame.to_csv(common/f'{name}.csv',index=False,encoding='utf-8-sig')
    audit.update(analysis_status='PROVISIONAL_RACE_CONTROL_REVIEW_PENDING',
                 candidate_sc_periods=int(periods.kind.eq('SC').sum()),
                 candidate_yellow_periods=int(periods.kind.eq('YELLOW').sum()),
                 race_control_review_items=len(reviews),
                 pair_join_rows=len(paired),candidate_summary=summary.astype(object).where(summary.notna(),None).to_dict('records'))
    (common/'analysis_audit.json').write_text(json.dumps(audit,indent=2,ensure_ascii=False,allow_nan=False))
    out=plot_results(root,sources,pair,gaps,periods,paired,summary)
    notes=LABELS['learning_notes']+'\n\n'+summary[['phase','n_pairs','median_delta_seconds','iqr_delta_seconds']].to_string(index=False)
    (out/'interpretation.txt').write_text(notes,encoding='utf-8')
    print(summary[['phase','n_pairs','median_delta_seconds','iqr_delta_seconds']].to_string(index=False))
    print(LABELS['pending'])
    return out


def main():
    # 1. Understand the race and audit the saved inputs.
    sources,pair,events,gaps,top10,audit=load_and_validate(ROOT)
    # 2. Keep exclusion reasons visible; boundaries are still provisional.
    periods,reviews=build_candidate_periods(pair,events)
    tagged,paired=select_candidate_pairs(pair,periods)
    # 3. Compare paired pace and inspect sensitivity and tyre context.
    summary=summarize_pace(paired)
    sensitivity=sensitivity_check(pair,periods)
    save_results(ROOT,sources,pair,events,gaps,top10,audit,periods,reviews,tagged,paired,summary,sensitivity)


if __name__ == '__main__':
    main()
