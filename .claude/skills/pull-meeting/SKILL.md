---
name: pull-meeting
description: Pull the latest meeting materials from the project's Google Drive master doc and slides into raw/, then run the ingest chain (/ingest-minutes, /ingest-slides, /ingest-feedback) with their confirmation gates intact. Use after a meeting, when asked to "pull the meeting", "fetch the minutes", "sync the meeting doc", or when raw/notes/ is behind the master doc.
---

# Pull meeting

Closes the one gap in the weekly loop that has repeatedly stalled projects: the manual export
of the master Google Doc's new dated block into `raw/notes/` (cumpa's June 12 minutes sat
un-exported for 3+ weeks; acg's RQ pages carry a non-raw "session decision" source because the
master doc was never ingested). This skill moves the export in, then hands off to the existing
ingest commands. It automates the FETCH only — every downstream judgment keeps its human gate.

The two-worlds boundary is unchanged: export coming in, draft-and-paste going out, never live
sync. This skill copies a snapshot into `raw/`; it never writes back to Drive.

## Preconditions
- Run inside a project folder. Read `_project.md` frontmatter: `drive_master`, `drive_slides`,
  `last_ingested`.
- Google Drive MCP tools available (search/read/download). If they are absent or unauthorized
  (cloud routines cannot OAuth), do NOT scrape or improvise: print the manual fallback — the
  `drive_master` URL, which dated sections to copy (those newer than `last_ingested`), and the
  exact target filename — then stop. The fallback IS a valid outcome.
- If `drive_master` is blank, ask for it; offer to record it in `_project.md`.

## Steps
1. **Fetch the master doc** via the Drive MCP (read content; download the slides file if
   `drive_slides` is set and a deck exists for the meeting date).
2. **Find the new dated sections**: those newer than `last_ingested`. If `last_ingested` is
   empty, ask which date to start from — same rule as /ingest-minutes; never default to
   "everything".
3. **File verbatim into raw/**, one file per meeting date, following the raw naming
   convention: `raw/notes/YYYY-MM-DD_meeting-notes.md` and
   `raw/notes/YYYY-MM-DD_meeting-slides.pdf`. Verbatim means verbatim: Korean untouched, no
   summarizing, no cleanup, no reformatting — provenance lives in raw/ and this file is the
   provenance. Never overwrite: if the target file exists and content differs, stop and report
   the difference; if identical, skip and note it.
4. **Report the fetch** before ingesting: which dates landed, file sizes, anything that looks
   truncated or unreadable. If the doc was unreachable or partially exported, say exactly what
   failed; never reconstruct missing content from memory or chat context.
5. **Chain the ingest commands in order** — /ingest-minutes, then /ingest-slides (if a deck
   landed), then /ingest-feedback — each with its own two-step analyze-confirm gate. Do not
   collapse or skip the gates because the fetch was automated; the gates are where accuracy
   lives. `last_ingested` is set by /ingest-minutes, not by this skill.
6. **Log the fetch itself**: prepend a dated entry to `wiki/log.md` — `## [YYYY-MM-DD]
   pull-meeting — exported <dates> block(s) from drive_master` directly under the log heading
   — so the export step has provenance too.

## Failure modes
- Drive returns a doc that lacks the expected dated heading structure → show the researcher
  what it does contain and ask where the meeting record lives; do not guess section
  boundaries.
- The deck for the date is missing → proceed with minutes only and note the gap; /ingest-slides
  and /ingest-feedback for that date wait until the deck lands.
- A deck exists for a date with no matching dated section in the master doc → file and ingest
  the deck alone via /ingest-slides, everything marked pre-advisor / `hypothesis`, and note
  that /ingest-feedback waits for the minutes (precedent: the cumpa 2026-06-10 deck,
  wiki/log.md).
- A section older than `last_ingested` changed upstream → report it as a discrepancy; raw/ is
  immutable, so never patch the already-filed export.

Tier 2 (Opus default); never needs escalation. Local/interactive workflow — cloud routines
should not attempt the OAuth fetch.
