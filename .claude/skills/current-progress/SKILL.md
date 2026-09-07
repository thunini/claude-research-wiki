---
name: current-progress
description: Snapshot the current state of research progress — what is established (findings), what is in play (hypotheses, docs in flight), what is open or blocked (questions, feedback, overdue tasks), and what is due. Use when asked where a project or the research stands, for a status update or progress summary, when returning to a project after time away, or before planning next steps. Reports state, not change — for what changed over a time window, use /weekly-delta instead.
---

# Current progress

A point-in-time snapshot of where the research stands, grounded in the wiki's own status fields.
State, not change: `/weekly-delta` reports what moved in a git window; this skill reports the
standing position. The two must not blur — the moment this skill computes a git-diff window by
default, it has become a duplicate `/weekly-delta`. Quote the newest weekly-delta report instead.

Read-only contract: never edit a wiki page, never touch a `status:` field, never prepend to
`log.md`. Summarizing must not mutate. This is routine Tier 2 work; it never needs escalation.

## Scope
Run in a project folder for that project; at the workspace root, cover every active project and
close with a cross-project roll-up. If the user names a project, cover only it. At the root,
`projects.md` is read twice wearing two hats: first only to enumerate the project folders, then
again last as the intent layer (see Sources).

## Sources, in reading order (per project)
Read only these. Theme/concept/comparison pages contribute frontmatter via grep, never their
bodies — if this skill is reading page bodies, it has blown its token budget and failed.
1. `_project.md` — frontmatter (stage, venue, deadline, last_ingested), the Documents checklist
   (`[doc_type:: ] [status:: ] [due:: ]` lines), and the Tasks section.
2. `wiki/index.md` — frontmatter `updated` plus the status banner/footer prose. The richest
   "where we are" text, but use it for cross-checks and selective phrase-level quotes only
   (block-quoting a banner would blow the whole project budget), and it is not ground truth:
   cross-check its date against the newest `log.md` entry and flag it when it lags.
3. `wiki/log.md` — the top 1–3 entries only. They carry last-touched date, quiet-week notes, and
   standing blockers; arguably the best single signal in the workspace.
4. `wiki/questions/*.md` — frontmatter only (status, confidence, updated). These are the RQs; a
   `hypothesis`→`finding` flip here is the crispest "RQ answered" event there is.
5. `wiki/feedback/*.md` — frontmatter (status, source, meeting, target) plus the "Resulting
   actions" checkboxes and each item's stated close condition. Projects without `feedback/` may
   hold the same signal elsewhere (e.g. `wiki/reviews/` plus `questions/`); degrade gracefully.
6. `drafts/` filenames (dated drafts are direct writing-stage evidence) and the newest
   `drafts/weekly/*-weekly-delta.md` as a ready-made "recently:" line. A missing `drafts/weekly/`
   is a finding about the weekly automation, not evidence the project is idle.
7. `git log --oneline -- <project>/` — last human-driven commit. Skip scheduled-routine commits
   (subjects like "Weekly delta + lint"), which inflate recency.

At the root, read `projects.md` last, as the intent layer (venue, lines of work, how projects
relate) — never as ground truth for stage. Where it disagrees with wiki evidence, that is a
Drift item to report, not a fact to average away.

## Steps
1. **Gather.** Run `python3 tools/progress_gather.py <project>` from the workspace root. It
   emits the table this skill narrates from: page, type, status, confidence, updated, open
   tasks, due dates, docs in flight, open questions, open feedback, `[~]` part-done actions,
   and the last human commit. It implements the `_dashboard.md` Dataview queries and never
   writes. When a project's real signal lives outside the dashboard's scope (e.g. a
   review-tracker checklist in `wiki/reviews/`), count it in the snapshot and note the
   dashboard blind spot under Drift & gaps. Every number in the snapshot comes from this
   table — the narration adds no counts of its own.
2. **Derive.** Days to deadline, OVERDUE if past — and a missing deadline or venue on a stage
   that implies one (revising, or a project whose drafts are essentially complete) is itself an
   actionable gap, not a null to skip. Hypothesis pages with no update for ~60 days get a stale
   flag. Bucket tasks overdue / due within 7 days / later / undated, overdue first. At-risk join:
   any task due within 7 days whose source page shows no recent activity. Last human activity per
   project: newest `log.md` header date, cross-checked against git — excluding the scheduled
   routine's traces in both places, its commits and its `log.md` entries (e.g. "weekly delta +
   lint (scheduled routine)"), since the weekly loop writes both.
3. **Narrate** in the fixed skeleton below, framing progress against the RQs in `wiki/questions/`
   ("RQ2 moved from hypothesis to finding, cited to the coded corpus") rather than as file lists.
4. **Verify before delivering.** Recheck every claim the snapshot presents as established against
   the gather table: it must cite a page whose frontmatter really says `status: finding`. Statuses
   are quoted, never assigned. Never write "we found" about a `hypothesis` page — meeting
   decisions are plans. A wrong-looking status, or a checkbox contradicting its inline `status::`
   field, is reported under Drift & gaps, never corrected here.

## Output
Fixed per-project skeleton, in this order and with these exact section names, so consecutive
snapshots stay diffable:
- **Status line** — stage, venue, deadline countdown, last human activity, optionally a one-line
  "recently:" quoting the newest weekly-delta headline (quoted, never recomputed).
- **Established** — `finding`-status pages, each cited by path. If a project predates the
  workspace status vocabulary and has no `finding` pages, do not report "none" — that would
  misread a submitted paper as no progress. Quote the established layer from the index banner,
  attributed as quoted prose, and file the vocabulary divergence under Drift & gaps.
- **In play** — active hypotheses, docs in flight, analysis under way.
- **Open / blocked** — open questions (with age), open feedback with its close condition, tasks
  with the overdue bucket first. Count `[~]` part-done actions separately — a naive checkbox
  grep misreads them as open; they are neither open nor done. When feedback or tasks are dense,
  aggregate: give the counts, then name only the top few items by priority marker with their
  close conditions; the rest are drill-down links.
- **Drift & gaps** — stale or contradicting intent fields, missing deadline or last_ingested,
  missing automation, schema-divergent pages. Flag, do not fix.

At the workspace root, close with a cross-project table (project, stage, deadline, last activity,
top blocker) and a prioritized what's-next list with the blocker named per item.

Each project reads as a router-grade summary the researcher can scan without scrolling; it is
not a report. A dense Open / blocked section stretches it by aggregating (counts plus top
items), never by enumerating. Prefer wikilinks and paths for drill-down over inlined detail. Deliver in chat. If asked to save: a
workspace run goes to `_snapshots/YYYY-MM-DD-progress.md` at the root, a single-project run to
`<project>/drafts/progress/YYYY-MM-DD-progress.md`, status `hypothesis`, and — unlike this config
file — with no hard-wrapped lines (one paragraph or bullet per source line; it is read in
Obsidian and greppable by queries).
