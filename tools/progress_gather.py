#!/usr/bin/env python3
"""Deterministic gather step for the current-progress skill (prompt-audit hunk 13,
2026-09-03). The skill's narrate and verify steps stay with the model; this script owns
the counting. REPORT-ONLY: never writes.

It implements the _dashboard.md Dataview queries in code, so the snapshot's numbers come
from one place every run instead of ad-hoc grep/awk:

  - _project.md frontmatter: stage, venue, deadline (+ days left / OVERDUE), last_ingested
  - Documents in flight: `doc_type::` lines whose status is not approved/submitted
  - Open action items: unchecked tasks in _project.md and wiki/feedback/, no doc_type,
    priority from a leading 🔴/🟡/🟢 marker, `[due:: ]` bucketed overdue / 7d / later / undated
  - Part-done `[~]` actions, counted separately (neither open nor done)
  - Open questions: type question + status hypothesis (with age since `updated`)
  - Stale hypotheses: any hypothesis-status page not updated for STALE_DAYS
  - Open feedback: type feedback + status open
  - Status roster: every wiki page by type/status/confidence (frontmatter only)
  - Newest log.md header date, and the last human commit (scheduled-routine subjects skipped)

Usage: python3 tools/progress_gather.py [project ...] [--json]   (no args = all projects)
"""
import datetime as dt
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STALE_DAYS = 60
ROUTINE_SUBJECT = re.compile(r"^Weekly (delta \+ lint|source sweep)", re.I)
TODAY = dt.date.today()


def frontmatter(text):
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end < 0:
        return None
    fm = {}
    cur_list_key = None
    for line in text[4:end].split("\n"):
        m = re.match(r"^(\w[\w_-]*):\s*(.*)$", line)
        if m:
            key, raw = m.group(1), m.group(2).strip()
            raw = re.sub(r"\s+#.*$", "", raw)  # trailing YAML comment
            if raw.startswith("[") and raw.endswith("]"):
                fm[key] = [x.strip().strip('"').strip("'") for x in raw[1:-1].split(",") if x.strip()]
                cur_list_key = None
            elif raw:
                fm[key] = raw.strip('"').strip("'")
                cur_list_key = None
            else:
                fm[key] = []
                cur_list_key = key
        elif cur_list_key is not None:
            lm = re.match(r"^\s+-\s+(.*)$", line)
            if lm:
                fm[cur_list_key].append(lm.group(1).strip().strip('"').strip("'"))
            elif line.strip():
                cur_list_key = None
    return fm


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def parse_date(s):
    if not isinstance(s, str):
        return None
    m = re.match(r"(\d{4}-\d{2}-\d{2})", s)
    return dt.date.fromisoformat(m.group(1)) if m else None


def discover_projects():
    return sorted(
        d for d in os.listdir(ROOT)
        if os.path.isfile(os.path.join(ROOT, d, "_project.md")) and not d.startswith((".", "_"))
    )


TASK_RE = re.compile(r"^\s*- \[( |x|X|~)\] (.*)$")
FIELD_RE = re.compile(r"\[(\w+)::\s*([^\]]*)\]")


def parse_task(line):
    m = TASK_RE.match(line)
    if not m:
        return None
    state, text = m.group(1), m.group(2)
    fields = {k: v.strip() for k, v in FIELD_RE.findall(text)}
    prio = "high" if "🔴" in text else "medium" if "🟡" in text else "low" if "🟢" in text else "normal"
    clean = FIELD_RE.sub("", text)
    clean = re.sub(r"[🔴🟡🟢]", "", clean).strip()
    return {
        "state": {" ": "open", "~": "partial"}.get(state, "done"),
        "text": clean,
        "priority": prio,
        "due": parse_date(fields.get("due")),
        "doc_type": fields.get("doc_type"),
        "doc_status": fields.get("status"),
        "owner": fields.get("owner"),
    }


def bucket(due):
    if due is None:
        return "undated"
    if due < TODAY:
        return "overdue"
    if due <= TODAY + dt.timedelta(days=7):
        return "due_7d"
    return "later"


def last_human_commit(project):
    try:
        out = subprocess.run(
            ["git", "log", "--format=%as\t%s", "-n", "40", "--", project],
            cwd=ROOT, capture_output=True, text=True, check=True,
        ).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    for line in out.splitlines():
        date, _, subject = line.partition("\t")
        if not ROUTINE_SUBJECT.match(subject):
            return {"date": date, "subject": subject}
    return None


def newest_log_date(log_path):
    if not os.path.isfile(log_path):
        return None
    for line in read(log_path).splitlines():
        m = re.match(r"^#{1,3} \[?(\d{4}-\d{2}-\d{2})", line)
        if m:
            return m.group(1)
    return None


