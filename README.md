# Claude Research Wiki

The configuration layer of a research workspace that Claude Code maintains: the instruction
files, slash commands, skills, subagents, lint and provenance tools, and CI workflows that
run five research wikis for one PhD student. The wikis themselves are private because they
hold unpublished research, study records, and review correspondence. This repository is the
harness, published so other researchers can read how it works and adapt it.

Snapshot: 2026-09-07. A handful of identifying details were generalized for the public copy.
The list is in "What was changed for the public copy" below. Everything else is the file as
it runs.

## What it is

One Obsidian vault, synced by git, holding one independent wiki per research project. Each
project has the same shape: `raw/` for immutable sources (meeting notes, transcripts, papers),
`wiki/` for agent-written synthesis, and `drafts/` for output. Claude Code writes and maintains
the wiki. The researcher curates sources, asks questions, and owns every decision that turns a
hunch into a claim.

At snapshot time: 5 project wikis, 201 wiki pages carrying a status, 159 commits since
2026-06-02, 10 slash commands, 8 skills, 2 subagents, 8 tools, 6 GitHub Actions workflows,
and weekly scheduled Claude runs per project.

Three rules drive every design choice.

**The wiki is the source, the chat is not.** Sources live in `raw/`, synthesis lives in
`wiki/`, and output is generated from `wiki/`, never re-derived from chat memory.

**Status protects accuracy.** Every page and every substantive claim carries one of `hypothesis`,
`finding`, `reference`, or `archived`. Meeting notes enter as `hypothesis` and become
`finding` only with analyzed data and an explicit instruction from the researcher. The agent
can never promote on its own. This single rule stops a meeting hunch from quietly becoming a
stated result months later.

**Two worlds, one boundary.** Google Drive stays the collaborative surface for meeting docs,
slides, IRB, and grants. The markdown wiki is the personal synthesis layer on git. They connect
by exports coming in and drafts pasted out, never by live sync.

## How Claude is used here

- **The instruction file is a log of recorded failures.** `CLAUDE.md` lists fifteen
  numbered mistakes that actually happened in this workspace, each dated and each paired with
  the rule that prevents it. Rules enter the file after an incident, and the incident is cited
  so the model believes the rule.
- **A human-only promotion gate.** `hypothesis` becomes `finding` only with analyzed data in
  `raw/` and an explicit researcher instruction. Every lint run ends with an attestation of
  zero promotions and re-checks it mechanically with a git diff over status lines.
- **`raw/` is immutable even when it is wrong.** The wiki works around source defects with
  banners. Corrections to a source go back to the person who owns the file.
- **Adversarial verification before filing.** Coding instruments and claim-bearing memos go to
  separate critic sessions told to refute them against the source, with the acceptance
  criterion written down before the run, because a critic told to refute never stops on its
  own. Corrections land as dated notes, never silent rewrites.
- **Cheap search, expensive verification.** A Sonnet-pinned literature scout does the legwork
  and its output is treated as unverified. A separate pass re-checks venues, author lists, and
  quotes against the paper before anything is filed. The gap critic runs on Opus and is
  forbidden to decide.
- **Participant data fenced by infrastructure, not instruction.** Identifiable study data is
  gitignored so it never reaches the remote or a cloud agent's sandbox. Privacy findings are
  flagged with exact locations and never scrubbed by the agent, because scrubbing rewrites
  evidence.
- **Corrections leave a scar.** Wrong wording stays visible under a dated correction marker so
  a reader can audit how a claim changed.

## Layout of this repository

```
claude-research-wiki/
├── CLAUDE.md                        # the operating manual Claude loads in every session
├── _schema/
│   ├── research-wiki-schema.md      # folder taxonomy, statuses, citation style, typed relations
│   └── voice.md                     # writing-voice anchor and the Writing Quality Check
├── .claude/
│   ├── commands/                    # 10 slash commands (ingest, query, draft, lint, ...)
│   ├── skills/                      # 8 skills (paper-ingest, verify-gap, revise, figures, ...)
│   └── agents/                      # 2 subagents (literature-scout, gap-critic)
├── tools/                           # deterministic checks the skills call
├── .github/workflows/               # Slack digests, model-registry diff, reminder
├── _workspace-notes/
│   ├── collaboration-style.md       # how decisions and verification run with the agent
│   └── chat-register.md             # phrasing rules for agent chat output
├── decisions/_template.md           # the decision-ledger entry template
├── _dashboard.md                    # Obsidian Dataview views over every project
├── SYNC_SETUP.md                    # git sync across machines, IRB data caution, Zotero
└── .gitignore                       # the privacy exclusion for */raw/study/
```

## Layout of a project (in the private vault)

```
<project>/
├── _project.md        # dashboard metadata: stage, venue, deadline, documents in flight
├── CLAUDE.md          # project-specific context: RQ, prior-work links, data status
├── drafts/            # output from /draft and /meeting-prep, never in wiki/
├── raw/               # IMMUTABLE sources. The researcher adds, the agent never edits.
│   ├── notes/         # meeting minutes and memos, dated filenames
│   ├── study/         # protocols, transcripts, exports (gitignored)
│   ├── system/        # architecture notes, latency logs
│   ├── papers/        # PDFs named by BibTeX key
│   └── assets/        # figures, screenshots
└── wiki/              # agent-owned synthesis
    ├── index.md       # the router, kept tight
    ├── log.md         # dated activity log, newest first
    ├── questions/  concepts/  methods/  comparisons/  design/  system/  themes/
    └── translations.md
```

## Commands, skills, and subagents

