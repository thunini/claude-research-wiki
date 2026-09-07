---
name: verify-gap
description: Stress-test whether a research direction has a clear, defensible research gap and strong motivation. Use when checking if an RQ is novel, whether prior work already covers it, or before committing to a direction or writing a related-work or introduction section.
---

# Verify gap

Tests whether a research direction has a defensible gap, the way a skeptical reviewer would. The
deliverable is a gap memo in `drafts/`, status `hypothesis`. The gap stays unverified until the
literature that could kill it has been searched for and not found; a gap is never verified by
asserting that no one did X.

## What the memo must establish
- The gap as one explicit, testable sentence ("No prior work does X for Y under condition Z"),
  stated against the direction's current framing. A vague gap cannot be tested.
- For every nearby `reference` page and every kill-risk paper, the delta: exactly how this
  direction differs. Where no delta can be named, the memo says the gap is weak there.
- The danger zone: prior work that may already cover the gap, argued the way the strongest
  reviewer would argue it. Objections are surfaced, never explained away.
- The gap type, because reviewers attack each differently: unstudied, studied-but-limited,
  untransferred, or evaluation gap.
- The holes: adjacent areas not yet in the wiki that could hold a killing paper, each with a
  search query at established-topic breadth. Kill-risk queries go to the `literature-scout`;
  ingest of approved hits happens in the main session after the researcher approves them, and
  the delta map is then redone against the new pages.
- The motivation: who is affected, how large the problem is, what breaks without a solution,
  with the evidence under each claim and every unsupported claim marked.
- The three or four strongest reviewer objections and whether the wiki currently answers each.
  Unanswered objections are the to-do list.
- What still must be checked before the gap can be called verified.
- The search boundary: the databases and tools queried, the query strings, and the screening
  limits (date range, language, venue class), so the absence claims below it are reproducible.

## Constraints
- Grounding: the wiki's `reference`-status pages and the direction's `questions/` pages are the
  base; web search extends it. Every cited work is verified to exist; anything unverified is
  marked `unverified`.
- Absence claims: never "no prior work does X." Write "not located within the documented search
  boundary," and the memo's search-boundary section is what makes that sentence honest. A
  quick search that found nothing is not evidence of novelty.
- Privacy: the researcher's unpublished gap sentence never enters an external search box
  verbatim; decompose it into established-topic component queries. alphaXiv, when connected,
  is discovery only (numbers come from the PDF) and its library tools stay unused. alphaXiv
  provenance rule (a vetting run once surfaced an unverifiable result): a result
  whose ID is not arXiv-form numeric (YYMM.NNNNN) is unverified until found on arXiv or a
  publisher page; never cite or ingest on the alphaXiv record alone.
- The memo never edits `wiki/`. It is critique; the researcher decides.

## Output
`drafts/<date>-gap-<topic>.md`, status `hypothesis`, one paragraph or bullet per source line.
