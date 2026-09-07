---
description: Ingest the latest dated section(s) from a master meeting-notes doc
---
Ingest meeting minutes from: $ARGUMENTS

The source is one master document of dated, nested bullet points, often in Korean (e.g. a
"May 15, 2026" heading followed by nested bullets under topic headers).

1. Find the date section(s) newer than `last_ingested` in _project.md. Process only new dates.
   If last_ingested is empty, ask me which date to start from rather than ingesting everything.
2. Analyze first, do not write yet. For each bullet, classify as one of:
   - decision (a plan the team agreed on)
   - hypothesis (a conjecture or hunch to test)
   - open question (something to investigate, e.g. "why has no one done history-based slot filling?")
   - paper reference (e.g. PUMICE) -> note it for raw/papers/ and a concept stub
   - action item (a task with an owner or a date)
   - limitation/gap (e.g. "no personalization benchmark")
   Report the classification and which existing wiki pages each touches. Preserve the Korean text
   and add a short English gloss.
3. After I confirm, write:
   - open questions and limitations -> wiki/questions/ (status hypothesis)
   - hypotheses -> the relevant theme/concept page (status hypothesis, confidence as warranted)
   - paper references -> a stub in wiki/concepts/ plus a note that the PDF should go in raw/papers/
   - action items -> `- [ ] task` in the project's tasks, prefixed 🔴/🟡/🟢 by importance
     (unmarked = normal), so the dashboard sees them. Add `[due:: YYYY-MM-DD]` only when a
     real deadline exists; never write an empty `[due:: ]`.
   Then update wiki/index.md, prepend a dated wiki/log.md entry (newest first, directly under
   the `# Log` heading), and set `last_ingested` in _project.md to the newest date processed.

Never promote anything to `finding`. These are meeting notes, so everything is `hypothesis`.
