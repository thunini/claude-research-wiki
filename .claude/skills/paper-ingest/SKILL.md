---
name: paper-ingest
description: Ingest an academic paper PDF into the project wiki as a reference-status page. Use when adding a related paper to the wiki, building related work, or recording what a cited paper contributes (e.g. a PDF in raw/papers/ or one the user points to).
---

# Paper ingest

Specializes the ingest workflow for academic papers. Read the PDF, then file it. This skill
composes with the PDF-reading capability for extraction; it adds the paper-specific logic.

## Read
- Read the PDF directly. For two-column ACM or IEEE layouts, follow column reading order and do
  not interleave the columns.
- Give the results tables and figures real attention, since a paper's findings often live there
  rather than in the prose.
- If the PDF is scanned (image-only), say so and note that OCR is needed before any claim can be
  trusted. Do not invent numbers from an unreadable scan.
- When a claim comes from extracted text rather than a visual read (pdftotext or similar),
  treat digits and signs as suspect: extractors silently substitute glyphs, drop minus signs,
  and scramble figure and table reading order. Re-check every load-bearing number against the
  rendered page image before citing it (failure catalog: joonan30 LLM-wiki gist, rev. 2026-08).
- For tables and figures, render the page with PyMuPDF and crop the region at two to three
  times zoom before reading numbers. A whole-page render at screen resolution is where digits
  get misread, and a low-effort read works from an overall impression instead of the crop.

## Metadata and filing
- Zotero first: with Zotero running (local API enabled), query
  `ZOTERO_LOCAL=true zotero-cli search "<author year or title>"`, then on a hit
  `zotero-cli get metadata <ITEM_KEY>` for the metadata skeleton (title, authors, year,
  venue, DOI) and `zotero-cli annotations list --item-key <ITEM_KEY>` for the researcher's
  PDF highlights, which mark passages to read first. Zotero is the key oracle and the
  skeleton, NOT the verification: check authors, year, and venue against the PDF itself
  (the 2026-08-21 trial caught a Zotero record missing its second author).
- If the item is not in Zotero (library backfill pending as of 2026-08-21) or Zotero is not
  running: proceed manually and write the breadcrumb "not in Zotero" in the page body next
  to the full citation, so the gap stays greppable.
- Extract title, authors, year, venue, DOI (Zotero skeleton plus PDF check, or PDF alone on
  the manual path).
- Match the Zotero Better BibTeX key (for example `li2017pumice`) and name the PDF in
  `raw/papers/` with that same key, so Zotero, `raw/papers/`, and the wiki share one identifier.
- Dedup before trusting a key: run
  `python3 tools/paper_dedup.py <project> --key K --title "T" [--doi D]`. An EXACT or
  DOI-clash finding means the work already has a key: use it. STEM and TITLE flags get
  verified against the sources before minting a new key. Flag, never silently resolve
  (mistake #13); renames are researcher-gated. cumpa's dual raw-key/wiki-slug convention
  is a known class pending the researcher's ruling (2026-09-01).
- If the PDF is not yet in `raw/papers/`, note that it should be added there.
- Read-only toward Zotero: this skill never adds, edits, or tags items in the library.
  Backfilling missing papers (`zotero-cli add doi ...`) is the researcher's own action.

## Write the page
Create a page in `wiki/concepts/` (or `wiki/papers/` if the project keeps one) with status
**`reference`**. A paper's claims are external facts, so they are `reference`, never `finding`.
Reserve `finding` for the project's own analyzed data. Structure the page:
- One-line contribution.
- Method, in two or three sentences.
- Key findings, each cited with a page number, e.g. `(Author, 2017, p.4)`.
  Illustrative shape of one key-findings bullet (fictional paper, form only): the paper's
  sentences are restated in this page's words, one short phrase is marked as a quotation,
  and every number carries its page:
  `- Older participants completed the voice task more slowly than the text task (median 41 s
  vs 27 s), and the authors attribute the gap to "turn-taking uncertainty" (Doe, 2019, p.6).`
  Correct because each claim is reworded, the single quoted phrase is marked and page-cited,
  and nothing is copied at sentence length. Unmarked source sentences on a reference page
  flow into drafts through /draft, which is a plagiarism risk at submission.
- Constructs or techniques it introduces that this project might reuse.
- Relation to this project's RQ: what it supports, contradicts, or leaves open. Link to the
  relevant `wiki/questions/` page.

Extraction provenance: every NEW paper page carries the three keys defined in the schema's
"Extraction provenance" section (`source_format`, `text_extractor`, `text_extracted_date`;
the schema is the single owner since 2026-08-26). Forward-only: never backfill existing pages.

Add wikilinks to related concept pages, update `wiki/index.md`, and prepend a dated entry to
`wiki/log.md` (newest first, directly under the `# Log` heading).

## Do not
- Do not paste long quotations. Paraphrase, and keep any quote short and page-cited.
- Do not let a paper's claim become a project `finding`.
