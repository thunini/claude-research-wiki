# Research Wiki Schema

Shared conventions for every project wiki in this workspace. This file is imported by the workspace-root CLAUDE.md, so it loads automatically in any project session. Do not duplicate it inside individual project CLAUDE.md files.

## The contract

- `raw/` is **immutable**. You read it, you never edit it. All provenance lives here.
- `wiki/` is **LLM-owned**. The researcher reads it; you write and maintain it.
- The researcher curates sources and asks questions. You do the summarizing, cross-linking, filing, and bookkeeping.

## Accuracy rules (highest priority)

1. **Every claim in `wiki/` cites its source.** No uncited assertions. A wiki page that cannot point back to a file in `raw/` is a defect, not a page.
2. **Status is mandatory on every page and every load-bearing claim.** Use exactly one of:
   - `hypothesis` — a conjecture, hunch, or planned direction. Not yet supported by data.
   - `finding` — supported by analyzed data with a citation to the evidence.
   - `reference` — external fact from a paper or prior work, cited to author-year.
   - `archived` — superseded or from a completed project, kept for context.
3. **Meeting notes and minutes are `hypothesis` by default.** A decision made in a meeting is a plan, not a result. Never let a meeting-note idea appear later as a `finding`. Promotion from `hypothesis` to `finding` requires (a) analyzed data and (b) an explicit instruction to promote.
4. **Tag confidence when a claim is shaky.** Add `confidence: low|medium|high` to claims that are provisional, contested, or based on a single source.
5. **Refer to participants by ID only** (P1, P2, ...). Never store real names. Same for any identifying detail of sites or people.
6. **Flag contradictions, do not silently overwrite.** If a new source conflicts with an existing page, note both and mark the page `confidence: low` until resolved.

## Folder taxonomy

### raw/ (your inbox, immutable)
- `notes/` — meeting minutes, advisor notes, your own memos. Name dated: `2026-05-27-kickoff.md`.
- `study/` — protocols, transcripts, coding sheets, survey exports, anything study-side.
- `system/` — architecture notes, specs, latency logs, anything system/build-side.
- `papers/` — PDFs or clipped articles. Name author-year: `karpathy2026.pdf`.
- `assets/` — screenshots, diagrams, figures.

### wiki/ (you write and maintain)
- `index.md` — the router. Participant/data roster, RQ list, page map. Keep it current.
- `log.md` — dated activity log, **reverse-chronological: newest entry at the top**. One entry per ingest/query/lint session. **Prepend** new entries directly under the `# Log` heading; never append to the bottom. Order by date descending; keep a single day's entries in the order they were written.
- `translations.md` — translation ledger: the original Korean for every quote rendered in English anywhere in `wiki/` or `drafts/`. Maintained provenance, not a knowledge page.
- `questions/` — open questions and hypotheses, each with status and what evidence would resolve it.
- `themes/` — qualitative themes (for the study side).
- `comparisons/` — quantitative results pages (SUS, NASA-TLX, latency numbers, timing).
- `concepts/` — theory and construct pages (e.g. common ground, levels of automation).
- `system/` — architecture, pipeline, component pages (for the system side).
- `design/` — design implications derived from findings.
- `methods/` — study design and analysis-process pages.

A mixed-method-plus-system project lives in **one wiki**, with the study and system material separated by these folders rather than by separate vaults. Keep the graph in one place.

## Frontmatter (every wiki page)

```yaml
---
title: "Page title"
type: theme | concept | comparison | system | participant | paper | question | overview | log
status: hypothesis | finding | reference | archived
confidence: low | medium | high      # omit only when status is reference or finding-high
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources:                               # files in raw/ this page draws from
  - raw/notes/2026-05-27-kickoff.md
related: ["[[other-page]]"]            # wikilinks for the graph
---
```

## Citation style inside pages

