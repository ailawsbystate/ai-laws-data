"""Fetch the published AI Laws by State data files and store them here.

Runs weekly from .github/workflows/snapshot.yml. Files are written only when the
list of laws (or the per-state counts) actually changed, so the git history is a
record of real changes, and each change also gets a dated copy in snapshots/.

The script refuses to overwrite good data with a broken export: it checks that
the three files agree with each other before writing anything.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import pathlib
import sys
import urllib.request
from datetime import datetime, timezone

BASE = "https://www.ailawsbystate.com/data/"
FILES = ("ai-laws.csv", "ai-laws-by-state.csv", "ai-laws.json")
ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
SNAPSHOTS = ROOT / "snapshots"
UA = "ai-laws-data-snapshot (+https://github.com/ailawsbystate/ai-laws-data)"
MIN_LAWS = 100          # a sanity floor, far below the real count
JURISDICTIONS = 51      # 50 states and D.C. in the by-state file


def fetch(name: str) -> bytes:
    req = urllib.request.Request(BASE + name, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        if r.status != 200:
            raise SystemExit(f"{name}: HTTP {r.status}")
        return r.read()


def check(blobs: dict) -> dict:
    doc = json.loads(blobs["ai-laws.json"])
    laws = doc["laws"]
    rows = list(csv.DictReader(io.StringIO(blobs["ai-laws.csv"].decode("utf-8"))))
    states = list(csv.DictReader(io.StringIO(blobs["ai-laws-by-state.csv"].decode("utf-8"))))
    problems = []
    if len(laws) < MIN_LAWS:
        problems.append(f"only {len(laws)} laws in ai-laws.json")
    if len(rows) != len(laws):
        problems.append(f"ai-laws.csv has {len(rows)} rows, ai-laws.json has {len(laws)} laws")
    if doc["totals"]["all"] != len(laws):
        problems.append("ai-laws.json totals do not match its list")
    if len(states) != JURISDICTIONS:
        problems.append(f"ai-laws-by-state.csv has {len(states)} rows")
    state_total = sum(int(s["enacted_ai_laws"]) for s in states)
    non_federal = sum(1 for l in laws if l["jurisdiction_code"] != "US")
    if state_total != non_federal:
        problems.append(f"by-state total {state_total} != {non_federal} state and D.C. laws")
    if problems:
        raise SystemExit("Export failed checks, nothing written:\n- " + "\n- ".join(problems))
    return doc


def fingerprint(doc: dict, states_csv: bytes) -> str:
    """What counts as a change: the laws and the per-state counts, not timestamps."""
    h = hashlib.sha256()
    h.update(json.dumps(doc["laws"], sort_keys=True).encode())
    h.update(states_csv)
    return h.hexdigest()


def main() -> int:
    blobs = {name: fetch(name) for name in FILES}
    doc = check(blobs)
    new = fingerprint(doc, blobs["ai-laws-by-state.csv"])
    manifest_path = DATA / "manifest.json"
    old = json.loads(manifest_path.read_text())["fingerprint"] if manifest_path.exists() else None
    if new == old:
        print("No change since the last snapshot.")
        return 0

    DATA.mkdir(exist_ok=True)
    (DATA / "ai-laws.csv").write_bytes(blobs["ai-laws.csv"])
    (DATA / "ai-laws-by-state.csv").write_bytes(blobs["ai-laws-by-state.csv"])
    (DATA / "ai-laws.json").write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
    day = doc["as_of"]
    SNAPSHOTS.mkdir(exist_ok=True)
    (SNAPSHOTS / f"ai-laws-{day}.csv").write_bytes(blobs["ai-laws.csv"])
    totals = doc["totals"]
    manifest = {
        "source": "https://www.ailawsbystate.com/press/embeds",
        "as_of": day,
        "fetched_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "laws": len(doc["laws"]),
        "totals": totals,
        "license": doc["license"],
        "fingerprint": new,
        "sha256": {name: hashlib.sha256(blobs[name]).hexdigest() for name in FILES},
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Updated: {len(doc['laws'])} laws as of {day}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