def gather(project):
    pdir = os.path.join(ROOT, project)
    pfile = os.path.join(pdir, "_project.md")
    ptext = read(pfile)
    pfm = frontmatter(ptext) or {}
    deadline = parse_date(pfm.get("deadline"))
    if deadline:
        days = (deadline - TODAY).days
        time_left = "OVERDUE" if days < 0 else f"{days} days"
    else:
        time_left = "no deadline"

    docs, tasks = [], []
    for line in ptext.splitlines():
        t = parse_task(line)
        if not t:
            continue
        if t["doc_type"]:
            docs.append(t)
        else:
            t["source"] = "_project.md"
            tasks.append(t)

    fb_dir = os.path.join(pdir, "wiki", "feedback")
    feedback = []
    if os.path.isdir(fb_dir):
        for name in sorted(os.listdir(fb_dir)):
            if not name.endswith(".md"):
                continue
            path = os.path.join(fb_dir, name)
            text = read(path)
            fm = frontmatter(text) or {}
            rel = f"wiki/feedback/{name}"
            for line in text.splitlines():
                t = parse_task(line)
                if t and not t["doc_type"]:
                    t["source"] = rel
                    tasks.append(t)
            if fm.get("type") == "feedback":
                feedback.append({
                    "page": rel,
                    "status": fm.get("status"),
                    "source": fm.get("source"),
                    "meeting": fm.get("meeting"),
                    "target": fm.get("target"),
                })

    roster, questions, stale = [], [], []
    wiki = os.path.join(pdir, "wiki")
    for dirpath, _, files in os.walk(wiki):
        for name in sorted(files):
            if not name.endswith(".md"):
                continue
            path = os.path.join(dirpath, name)
            fm = frontmatter(read(path))
            if fm is None:
                continue
            rel = os.path.relpath(path, pdir)
            updated = parse_date(fm.get("updated"))
            row = {
                "page": rel,
                "type": fm.get("type"),
                "status": fm.get("status"),
                "confidence": fm.get("confidence"),
                "updated": updated.isoformat() if updated else None,
            }
            roster.append(row)
            age = (TODAY - updated).days if updated else None
            if fm.get("type") == "question" and fm.get("status") == "hypothesis":
                questions.append({**row, "age_days": age})
            if fm.get("status") == "hypothesis" and age is not None and age >= STALE_DAYS:
                stale.append({**row, "age_days": age})

    open_tasks = [t for t in tasks if t["state"] == "open"]
    partial = [t for t in tasks if t["state"] == "partial"]
    prio_rank = {"high": 0, "medium": 1, "normal": 2, "low": 3}
    open_tasks.sort(key=lambda t: (prio_rank[t["priority"]], t["due"] or dt.date.max))
    buckets = {"overdue": [], "due_7d": [], "later": [], "undated": []}
    for t in open_tasks:
        buckets[bucket(t["due"])].append(t)

    status_counts = {}
    for r in roster:
        status_counts[r["status"] or "MISSING"] = status_counts.get(r["status"] or "MISSING", 0) + 1

    return {
        "project": project,
        "meta": {
            "stage": pfm.get("stage"), "venue": pfm.get("venue"),
            "deadline": deadline.isoformat() if deadline else None, "time_left": time_left,
            "last_ingested": pfm.get("last_ingested"),
        },
        "docs_in_flight": [d for d in docs if d["doc_status"] not in ("approved", "submitted")],
        "docs_all": len(docs),
        "open_tasks": open_tasks, "task_buckets": {k: len(v) for k, v in buckets.items()},
        "partial_tasks": partial, "done_tasks": sum(1 for t in tasks if t["state"] == "done"),
        "open_questions": questions, "stale_hypotheses": stale,
        "feedback_open": [f for f in feedback if f["status"] == "open"], "feedback_all": len(feedback),
        "status_counts": status_counts, "pages": len(roster),
        "log_newest": newest_log_date(os.path.join(wiki, "log.md")),
        "last_human_commit": last_human_commit(project),
    }


def fmt_task(t):
    due = f" due {t['due']}" if t["due"] else ""
    return f"    [{t['priority']}]{due} {t['text'][:90]}  ({t['source']})"


def render(g):
    m = g["meta"]
    lines = [f"== {g['project']} ==",
             f"stage={m['stage']} venue={m['venue']} deadline={m['deadline']} ({m['time_left']}) last_ingested={m['last_ingested']}",
             f"log newest={g['log_newest']} last human commit={g['last_human_commit']}",
             f"pages={g['pages']} status counts={g['status_counts']}",
             f"docs in flight={len(g['docs_in_flight'])}/{g['docs_all']}"]
    for d in g["docs_in_flight"]:
        lines.append(f"    {d['doc_type']}: {d['text'][:70]} [status {d['doc_status']}] due {d['due']}")
    lines.append(f"open tasks={len(g['open_tasks'])} buckets={g['task_buckets']} partial={len(g['partial_tasks'])} done={g['done_tasks']}")
    for t in g["open_tasks"]:
        lines.append(fmt_task(t))
    for t in g["partial_tasks"]:
        lines.append("    [~]" + fmt_task(t)[4:])
    lines.append(f"open questions={len(g['open_questions'])}")
    for q in g["open_questions"]:
        lines.append(f"    {q['page']} conf={q['confidence']} age={q['age_days']}d")
    lines.append(f"stale hypotheses (>= {STALE_DAYS}d)={len(g['stale_hypotheses'])}")
    for s in g["stale_hypotheses"]:
        lines.append(f"    {s['page']} age={s['age_days']}d")
    lines.append(f"open feedback={len(g['feedback_open'])}/{g['feedback_all']}")
    for f in g["feedback_open"]:
        lines.append(f"    {f['page']} src={f['source']} meeting={f['meeting']} target={f['target']}")
    return "\n".join(lines)


def main(argv):
    as_json = "--json" in argv
    names = [a for a in argv if not a.startswith("--")] or discover_projects()
    results = [gather(p) for p in names]
    if as_json:
        print(json.dumps(results, indent=1, default=str))
    else:
        print("\n\n".join(render(g) for g in results))


if __name__ == "__main__":
    main(sys.argv[1:])
