#!/usr/bin/env python3
"""P2: deterministic structural wiki lint (adopted 2026-09-01; v1.1 after adversarial
review same day; v1.2 adds the P3-a checks, decisions/2026-09.md).

The code half of /lint, after the Zissa Wiki pattern: structural checks run here,
deterministically, against tools/wiki-lint-conventions.toml; judgment checks
(contradictions, staleness, promotion candidates) stay with the model pass. REPORT-ONLY:
never writes. Fixes remain governed by the workspace CLAUDE.md auto-fix allowlist.

Scope: every <project>/wiki/ plus <project>/_project.md. Projects are DISCOVERED by
globbing */wiki under the workspace root, so a new wiki is covered automatically.

P3-a checks (2026-09-01): sources-path existence (every repo path cited in a sources list
must exist; prose, URLs, and author-year entries skipped) and upstream drift (a cited page
updated after the citing page is an INFO re-read pointer, never a defect - raw/ is
immutable, so drift only exists between wiki pages).

Known limits (recorded in the 2026-09-01 review, fix in v2): ambiguous wikilinks credit
all candidates; case-sensitivity not normalized; typed-relation reciprocity and
confidence-required-by-status unchecked; no type enum; no duplicate-key flag; no
hard-wrap heuristic; angle-bracket/%20 link forms unmatched; task checks read raw text;
inbound credit from archived pages still counts.

Usage: python3 tools/wiki_lint.py [project ...]   (no args = all discovered projects)
"""
import os
import re
import sys
import tomllib
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONF = os.path.join(ROOT, "tools", "wiki-lint-conventions.toml")
WOZ_CUTOVER = "2026-07-01"


def load_conf():
    with open(CONF, "rb") as f:
        return tomllib.load(f)


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


def strip_noise(text):
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    return re.sub(r"`[^`\n]*`", "", text)


def discover_projects():
    out = []
    for d in sorted(os.listdir(ROOT)):
        if os.path.isdir(os.path.join(ROOT, d, "wiki")) and not d.startswith((".", "_")):
            out.append(d)
    return out


