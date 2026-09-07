---
description: Ingest a source into this wiki (two-step, accuracy-first)
---
Ingest the source: $ARGUMENTS

Step 1 — analyze (do not write pages yet). Read the source. Report:
- Source type (meeting-note / transcript / paper / system-log / survey).
- For meeting notes: separate decisions, hypotheses, and open questions. All become status
  `hypothesis` unless backed by analyzed data.
- Which existing wiki pages this touches, and any contradictions with them.

Step 2 — write (after I confirm). Create/update pages following the schema: correct status,
inline citations to the raw source, wikilinks, participant IDs only. Then update index.md and
prepend a dated entry to log.md (newest first, directly under the `# Log` heading — never
append to the bottom). Never promote an existing hypothesis to finding without data
and my explicit say-so.