- Cite the raw source inline: `(raw/notes/2026-05-27-kickoff.md)` or `(P7, study/transcripts/P7.txt)`.
- Paper claims cite author-year and page: `(Norman, 1983, p.12)`.
- Korean quotes: translate to English in the page and do **not** include the original Korean inline. Record each original Korean quote with its English translation in `wiki/translations.md` so the original stays recoverable.

## Typed relations (optional frontmatter keys)

Four optional frontmatter keys make load-bearing relations machine-readable. Each is a YAML list of wikilinks written in the project's existing `related:` style. They complement prose: the banner or sentence stays for the human reader, and the key is the layer that greps and Dataview queries can see.

- `supports:` — this page's data or argument supports the claim on the linked page (direction: evidence → claim).
- `contradicts:` — this page and the linked page conflict (accuracy rule 6). Reciprocal: both pages carry the key. Pairs with the sanctioned flag-only `confidence: low` drop.
- `supersedes:` — this page replaces the linked page's account. The key lives on the superseding page only; the superseded page keeps its banner.
- `answers:` — this page answers the linked `questions/` page (direction: evidence → question).

Rules (merged 2026-08-26, all constraints kept):
- Optional, forward-only, frontmatter only: add a key at page creation or during a content edit; never bulk-backfill (bulk edits stay researcher-gated); never as inline `[field:: ]` body syntax.
- Only `contradicts` is mirrored on both pages; inbound edges for the other three are computed by query. Typed edges never change status or confidence semantics and never weaken the promotion gate: a `supports` edge feeds a lint REPORT of promotion candidates, nothing more.
- woz-mobile-agent legacy pages (pre-2026-07) are exempt; their banner conventions are protected.

## Extraction provenance (optional frontmatter keys, paper pages)

Adopted 2026-08-21 (source-gatherer pilot). New paper pages record how their text was obtained: `source_format:` (pdf | html | scan), `text_extractor:` (tool name, or `visual-read`), `text_extracted_date:` (YYYY-MM-DD). Rationale: PDF text extractors fail silently (substituted glyphs, dropped minus signs, scrambled table order), so a page states which extractor its numbers passed through. Forward-only: written by the paper-ingest skill on new pages, never backfilled onto existing pages.

## Line-wrapping: never hard-wrap wiki output

Every `.md` you write outside `raw/` (wiki pages, drafts, `_project.md`) is read in Obsidian, which renders a single newline as a visible line break. So:

- **One paragraph = one source line. One bullet or task = one source line**, no matter how long. Let the editor soft-wrap; never insert a newline to fit a column width.
- Never split across lines: a task and its inline fields (`[due:: ]` must stay on the same line as its `- [ ]` marker or Dataview drops it from the dashboard), wikilinks, or bold/italic pairs.
- A further reason: queries grep this wiki, and a phrase split across a wrap is un-greppable.
- The CLAUDE.md files (and `.claude/`, `.github/`, README.md, SYNC_SETUP.md) **are** wrapped at ~95 columns — deliberate for terminal reading; do not imitate their wrapping. This schema file and `_schema/voice.md` are researcher-read in Obsidian and UNWRAPPED (one paragraph or bullet per source line) since 2026-08-26: never re-wrap them. Do not imitate any wrapped page you encounter; fix it instead.

## The three workflows

The binding contracts are the workspace command files (`.claude/commands/ingest.md`, `query.md`, `lint.md`); workspace CLAUDE.md rule 4 makes them authoritative, so this section is one-line orientation only (deduplicated 2026-08-26). Ingest: two-step — analyze and confirm with the researcher, then write with correct statuses, citations, and index/log bookkeeping. Query: read `index.md`, grep to pages, never load the whole wiki; offer a novel synthesis as a page. Lint: audit; fixes only per the workspace CLAUDE.md auto-fix allowlist, everything else reported. Run lint after every ~10 ingests or monthly, and before any major synthesis or writing session. Token discipline lives in the workspace CLAUDE.md (single owner since 2026-08-26).
