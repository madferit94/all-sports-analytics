from __future__ import annotations

import argparse
import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import pandas as pd
import requests


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "sofascore"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; WorldCup2026 research notebook)",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.sofascore.com/",
}


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def save_json_response(url: str, output_dir: Path, source_name: str) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    response = requests.get(url, headers=HEADERS, timeout=30)
    response.raise_for_status()

    text = response.text
    digest = sha256_text(text)[:12]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = output_dir / f"{timestamp}_{source_name}_{digest}.json"
    meta_path = output_dir / f"{timestamp}_{source_name}_{digest}.metadata.json"

    json_path.write_text(text, encoding="utf-8")
    meta_path.write_text(
        json.dumps(
            {
                "source_name": source_name,
                "url": url,
                "status_code": response.status_code,
                "fetched_at_utc": utc_now_iso(),
                "content_sha256": sha256_text(text),
                "json_path": str(json_path.relative_to(PROJECT_ROOT)),
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    return json_path


def read_event_ids(path: Path) -> list[int]:
    df = pd.read_csv(path)
    if "event_id" not in df.columns:
        raise ValueError(f"{path} must contain an event_id column")
    return [int(event_id) for event_id in df["event_id"].dropna().unique()]


def collect_event_details(event_ids: Iterable[int], sleep_seconds: float = 2.0) -> None:
    endpoints = {
        "event": "https://www.sofascore.com/api/v1/event/{event_id}",
        "statistics": "https://www.sofascore.com/api/v1/event/{event_id}/statistics",
        "lineups": "https://www.sofascore.com/api/v1/event/{event_id}/lineups",
        "incidents": "https://www.sofascore.com/api/v1/event/{event_id}/incidents",
    }

    for index, event_id in enumerate(event_ids, start=1):
        print(f"[{index}] event {event_id}")
        for name, template in endpoints.items():
            url = template.format(event_id=event_id)
            try:
                save_json_response(url, RAW_DIR / name, f"{event_id}_{name}")
                print(f"  saved {name}")
            except requests.HTTPError as exc:
                print(f"  skipped {name}: {exc}")
            time.sleep(sleep_seconds)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--event-ids",
        type=Path,
        default=PROCESSED_DIR / "sofascore_event_ids.csv",
        help="CSV containing an event_id column.",
    )
    parser.add_argument("--sleep", type=float, default=2.0)
    args = parser.parse_args()

    event_ids = read_event_ids(args.event_ids)
    collect_event_details(event_ids, sleep_seconds=args.sleep)


if __name__ == "__main__":
    main()
