---
name: revise
description: Operate a peer-review revision round — ingest a decision letter into a demand tracker, map each reviewer demand to wiki evidence, draft response-letter and rebuttal text, and run manuscript-consistency sweeps. Use when reviews arrive, when working an R&R (e.g. a journal major revision), when drafting reviewer responses, or before resubmission.
---

# Revise

The review-round workflow that was hand-built for a journal major revision (2026-07-01),
generalized so the next round — and the next venue — does not start from scratch. The woz
artifacts are the canonical shape: raw letter at `raw/reviews/YYYYMMDD-<venue>-review.md`,
tracker at `wiki/reviews/<venue>-YYYY-major-revision.md`, question fan-out in `wiki/questions/`,
challenge banners on contested pages.

Ground rules, non-negotiable:
- Reviews are critique, not data. A review round NEVER promotes anything to `finding`.
- Review content is `reference`; every planned response is `hypothesis`.
- Contested pages get a dated top-of-body banner and `confidence: low`; their original claim
  text stays intact (accuracy rule 6 — flag, never overwrite).
- `raw/final_draft/` (or any submitted manuscript under raw/) is immutable. Paper-side edits
  live as tracker checklist items the researcher replays in Overleaf; this skill never applies
  them.

## Mode A — ingest a round (a decision letter arrived)
1. File the letter verbatim at `raw/reviews/YYYYMMDD-<venue>-review.md` if not already there.
   This is the one raw/ write this skill may make: a NEW file, exact text, never an edit.
2. Two-step like any ingest: analyze first. Report per reviewer: recommendation, role
   (expert/secondary), headline concerns; and a candidate demand list. Wait for confirmation.
3. Build or update the tracker `wiki/reviews/<venue>-<year>-<round>.md` (status `reference`):
   a per-reviewer summary table; a demand matrix with columns
   `# | Demand | Raised by | Class | Owning pages | Response status` where Class is
   Decision / Conjecture / Open-Q; a `- [ ]` minor/length checklist; and a "what this ingest
   did NOT do" section (promotions: none; raw edits: the letter file only).
4. Fan out: each demand that is a genuine open question gets a `wiki/questions/` page
   (`status: hypothesis`, `confidence: low`, sourced to the review file) with at minimum the
   sections The demand / The open question / What would resolve it, extended with
   demand-specific sections as the canonical woz pages do.
5. Banner the contested pages: a uniformly headed dated blockquote
   (`**Reviewer challenge (YYYY-MM-DD) — <venue> <round>.**`) naming the challenging reviewers
   and linking the tracker, with a page-specific body stating exactly which claims on THAT
   page are contested; plus `confidence: low` in frontmatter. List every bannered page in the
   tracker.
6. Bookkeeping: index.md, prepend log.md, flip `_project.md` `stage:` (e.g. under-review →
   revising) and flag a blank `deadline:` — a revising stage with no deadline is the
   dashboard's known worst gap.

## Mode B — work a demand (drafting responses)
1. Pick the demand from the matrix (or take the one the researcher names). Read its owning
   pages and their raw sources; do not load the whole wiki.
2. Evidence discipline: factual rebuttals cite `finding` pages only. A `hypothesis` page
   supports only "we will analyze / we propose" framings. If the response needs a claim that
   is still hypothesis, STOP and say which analysis would license it — same rule as /draft.
3. Draft to `drafts/revision/YYYY-MM-DD-response-<demand-slug>.md` (create `drafts/revision/`
   if absent), status `hypothesis`, voice-matched to `_schema/voice.md`, its
   `# Writing Quality Check` run before saving. Reviewer-facing register: concede plainly what
   is conceded, state the change made, cite the manuscript location.
4. Update the demand's `Response status` in the tracker and prepend a log.md line. Response
   drafts are paste-out material; they never enter `wiki/`.

## Mode C — consistency sweep (before resubmission)
Each sweep is a report-first pass: show the diff, fix wiki-side only after confirmation, and
never touch raw/.
- **N-discipline**: every analytic claim uses the project's analytic constants (workspace
  CLAUDE.md mistake #15 — for woz, the analytic N excludes one participant; flag denominators
  that use the recruited N and missing N-banners).
- **Numbering**: wiki table/figure references vs the named manuscript PDF, claim by claim (the
  woz 2026-07-01 pass diffed 100 claims; expect that scale).
- **Banner audit**: every tracker-listed contested page still carries its banner and
  `confidence: low`; every resolved demand's banner is flagged for researcher removal (not
  auto-removed).
- **Checklist audit**: tracker checkboxes vs reality; stale `Response status` cells.

A full-manuscript Mode C sweep or cross-reviewer synthesis is Tier 3 case (d) — ask before
escalating. Modes A and B are Tier 2.
