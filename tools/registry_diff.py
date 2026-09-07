#!/usr/bin/env python3
"""B2 registry diff (P1 fix, 2026-09-01): OpenRouter model-listing diff vs the cached
snapshot. Runs weekly in CI (.github/workflows/registry-diff.yml), where egress is open,
because the cloud sweep sandbox cannot reach openrouter.ai (measured 2026-08-31). The
source-sweep skill READS the report this writes; it no longer fetches the registry itself
in cloud runs. Local sessions can run this directly.

Writes: _workspace-notes/sweeps/.openrouter-registry.json (snapshot, overwritten)
        _workspace-notes/sweeps/.registry-diff-latest.md   (report, overwritten)
Both are dot-prefixed on purpose: out of Obsidian's view and outside the reminder
workflow's *.md glob. Exits 1 on fetch failure so CI fails loudly (guarantee not in force).
"""
import datetime
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SNAP = os.path.join(ROOT, "_workspace-notes", "sweeps", ".openrouter-registry.json")
REPORT = os.path.join(ROOT, "_workspace-notes", "sweeps", ".registry-diff-latest.md")


def fetch():
    # curl instead of urllib: the local python.org build lacks macOS trust certs, and
    # curl uses the system store on both macOS and the CI runner.
    out = subprocess.run(
        ["curl", "-sS", "--max-time", "30", "https://openrouter.ai/api/v1/models"],
        capture_output=True, text=True, check=True)
    data = json.loads(out.stdout)["data"]
    return {m["id"]: {"name": m.get("name"), "ctx": m.get("context_length"),
                      "prompt": m.get("pricing", {}).get("prompt"),
                      "completion": m.get("pricing", {}).get("completion")} for m in data}


def main():
    today = datetime.date.today().isoformat()
    try:
        live = fetch()
    except Exception as e:
        sys.exit(f"registry fetch FAILED ({type(e).__name__}: {e}); "
                 "snapshot NOT touched; the B2 guarantee is not in force this week.")
    old = {}
    old_date = "none"
    if os.path.exists(SNAP):
        snap = json.load(open(SNAP, encoding="utf-8"))
        old, old_date = snap.get("models", {}), snap.get("snapshot_date", "unknown")
    added = sorted(set(live) - set(old))
    removed = sorted(set(old) - set(live))
    lines = [f"# Registry diff (generated {today}; baseline snapshot {old_date})", ""]
    lines.append(f"Listing: {len(live)} models. Added since baseline: {len(added)}. "
                 f"Removed: {len(removed)}.")
    if added:
        lines.append("")
        lines.append("## Added")
        for mid in added:
            m = live[mid]
            lines.append(f"- `{mid}` | {m['name']} | ctx {m['ctx']} | in {m['prompt']} / out {m['completion']}")
    if removed:
        lines.append("")
        lines.append("## Removed")
        for mid in removed:
            lines.append(f"- `{mid}` | {old[mid].get('name')}")
    if not added and not removed:
        lines.append("")
        lines.append("No membership changes; a genuinely quiet week at the registry.")
    lines.append("")
    lines.append("Stealth/new-model standing conclusions live in the source-sweep skill; "
                 "this report is data for its buzz section.")
    with open(REPORT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    json.dump({"snapshot_date": today, "models": live}, open(SNAP, "w", encoding="utf-8"),
              indent=0, sort_keys=True)
    print(f"diff written: +{len(added)} -{len(removed)} (of {len(live)}); "
          f"baseline was {old_date}")


if __name__ == "__main__":
    main()
