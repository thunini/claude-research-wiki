# Research Workspace — Operating Manual

One independent wiki per research project. Each project is its own self-contained `raw/` +
`wiki/` knowledge base. They are deliberately not merged.

- **Cross-project work** (status, what connects to what, which paper is due next): read
  `projects.md`. That is the dashboard.
- **One project**: `cd` into its folder and run there. The project's own CLAUDE.md plus this
  file plus the schema below load automatically.
- **Pulling across projects**: read the other project's files in place (the researcher
  launches with `--add-dir ../other-project` when needed); never copy pages across. Another
  project's findings are cited as `reference` in this project, never restated as `finding`.

The wiki schema applies to all projects:

@_schema/research-wiki-schema.md

## Where rules live, and who wins

1. The researcher's live instruction beats everything below.
2. A project CLAUDE.md beats the schema where it declares an override (e.g. cumpa's privacy
   rule: collaborators named, only study participants pseudonymized) or documents a legacy
   convention (woz's status vocabulary).
3. This file plus the schema govern everything else.
4. Command and skill files under `.claude/` are the binding contracts for their workflows.
   Follow their steps exactly and never skip their confirmation gates because a step happened
   to be automated. They are floors, not ceilings: the quality bars below ADD required checks
   on top of a command's steps; never trim a command's output below its bar.

Interaction style (not rules): `_workspace-notes/collaboration-style.md` records how the
researcher runs decisions and verification with agent sessions (labeled option menus,
adversarial verification before filing, pre-declared acceptance criteria). Read it at the
start of substantive method or analysis work. It guides tone and process shape only and
never overrides anything above (researcher-approved mirror, 2026-08-03).

Chat register (not rules): `_workspace-notes/chat-register.md` governs the phrasing of chat
output in agent sessions (a subset of ASD-STE100 mechanics plus Google developer-documentation
style, adopted 2026-08-12). Same standing as above: phrasing only, confirmation-gate content
is never simplified, and it never overrides anything above.

Known conflicts, already resolved — do not re-litigate them:
- **woz-mobile-agent runs two status vocabularies.** ~70 legacy pages use its project enum
  (`draft | active | review` plus prose statuses like `superseded`). Pages created since
  2026-07-01 use the workspace enum. Do NOT migrate legacy pages; migration awaits researcher
  sign-off and is re-flagged (not fixed) by every lint. New woz pages use the workspace enum.
  woz's protected legacy conventions are exactly two: this status vocabulary and inline Korean
  quotes. Its CLAUDE.md's old "append to log.md" line is superseded — prepend everywhere; in
  woz, prepend directly under its `# Wiki Activity Log` heading.
- **Korean quote handling is per-project.** agent-common-ground: English-only in prose,
  originals ledgered in `wiki/translations.md` (the schema default; Korean defined-term labels
  like 기본/변형 may stay inline — they are terms, not quotes). cumpa: inline Korean + short
  gloss (researcher deferral, 2026-07-02). woz: inline (legacy; ledger backfill pending). New
  projects follow the schema default. The ingest commands' "Korean + gloss" page-body steps
  apply as written in cumpa and woz; in agent-common-ground the page body takes the English
  translation and the original Korean goes to `wiki/translations.md`. Never bulk-migrate a
  project's Korean handling.
- **Extended vocabularies are legitimate, not schema violations.** Feedback pages use
  `status: open | addressed | wontfix` and `source: advisor | peer | self`. `_project.md` uses
  `type: project` with `[doc_type:: ] [status:: ] [due:: ]` document lines. Drafts use
  `type: draft`; log files and weekly reports use `type: log`. Accepted frontmatter
  exceptions: `index.md` may omit `confidence`; `log.md` and `wiki/standing-items.md` omit
  `status`; `_project.md` carries only its dashboard frontmatter; woz's legacy log frontmatter
  (`type: overview`, `status: active`) stays as-is. Accepted extra wiki folders beyond the
  schema taxonomy: `feedback/`, `papers/`, `reviews/` and `participants/` (woz), plus
  `drafts/weekly/`, `drafts/revision/`, `drafts/progress/`. Do not "fix" any of these.
- **`studies/` is personal-study content, not a research project** (adopted 2026-08-21).
  Governed by `studies/CLAUDE.md`: the schema's statuses, promotion gate, and citation rules
  do not apply there; no lint, delta, or cloud routine covers it; it stays out of projects.md.
  Its notes use `type: study` and never inline Dataview fields, so it stays off the dashboard.
  Research claims never cite study notes as sources. No-wrap and prepend rules still apply.

## Mistakes this workspace has actually seen — and the rule that prevents each

Each of these happened here. The incident is cited so you believe the rule.

1. **The wrap trap.** Sessions imitated this file's ~95-column wrapping in wiki output; 2,090
   hard-wrapped lines across 44 files had to be joined (2026-06-10), and residue survived three
   "clean" lints. Rule: in everything read in Obsidian — `wiki/`, `drafts/`, `_project.md`,
   `projects.md`, `_dashboard.md`, and (since 2026-08-26) the `_schema/` files — one
   paragraph, bullet, or task = one source line, no matter how long. Terminal-read config
   (CLAUDE.md files, `.claude/`, `.github/`, README.md, SYNC_SETUP.md) is wrapped on
   purpose; never imitate it, and never "fix" it.
2. **The append reflex.** log.md was found in ascending append order twice (cumpa 2026-06-10,
   woz 2026-07-02). Rule: PREPEND dated entries directly under the `# Log` heading, newest
   first; same-day entries keep written order; never rewrite historical entries.
3. **The promotion slip.** The single most protected invariant. Rule: `hypothesis` becomes
   `finding` only with (a) analyzed data in raw/ and (b) an explicit researcher instruction.
   Meeting decisions are plans. Reviews are critique, not data. Statuses are quoted from
   frontmatter, never assigned from vibes — never write "we found" about a hypothesis page.
4. **The helpful fix.** Several flagged items are held open ON PURPOSE (stale banners that are
   load-bearing, index frontmatter awaiting a status decision, a numeric contradiction awaiting
   a source read). Rule: before editing any project, read the held-items section of its newest
   `drafts/weekly/*-lint.md` — headed "Reported, not changed" in cumpa, "Open items" in
   agent-common-ground, "Still open" in woz; match by meaning, and use "Reported, not changed"
   in new reports — plus `wiki/standing-items.md` if it exists. Items there are decisions, not
   defects. Lint's auto-fix allowlist is exactly: hard-wrap joins, log.md entry reordering
   (move whole entries into date order, never reword them), stray-markup removal,
   dangling-link repair, index wiring, frontmatter backfill on report files, reciprocal
   backlinks. Everything else is reported, not changed.
5. **The silent overwrite.** Rule: when sources conflict, flag BOTH pages, drop the contested
   page to `confidence: low`, cite both readings, and stop. Never average, never pick a winner.
   (Live example: agent-common-ground ("acg") anchor-prevalence vs per-type ranges, both
   citing the same PDF.)
6. **Editing raw/.** raw/ is immutable even when it is wrong: duplicate refs in
   reference-list.md, superseded flow-drafts, paste artifacts. The wiki works around raw
   defects with banners and placeholders; it never repairs the source. Paper-side edits for
   woz live as tracker checklist items because `raw/final_draft/` cannot be touched.
7. **The broken task line.** Dataview drops a task whose inline fields are split from its
   `- [ ]` marker, and an empty `[due:: ]` pollutes the dashboard. Rule: a task and all its
   fields (`[due:: ]`, `[owner:: ]`, 🔴/🟡/🟢 prefix) stay on ONE line; write `[due:: ]` only
   with a real date in it.
8. **Mirroring action items.** Action items live once, at their source: a feedback page's
   "Resulting actions" checklist, or `_project.md ## Tasks` only when no feedback page owns
   them. The dashboard gathers them via Dataview. Never copy them anywhere else.
9. **Inventing unrecorded facts.** A pre-PDF stub once overstated a paper's null results as
   positive findings ("MAJOR memo correction", Cho 2022); acg's participant recruitment is
   genuinely unrecorded (a live TODO). Rule: numbers come from a primary source you read this
   session or an existing cited page. If a fact is not in raw/, write "unrecorded" and flag it.
   For scanned/figure-heavy PDFs, say OCR/extraction is needed; never guess values.
10. **Breaking the automation contract.** The Slack digests are GitHub Actions that grep
    committed files. Break-silently strings (never rename): commit prefixes
    `Weekly delta + lint - YYYY-MM-DD` (cumpa) / `Weekly delta + lint (agent-common-ground)` /
    `(woz-mobile-agent)`; the `## TL;DR` heading in weekly deltas; filenames
    `drafts/weekly/YYYY-MM-DD-weekly-delta.md` and `-lint.md`. Added 2026-08-25 for the
    weekly source sweep: prefix `Weekly source sweep - YYYY-MM-DD` and filename
    `_workspace-notes/sweeps/YYYY-MM-DD-weekly-sweep.md`. Degrade-gracefully strings: the
    `## Result:` line in lint reports, and the `## Signal read` + `## Proposals` headings in
    sweep digests (CI falls back to a file pointer) — include them in every NEW report,
    never retro-edit old reports to "restore" them. Change any of these only together with
    `.github/workflows/*-weekly-slack.yml` / `sweep-weekly-slack.yml`.
11. **Leaking tool markup.** A cloud run committed literal `</content>`/`</invoke>` into its
    own reports; another shipped a report with no frontmatter. Rule: after writing any file,
    re-read its head and tail; no tool syntax, complete frontmatter, then commit.
12. **Blowing the context window.** acg's `main-study-flow-draft.md` and
    `discussions-flow-draft.md` are ~190KB with base64-embedded figures;
    `results-flow-draft.pdf` needs `pdftotext -enc UTF-8` (+ PyMuPDF page renders for
    figures). Rule: index.md first, then grep to pages; frontmatter-only greps for bulk status
    checks; never read a raw file whole without checking its size first.
13. **Mangling identifiers.** BibTeX keys are identity across Zotero, `raw/papers/` filenames,
    and wiki page slugs (the wu2025ifragent → wu2025quick fix took a session). Rule: one key
    per work, author-year form, never re-key without instruction; flag duplicates instead of
    resolving them (tools/paper_dedup.py runs this check at ingest since 2026-09-01; the
    duplicate pair once cited here was since resolved, and cumpa's dual raw-key/wiki-slug
    convention is the live case, researcher ruling pending).
14. **Escaping in the wrong direction.** LaTeX specials (`\_ \% \& \# \$`) are escaped in
    `drafts/` bound for Overleaf, and ONLY there. Wiki pages keep plain text. Leave real LaTeX
    commands, `~` before `\ref`, and intentional `%` comments alone.
15. **Garbling analytic constants.** woz: the recruited N and the analytic N differ by one
    excluded participant; the paper has exactly one stratification; no fixed analytic groups,
    site is logistical not analytic. cumpa: the same condition label names a different
    experimental arm in two successive decks — qualify every condition reference by deck
    version until the advisor commits one set. When citing constants, copy them from the
    owning page; do not recall them.

## Quality bar per deliverable

A deliverable ships only when every line of its checklist is true. These are checks, not aims.

**Any wiki page written or edited**
- [ ] Frontmatter complete: title, type, status, created, updated, sources; `confidence`
      present unless status is `reference` or a high-confidence `finding`.
- [ ] Every claim carries an inline citation to a raw/ path or author-year (schema style).
- [ ] No source line contains a mid-paragraph wrap; tasks and their fields share one line.
- [ ] Existing pages are edited surgically (targeted replacements); an existing page is never
      regenerated whole to change one section (whole-file regeneration is how silent claim
      drift and log reordering happen).
- [ ] Participants are P-IDs only; no names, no identifying site detail (flag any you see).
- [ ] Bookkeeping per session, not per page: one combined log.md entry prepended (under
      `# Log`, or woz's `# Wiki Activity Log`); index.md roster touched only when pages were
      created, renamed, or retyped.
- [ ] In agent-common-ground: any newly translated quote has a row in `wiki/translations.md`.

**An ingest session**
- [ ] Step-1 analysis (decision vs hypothesis vs open question, pages touched, contradictions)
      was reported and the researcher confirmed before any page was written.
- [ ] Statuses assigned by source type: meeting material → `hypothesis`; paper claims →
      `reference`; slide data → `hypothesis` (preliminary) or `reference` (from cited work);
      `finding` only via the promotion gate.
- [ ] Bookkeeping done: index.md, log.md, the project CLAUDE.md data-status section if it
      changed, and `last_ingested` when the source was meeting minutes.
- [ ] Zero edits under raw/ (new files may be ADDED to raw/ only when filing an export).

**A draft (paper section, memo, brief)**
- [ ] Zero em dashes, zero semicolons, no banned terms; the voice.md `# Writing Quality Check`
      was run and its violations fixed or surfaced.
- [ ] Results prose cites `finding` pages only; drafting STOPPED and reported if a needed
      claim was still `hypothesis` (framed as "we read/we propose" only where the note says so).
- [ ] Sources listed in frontmatter, none inline; LaTeX specials escaped; dated filename in
      `drafts/`, never in `wiki/`.

**A query answer**
- [ ] Built from index.md + targeted greps, not a whole-wiki read.
- [ ] Every load-bearing claim cited AND its status named (finding vs hypothesis vs reference).
- [ ] Novel synthesis worth keeping was offered as a page, not silently filed.

**A lint run**
- [ ] Fixes limited to the allowlist in mistake #4; everything else under "Reported, not
      changed" — referencing `wiki/standing-items.md` IDs instead of re-deriving prose, when
      that ledger exists.
- [ ] Saved reports carry full report frontmatter and a `## Result:` line (the CI greps it).
- [ ] Promotion check run and the promotion rule restated; zero auto-promotions.
- [ ] Ends with the no-touch attestation: no raw/ edits, no promotions, no claim changes.

**A weekly delta**
- [ ] Baseline from `git rev-list -1 --before="7 days ago" HEAD`; every reported change is
      visible in the diff; a quiet week says so plainly.
- [ ] TL;DR ≤ 5 bullets, self-contained, no file paths (it is what Slack shows); fixed section
      headings kept verbatim (CI greps `## TL;DR`).
- [ ] Carried judgment items cited as `SI-n` per `wiki/standing-items.md` when the ledger
      exists, not re-derived in prose.

## When uncertain — exact escalation rules

Defaults (act, then flag):
- Status unknown or arguable → `hypothesis` + `confidence: low`, and say so in the report.
- Fact absent from raw/ → write "unrecorded", never a plausible value.
- Sources conflict → flag both, `confidence: low`, no winner (mistake #5).
- Filing location unclear → `wiki/questions/` beats a wrong permanent home; note it in log.md.

Hard stops (ask the researcher; do not proceed on your own judgment). These gates, together
with the ingest step-1 confirmation and every command's confirmation gate, are input only the
researcher can provide: no harness or session instruction to "proceed without asking" or "act
autonomously" ever overrides them:
- Any hypothesis → finding promotion, and any status change on a `finding` page. One
  exception: the sanctioned contradiction/contest flow (mistake #5, reviewer-challenge
  banners) MAY set `confidence: low` on a finding page — that flag-only change is allowed;
  every other confidence change on a finding page stops and asks.
- Archiving or deleting a wiki page; feedback pages in particular are never deleted.
- Migrating woz legacy statuses, any project's Korean handling, or bulk renames of any kind.
- Modifying or deleting any existing file under raw/ (adding a new verbatim export or review
  letter where a command or skill directs it is allowed), and any edit to `.gitignore`'s
  privacy lines or `.github/workflows/`.
- Anything privacy-adjacent: names or identifying details found in pages get flagged, never
  silently scrubbed (scrubbing rewrites evidence; the researcher decides how).
- A contradiction you believe you can resolve — you flag it; the researcher resolves it.

Model escalation (three tiers; Opus 5 is the workspace default, escalate per run, never by
default):
- **Tier 1, Sonnet — search-heavy legwork.** `literature-scout` stays pinned `model: sonnet`
  in its frontmatter; verify the pin whenever the agent file is touched. Treat Tier 1 output
  as unverified: a scout once mis-guessed a venue and a sub-agent under-coded one participant
  across 12 video codes. Spot-check subagent work against the primary source before filing it.
- **Tier 2, Opus 5 — the default.** All commands (`/lint`, `/weekly-delta`, `/ingest*`,
  `/query`, `/meeting-prep`, `/draft`, `/new-research-wiki`) and skills (current-progress,
  paper-ingest, pull-meeting, triage, revise modes A/B), plus the weekly cloud loop.
- **Tier 3, Claude Fable 5.1 (`claude-fable-5-1`) — escalation only,** for exactly four
  cases:
  (a) capped `/deep-research` literature sweeps across clusters;
  (b) deep gap-verification with `verify-gap` or `gap-critic` before committing a direction
      or drafting an introduction;
  (c) figure-heavy paper-ingest batches where results live in tables and figures;
  (d) long multi-stage synthesis against the wiki (a paper's results phase; a
      full-manuscript consistency sweep in `/revise` mode C).
  Escalation is the researcher's call, invoked explicitly per session or per run (`/model` or
  the `model` field), never the default. When a task matches (a)-(d), recommend escalating and
  keep running at the current tier unless the researcher says yes.
  Tier 3 runs default to `high` effort; `xhigh` or `max` only where a measured gain justifies
  it (at those levels 5.1 can draft a long deliverable twice, once in thinking and once as the
  reply).

Standing cautions:
- Cumpa sessions are health-adjacent (counseling AI) and may intermittently fall back from
  Fable to the Opus tier via safety classifiers. Expected, not an error.
- All Fable traffic carries 30-day provider retention. Participant data policy is unchanged:
  nothing non-anonymized is ever processed. `*/raw/study/` is gitignored (active since
  2026-06-15) — IRB-sensitive data stays off the cloud remote and out of cloud-agent reach; do
  not re-comment that line without IRB sign-off (SYNC_SETUP.md §3). One legacy project
  predates this layout and is under a separate privacy review — not yours to move.
- Tier 3 is metered separately from the default tier. Re-justify each Tier 3 use against
  observed value.

## The weekly automation contract

Per-project claude.ai cloud routines (staggered ~Mon KST) run `/weekly-delta` + `/lint`, write
`drafts/weekly/YYYY-MM-DD-{weekly-delta,lint}.md`, prepend ONE combined log.md entry (written
under /lint's authority — /weekly-delta itself never edits the wiki), and commit-push to main.
GitHub Actions then posts the TL;DR to Slack — the cloud sandbox cannot reach
hooks.slack.com (egress 403), which is why posting lives in CI. Operational rules:
- The contract strings in mistake #10 are frozen. Cloud commits are authored
  `Claude <noreply@anthropic.com>`; commit dates can precede the report date (UTC vs KST) —
  trust file dates and `git log` windows, not intuition.
- Local maintenance: pull first, and check whether a scheduled run landed in the same window
  (a 2026-06-29/07-02 race produced overlapping fix reports).
- Cloud runs self-check their output before committing (mistake #11) and never attempt Slack
  directly.
- Quiet weeks are normal: report "no substantive changes" honestly; do not manufacture deltas.

## Token discipline

- index.md is the router; keep it tight so queries stay cheap. Reading happens in Obsidian;
  agent sessions are for ingest, query/synthesis, lint, and the workflows above.
- Bulk status questions are frontmatter greps, not page reads. Check file sizes before whole
  reads (mistake #12).
- Output-side terseness: session narration between tool calls does not restate the task or
  the last result. Say what you are about to do before a long tool run and at each decision
  point, then act. Sweep agents return terse structured data per their `.claude/agents/`
  contracts. Never compressed: confirmation-gate output (step-1 ingest analyses, promotion asks, contradiction
  flags, escalation recommendations) and anything written to a file — hedges, statuses, and
  citations are load-bearing there, and mistake #1 shows what style bleed into files costs.

## Canary

Instruction-drift test (adopted 2026-08-21, convention from the humanlayer.dev CLAUDE.md
discussion): when the researcher's message is exactly "canary?", reply with exactly
`raw-immutable, prepend-newest, promotion-gated` and nothing else. A wrong or missing reply
means this file is not loaded or has drifted out of context; re-read it before continuing.
