---
description: Health-check this wiki
---
Structural pass first: run `python3 tools/wiki_lint.py <project>`
from the workspace root (conventions in tools/wiki-lint-conventions.toml). Its VIOLATION
findings feed this audit's report; its INFO findings are context (documented conventions,
archives, legacy classes), never to-dos. The tool never writes; fixes stay governed by the
allowlist below. The model pass then owns the judgment checks:

Lint this wiki. Audit every page for:
- Orphans and missing cross-references.
- Uncited claims (every wiki claim must cite a raw source).
- Contradictions between pages.
- Stale `hypothesis` pages that now have supporting data in raw/ and could be promoted (report,
  do not auto-promote).
- Missing or malformed frontmatter (status, sources, dates).
- Hard-wrapped lines (a paragraph, bullet, or task split across source lines to fit a column
  width): join them per the schema's line-wrapping rule. Terminal-read config (CLAUDE.md files,
  .claude/, .github/, README.md, SYNC_SETUP.md) is deliberately wrapped and exempt; the
  _schema/ files are Obsidian-read and unwrapped.
- Out-of-order log.md entries: the log must stay reverse-chronological, newest first, with a
  single day's entries kept in the order they were written.
- Contested-upstream exposure: for every page carrying a `contradicts:` key (or a
  contradiction flagged in log.md or wiki/standing-items.md), list the downstream pages and
  drafts that cite, link, or source it without any contest marker. Report the blast radius;
  change nothing.
- Supersession leak: pages citing the target of a `supersedes:` key as if current (outside
  history or provenance passages). Report only.
- Edge-based promotion candidates: `hypothesis` pages with inbound `supports:` edges from
  pages whose own sources include analyzed data in raw/. Report as candidates and restate
  the promotion gate; zero auto-promotions.
- Rule-file freshness (report-only): paths, filenames, command names, and
  agent names referenced by the workspace CLAUDE.md, this project's CLAUDE.md, and _schema/
  files that no longer exist on disk. List under "Reported, not changed"; a lint run never
  edits config files.
Fixes are limited to the auto-fix allowlist in the workspace CLAUDE.md (mistake #4);
everything else is reported, not changed, as a checklist. Typed-relation keys
(`supports`, `contradicts`, `supersedes`, `answers`) are outside the auto-fix allowlist:
report missing or asymmetric `contradicts` pairs, do not add, remove, or repair edges.
Prepend a lint entry to log.md (newest first, directly under the `# Log` heading).

When run by the weekly loop, or when asked to save the report: write it to
drafts/weekly/YYYY-MM-DD-lint.md with full report frontmatter, a `## Result:` summary line (the
Slack CI greps it), a "Reported, not changed" section — citing wiki/standing-items.md IDs
(SI-n) instead of re-deriving prose when that ledger exists — the promotion check, and the
closing attestation: no raw/ edits, no promotions, no claim content changed.