def lint(proj, conf):
    g = conf["global"]
    pc = conf.get("project", {}).get(proj, {})
    if proj not in conf.get("project", {}):
        print(f"\n=== {proj}: NOTE - no [project.{proj}] table in wiki-lint-conventions.toml; global rules only ===")
    wiki = os.path.join(ROOT, proj, "wiki")
    if not os.path.isdir(wiki):
        print(f"\n=== {proj}: UNSCANNED - no wiki/ directory ===")
        return
    pages = {}
    for dirpath, _, files in os.walk(wiki):
        for fn in files:
            if fn.endswith(".md"):
                p = os.path.join(dirpath, fn)
                pages[p] = open(p, encoding="utf-8", errors="replace").read()
    projmd = os.path.join(ROOT, proj, "_project.md")
    if os.path.exists(projmd):
        pages[projmd] = open(projmd, encoding="utf-8", errors="replace").read()
    basenames = defaultdict(list)
    for p in pages:
        basenames[os.path.splitext(os.path.basename(p))[0]].append(p)
    viol, info = defaultdict(list), defaultdict(list)
    inbound = defaultdict(int)
    fms = {}
    edges = set()
    held = set(pc.get("held_pages", []))
    archived_dirs = set(g["archived_dirs"])
    info_dirs = set(pc.get("info_only_dirs", []))
    ws_enum = set(g["status_enum"])
    fb_enum = set(g["feedback_status_enum"])
    legacy = set(pc.get("legacy_status_enum", []))
    prose_ok = pc.get("legacy_status_prose_ok", False)

    def rel(p):
        return os.path.relpath(p, wiki) if p.startswith(wiki) else os.path.basename(p)

    def top_dir(p):
        r = rel(p)
        return r.split(os.sep)[0] if os.sep in r else ""

    for path, text in pages.items():
        r, base = rel(path), os.path.basename(path)
        in_info_dir = top_dir(path) in info_dirs or top_dir(path) in archived_dirs
        sink = info if in_info_dir else viol
        if "�" in text:
            viol["encoding-corruption (U+FFFD present)"].append(r)
        fms[path] = frontmatter(text) or {}
        # frontmatter
        if base not in g["frontmatter_exempt_files"] and r not in pc.get("extra_frontmatter_exempt", []):
            fm = fms[path] if frontmatter(text) is not None else None
            if fm is None:
                sink["missing-frontmatter"].append(r)
            else:
                for k in g["required_keys"]:
                    if k == "status" and base in g["status_exempt_files"]:
                        continue
                    if k == "sources" and base in g["sources_exempt_files"]:
                        continue
                    if k not in fm:
                        sink[f"frontmatter-missing-{k}"].append(r)
                    elif not fm[k]:
                        sink[f"frontmatter-empty-{k}"].append(r)
                # sources-path existence (P3-a, adopted 2026-09-01): a cited repo path
                # must exist. Prose descriptors, URLs, and author-year entries are skipped.
                src = fm.get("sources", [])
                for s in (src if isinstance(src, list) else [src]):
                    s0 = s.split(" (")[0].strip()
                    if s0.startswith("http") or "/" not in s0 or " " in s0:
                        continue
                    cands = [os.path.join(ROOT, proj, s0), os.path.join(wiki, s0),
                             os.path.normpath(os.path.join(ROOT, proj, s0))]
                    if not any(os.path.exists(c) for c in cands):
                        sink["sources-path-missing"].append(f"{r} -> {s0}")
                st = fm.get("status", "")
                ok_here = ws_enum | (fb_enum if top_dir(path) == "feedback" else set())
                if st and st not in ok_here:
                    created = fm.get("created", "")
                    cutover = pc.get("legacy_cutover", "")
                    in_window = not cutover or not created or created < cutover
                    is_legacy = (st in legacy or prose_ok) and in_window
                    if is_legacy:
                        info["legacy-status (protected, do not migrate)"].append(f"{r} ({st[:40]})")
                    elif st in fb_enum:
                        sink["feedback-enum-outside-feedback-dir"].append(f"{r} ({st})")
                    else:
                        sink["status-outside-enum"].append(f"{r} ({st[:40]})")
        # links
        body = strip_noise(text)
        link_sink = info if (r in held or base in held or in_info_dir) else viol
        skip_links = base in g.get("link_check_exempt_files", [])
        for m in re.finditer(r"\]\(([^)\s]+?\.md)(#[^)]*)?\)", body):
            target = m.group(1)
            tgt = os.path.normpath(os.path.join(os.path.dirname(path), target))
            stem = os.path.splitext(os.path.basename(target))[0]
            has_dir = "/" in target.replace("./", "")
            if tgt in pages:
                inbound[tgt] += 1
                edges.add((path, tgt))
            elif not has_dir and len(basenames.get(stem, [])) == 1:
                inbound[basenames[stem][0]] += 1
                edges.add((path, basenames[stem][0]))
            elif not skip_links:
                if os.path.exists(tgt) or os.path.exists(os.path.join(ROOT, target)):
                    continue  # resolves outside the wiki (drafts/, CLAUDE.md, vault-root style)
                if not has_dir and len(basenames.get(stem, [])) > 1:
                    link_sink["ambiguous-basename-link"].append(f"{r} -> {target}")
                else:
                    link_sink["dangling-md-link"].append(f"{r} -> {target}")
        for m in re.finditer(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]", body):
            name = m.group(1).strip()
            if not name or name == "...":
                continue
            if "/" in name:
                cand = os.path.normpath(os.path.join(wiki, name + ".md"))
                if cand in pages:
                    inbound[cand] += 1
                    edges.add((path, cand))
                elif not skip_links and not os.path.exists(os.path.join(ROOT, proj, name)):
                    link_sink["dangling-wikilink"].append(f"{r} -> [[{name}]]")
                continue
            if "." in name:
                continue  # embeds/files: v2
            if name in basenames:
                for p2 in basenames[name]:
                    inbound[p2] += 1
                    edges.add((path, p2))
            elif not skip_links:
                link_sink["dangling-wikilink"].append(f"{r} -> [[{name}]]")
        # task-field integrity (mistake #7)
        if base not in g["task_check_exempt_files"]:
            for i, line in enumerate(text.split("\n"), 1):
                for field in ("due", "owner"):
                    if re.search(rf"\[{field}::\s*\]", line):
                        viol[f"empty-{field}-field"].append(f"{r}:{i}")
                    if re.search(rf"\[{field}::", line) and not re.match(r"\s*-\s*\[[ xX]\]", line):
                        viol[f"{field}-field-off-task-line"].append(f"{r}:{i}")
    # upstream drift (P3-a, adopted 2026-09-01): a cited page updated after the citing
    # page is a re-read pointer, INFO only - it never implies a defect in either page.
    def fdate(path_, key):
        v = fms.get(path_, {}).get(key, "")
        m_ = re.match(r"(\d{4}-\d{2}-\d{2})", v if isinstance(v, str) else "")
        return m_.group(1) if m_ else ""
    drift_structural = {"index.md", "log.md", "translations.md", "standing-items.md", "_project.md", "overview.md"}
    for a, b in sorted(edges):
        if a == b or os.path.basename(b) in drift_structural or os.path.basename(a) in drift_structural:
            continue
        if top_dir(a) in archived_dirs:
            continue
        ua, ub = fdate(a, "updated"), fdate(b, "updated")
        if ua and ub and ub > ua:
            info["upstream-drift (cited page updated later; re-read pointer)"].append(
                f"{rel(a)} (@{ua}) cites {rel(b)} (@{ub})")
    # orphans + index drift
    structural = {"index.md", "log.md", "translations.md", "standing-items.md", "_project.md", "overview.md"}
    idx = pages.get(os.path.join(wiki, "index.md"), "")
    for path in pages:
        base = os.path.basename(path)
        if base in structural or top_dir(path) in archived_dirs or top_dir(path) in info_dirs:
            continue
        stem = os.path.splitext(base)[0]
        linked_from_index = re.search(r"(?<![\w-])" + re.escape(stem) + r"(?![\w-])", idx) is not None
        if inbound[path] == 0 and not linked_from_index:
            info["orphan (no inbound link, not in index)"].append(rel(path))
        elif not linked_from_index:
            info["not-in-index"].append(rel(path))
    # log presence + order
    logp = os.path.join(wiki, "log.md")
    if logp not in pages:
        viol["log-missing"].append("wiki/log.md absent")
    else:
        dates = re.findall(r"^#{1,4} \[?(\d{4}-\d{2}-\d{2})|^\*\*(\d{4}-\d{2}-\d{2})\*\*", pages[logp], re.M)
        flat = [a or b for a, b in dates]
        if not flat and re.search(r"\d{4}-\d{2}-\d{2}", pages[logp]):
            info["log-format-not-recognized (order unchecked)"].append("log.md")
        bad = [i for i in range(len(flat) - 1) if flat[i] < flat[i + 1]]
        if bad:
            viol["log-out-of-order"].append(f"log.md (first inversion at entry {bad[0] + 1})")

    print(f"\n=== {proj}: {len(pages)} pages ===")
    for label, sink in (("VIOLATION", viol), ("INFO", info)):
        for cat in sorted(sink):
            hits = sink[cat]
            print(f"  {label} [{cat}] {len(hits)}")
            for h in hits[:5]:
                print(f"      {h}")
            if len(hits) > 5:
                print(f"      ... +{len(hits) - 5} more")
    print(f"  totals: {sum(len(v) for v in viol.values())} violations, {sum(len(v) for v in info.values())} info")


if __name__ == "__main__":
    conf = load_conf()
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    projs = args or discover_projects()
    known = discover_projects()
    for proj in projs:
        if proj not in known:
            print(f"\n=== {proj}: UNKNOWN PROJECT (no {proj}/wiki under workspace root) ===")
        lint(proj, conf)
