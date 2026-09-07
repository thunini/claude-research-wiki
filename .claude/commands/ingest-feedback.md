---
description: Capture advisor/peer feedback from a meeting, bound to the slides it addressed, tracked to resolution
---
Capture feedback from the meeting: $ARGUMENTS  (a meeting date whose deck and notes are ingested)

Feedback is high-value and directional, so it gets first-class treatment, not a generic bullet.
Run this after that date's deck (/ingest-slides) and notes (/ingest-minutes) are in.

1. Read that meeting's deck and notes. Find every feedback item: a critique, suggestion,
   redirection, or pointed question from the advisor or a peer, not a decision the team made.
2. Bind each item to what it addressed: the specific slide, figure, claim, or RQ. If it
   references a slide, link the saved asset (raw/assets/<date>-*.png) and the wiki page that
   slide maps to. The binding is the point. A critique without its slide loses half its meaning.
3. Write each as an entry in wiki/feedback/ with frontmatter:
   type: feedback
   status: open            # open | addressed | wontfix
   source: advisor         # advisor | peer | self
   meeting: <date>
   target: "[[slide or claim or page it addressed]]"
   related: ["[[questions/...]]"]
   Body: the critique (Korean + gloss), what was on the slide, and
   `- [ ] resulting action`, prefixed 🔴/🟡/🟢 by importance (unmarked = normal). Add
   `[due:: YYYY-MM-DD]` only when a real deadline exists; never write an empty `[due:: ]`.
   Leave a Resolution line blank.
4. Link each entry from its target page and the relevant questions page. Prepend a dated entry
   to wiki/log.md (newest first, directly under the `# Log` heading).
   If feedback opens a new direction, create a questions/ entry for it, status hypothesis.
5. Do not copy TODOs into _dashboard.md. The dashboard gathers tasks by Dataview; the
   priority marker at the source controls the high-to-low ordering there.

Later, when you address an item, flip status to addressed and fill Resolution with a link to what changed. Never delete feedback. Closed feedback is the record of how the direction evolved.
