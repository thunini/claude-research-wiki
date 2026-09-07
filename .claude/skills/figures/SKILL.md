---
name: figures
description: Make publication-quality figures for papers, revisions, and meeting decks using the house style (tools/figstyle.py). Use when asked to plot results, build or restyle a paper figure, or prepare charts for a deck. Every plotted number must trace to a data file.
---

# Figures

Discipline adapted from alphaXiv's orx-figures skill and styled on SciencePlots. The style
module is `tools/figstyle.py`; run with the system python3 (SciencePlots and matplotlib are
installed there).

## The contract

- A figure is an argument: it makes one claim, and a reader who skips the prose should
  still get that claim right. If the figure needs a paragraph to parse, redesign it.
- Provenance (workspace accuracy rule 1, extended to figures): every plotted number comes
  from a data file. `figstyle.save_fig()` REQUIRES `sources=[...]` naming the repo-relative
  data paths and writes a `.sources.txt` sidecar. Synthetic or illustrative data must be
  declared `sources=["synthetic-demo"]`, which stamps the figure; a stamped figure never
  enters a paper or a results page.
- The promotion gate reaches plots: a results figure draws only on `finding`-grade data.
  Hypothesis-grade data can be plotted for meetings and exploration, labeled preliminary
  in the caption, and never filed as a results figure.
- Build at final printed size: `figstyle.fig(width="column")` (3.34in) or `"text"` (7.0in)
  for ACM acmart, then `width=\linewidth` in LaTeX. Never build big and rescale down.
- No `ax.set_title` on paper figures: the caption is the title. Decks may use titles.
- Export via `figstyle.save_fig()`: PDF and SVG are the paper artifacts, PNG (300dpi) is
  for decks and previews. Fonts stay embedded (fonttype 42) and SVG text stays text.
- Colors come from the module's Okabe-Ito cycle (colorblind-safe, greyscale-safe). Never
  jet/rainbow, never encode meaning in color alone.
- Error bars or intervals on every aggregated point, with the N and interval type (SD, SE,
  95% CI) stated in the caption. A mean without spread is not a result.
- Korean text in figures: matplotlib needs a CJK font set explicitly (SciencePlots has CJK
  styles); English-only figures for papers per each project's language conventions.

## Workflow

1. Locate the data file in raw/ or an export in the project (never retype numbers from a
   page or from memory; mistake #9 applies to figures too).
2. `import figstyle; figstyle.use_paper_style()`, build with `figstyle.fig()`, draw.
3. Export with `save_fig(fig, stem, outdir, sources=[...])`. Paper figures land in the
   project's `drafts/figures/` (create it if absent); never in wiki/ or raw/.
4. Audit before shipping: view the PNG at 100%; check the one-claim test, label
   readability at print size, interval annotation in the planned caption, and the
   sources sidecar.
5. Log per session in the project log.md, as with any deliverable.

## Diagrams

Method, architecture, and model diagrams (the IIC model, pipeline overviews) follow the
same contract, tool-agnostically:
- One claim per figure: an overview making two arguments becomes two figures.
- Build at final printed width, text readable at 5-8pt there. A memo or deck dashboard is
  a different artifact from its paper figure: redraw at paper width, never shrink.
- Greyscale-safe redundancy: never encode a distinction in color alone; pair color with
  border style, shape, or a label. Colors come from `figstyle.PALETTE` so diagrams and
  data plots read as one visual system across the paper.
- Caption owns the title; no baked-in headings on paper versions.
- Status honesty: a diagram renders claims, so hypothesis-grade design carries a small
  status note, and the figure cites its source memo or wiki pages in a `.sources.txt`
  sidecar (via save_fig, or written by hand for non-matplotlib SVG).
- Preferred paper format is vector. matplotlib through figstyle is fine for simple
  diagrams and gives sizing, export, and provenance for free; hand-built SVG for complex
  ones, with the same palette and fonts.
- Paper diagrams are English-only per project language conventions; bilingual variants
  are deck artifacts.

## Templates (HCI-shaped starting points)

- Grouped bars + CI: condition on x, groups side by side, `yerr=`, `capsize=3`, legend
  inside the axes. The demo in the F1 decision is the reference implementation.
- Distribution comparison: box or violin per condition for Likert-scale composites (SUS,
  NASA-TLX, MDPQ-style splits); overlay jittered points when N is small enough to show.
- Paired/within-subject change: slope graph (two x positions, one line per participant,
  P-IDs never labeled on the figure) with the group mean bolded.
