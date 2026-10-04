# Full-race replay walkthrough

[English](v4_replay_guide.md) · [한국어](v4_replay_guide.ko.md)

Follow two cars on the same UTC clock across all 51 recorded laps. The 98m 02.755s race interval becomes a 4m 05.2s MP4 at 24× base speed and 20fps.

1. Open `outputs/en/v4/replay.html` for lap seeking, SC1/SC2/last-lap buttons and 12×/24×/48× speed.
2. Run `python scripts/en/v4_full_race_replay.py` after installing requirements.txt. Add `--fetch-missing` only for missing originals. Existing originals are preserved.
3. Run All in `notebooks/en/v4_full_race_replay.ipynb` for a tutorial. It renders three representative frames by default. Set `RENDER_FULL_VIDEO=True` to encode the complete video again.

## Sources and checks

Each full API response contains 37,095 samples, including pre/post-race observations. Preserve the response and select 22,538 race/boundary-support samples per driver. Every one of the 51 laps has source observations. Maximum sample interval is 1.339s; race-window duplicate times and missing coordinates are zero.

Interpolate onto a shared clock only across at most 2s. Hide markers across longer gaps. There are no such gaps in this race interval; a separate synthetic 20s dropout verifies hiding. The outline comes from Russell lap 29. It cannot recover precise racing lines or lateral track placement.

The VER→RUS gap uses published OpenF1 timing, never map-marker distance. Samples older than 12s remain blank; sample age is shown separately. The official final result, **VER +0.196s**, is displayed separately. The estimated final-lap end and timing-update timestamp differ, so the last replay sample can be 0.237s. That sample is not the official finishing margin.

SC shaded ends use next-leader-lap candidates, not verified withdrawal times. Tyre age is age at stint start, not current age or degradation.

## Function map

| Function | Purpose |
|---|---|
| `download_locations` | Download missing raw responses only. |
| `load_replay_inputs` | Verify identity, keys, time range, raw hashes and all 51 laps. |
| `build_replay_frames` | Align position, lap and latest timing on a common frame clock. |
| `save_replay_tables` | Save lap coverage, frame alignment and audits. |
| `make_frame_renderer` | Draw track, markers, lap/tyre context and timeline. |
| `render_video` | Encode MP4 and decode every frame to validate it. |

MP4 is the continuous replay. The GIF is an approximately 14s overview using 80 frames from across the race. V1–V3 and the original short V2 replay remain intact.

Source: [OpenF1 location documentation](https://openf1.org/docs/#location). [Source/frame audit](../data/processed/v4/replay_audit.json) · [Execution check](v4_execution_check.json).

For seeking, run `python src/serve_replays.py --port 8767` from the project and open `http://127.0.0.1:8767/outputs/en/v4/replay.html`. The included byte-range server supports video seeking; a basic `python -m http.server` is insufficient.