All agent tooling is project-local under `.claude/` and versioned with the vault. Model routing
is governed by `CLAUDE.md`.

| Command | What it does |
|---|---|
| `/new-research-wiki` | Scaffold a new project wiki from the schema. |
| `/ingest` | Ingest one source in two steps: analyze and report, then write after the researcher confirms. |
| `/ingest-minutes` | Ingest only the dated sections of a meeting-notes doc newer than the last ingest. |
| `/ingest-slides` | Ingest a slide deck, adding only what the minutes lack. |
| `/ingest-feedback` | Capture advisor or peer feedback bound to the slides it addressed, tracked to resolution. |
| `/query` | Answer from the wiki with citations, naming the status of every claim relied on. |
| `/draft` | Produce voice-matched prose from `finding` pages. Stops if a needed claim is still `hypothesis`. |
| `/meeting-prep` | Draft a slide-ready brief of changes, open questions, and action-item status. |
| `/weekly-delta` | Summarize the week's changes, grounded in git, not memory. |
| `/lint` | Audit. Fix only from a short mechanical allowlist and report everything else. |

| Skill | What it does |
|---|---|
| `paper-ingest` | Read the PDF itself, record the extractor, crop tables at zoom, file as `reference`. |
| `verify-gap` | Stress-test a research gap. A gap is never verified by asserting that no one did X. |
| `current-progress` | Snapshot of what is established, open, blocked, and due at a point in time. |
| `pull-meeting` | Fetch new meeting material verbatim into `raw/`, then chain the ingest commands with their gates intact. |
| `revise` | Operate a peer-review round: demand tracker, evidence map, response drafts, consistency sweeps. |
| `triage` | Decide the judgment calls lint keeps re-reporting. Record the researcher's words verbatim. |
| `figures` | House-style figures. The save function refuses to run without named data sources. |
| `source-sweep` | Weekly scan of how others build agentic research setups. Proposes, never adopts. |

| Subagent | What it does |
|---|---|
| `literature-scout` | Finds and ranks related work. Reads and reports only, pinned to Sonnet, output treated as unverified. |
| `gap-critic` | Attacks a research direction the way a hostile reviewer would. It critiques. The researcher decides. |

## Tools

| Tool | What it does |
|---|---|
| `wiki_lint.py` + `wiki-lint-conventions.toml` | Deterministic structural pass: frontmatter, statuses, links, task fields, log order. Report-only. |
| `paper_dedup.py` | Exact, DOI, stem, and title-similarity checks before a BibTeX key is trusted. Flags, never resolves. |
| `voice-lint.py` | Mechanical voice check parsed from `_schema/voice.md`. Fails closed on a bad parse. |
| `voice-check.sh` | One call to a non-Anthropic model as a cross-family editorial pass. Refuses documents with participant IDs. |
| `figstyle.py` | House figure style on SciencePlots. `save_fig` requires `sources=` and writes a provenance sidecar. |
| `progress_gather.py` | Reads the dashboard's frontmatter fields so the progress snapshot never counts by hand. |
| `registry_diff.py` | Deterministic diff of a public model registry, run in CI where egress is open. |

## Automation

Per-project scheduled Claude runs fire weekly, run `/weekly-delta` and `/lint`, write two
report files, prepend one log entry, and commit. GitHub Actions then post the digest to Slack,
because the cloud sandbox cannot reach Slack. A separate weekly Action runs the model-registry
diff. Contract strings the Actions grep for are frozen and listed in `CLAUDE.md`.

## Model routing

Three tiers, escalated per run and never by default. Sonnet does search-heavy legwork whose
output is treated as unverified. Opus is the default for every command, skill, and the weekly
runs. Fable is reserved for four named cases (capped literature sweeps, deep gap verification,
figure-heavy paper ingests, long multi-stage synthesis), invoked explicitly by the researcher.

## What is not here, and why

The wiki pages, raw sources, drafts, decision ledgers, and per-project `CLAUDE.md` files stay
private. They hold unpublished research directions, participant transcripts, peer-review
letters, and collaborator details.

### What was changed for the public copy

- `CLAUDE.md`: participant IDs and exact analytic constants in two incident descriptions were
  generalized (mistake #15 and the Tier 1 caution). A conference name in the Tier 3 list and a
  note about the researcher's billing plan were generalized. A pointer to one project's
  tracked transcripts was reduced to "under a separate privacy review".
- `.claude/skills/revise/SKILL.md`: the venue name and file paths of the one review round it
  was built from were generalized, and one participant ID was removed.
- `_workspace-notes/collaboration-style.md`: a reviewer count naming the venue was
  generalized.
- `_schema/voice.md`: the three prose samples were removed because they are manuscript text.
  The section header and instructions stay so the mechanism is visible.

Nothing else was edited. Dates, counts, and incident descriptions are as recorded in the
private workspace.

## Adapting it

1. Clone into a normal local path, open the folder as an Obsidian vault, install Dataview.
2. In Claude Code inside the folder, run `/new-research-wiki` for each project.
3. Rewrite the mistakes section of `CLAUDE.md` as your own incidents accumulate. The fifteen
   here are this workspace's, and rules without a recorded failure behind them tend to be
   ignored.
4. Edit `tools/wiki-lint-conventions.toml` for your project names and legacy exceptions.
5. Keep `*/raw/study/` gitignored unless your IRB has approved cloud storage.

## Provenance

Built with Claude Code between June and September 2026. Interactive-session commits are
authored by the researcher with Claude as co-author. The scheduled cloud routine commits under
its own name. This public copy was produced from the private workspace on 2026-09-07.

Released under the MIT License. See LICENSE.
