"""House figure style for research-workspace papers (F1, adopted 2026-08-31).

Layers SciencePlots' 'science' base ('no-latex' variant, since no TeX install) with ACM
sizing, sans-serif labels, and the Okabe-Ito colorblind-safe palette. The discipline
contract lives at .claude/skills/figures/SKILL.md; decisions/2026-08.md records adoption.

Provenance rule (workspace accuracy rule 1, extended to figures): save_fig() REQUIRES a
sources list naming the raw/ or wiki/ data files every plotted number came from. Synthetic
or demo data must be declared as sources=["synthetic-demo"], which stamps the figure.
"""
import warnings

import matplotlib.pyplot as plt
import scienceplots  # noqa: F401  (registers the styles)

# ACM acmart geometry, inches (columnwidth ~241pt, textwidth ~506pt).
COLUMN = 3.34
TEXT = 7.0
GOLDEN = 0.618

# Okabe-Ito, colorblind-safe and greyscale-distinguishable.
PALETTE = ["#0072B2", "#E69F00", "#009E73", "#D55E00",
           "#CC79A7", "#56B4E9", "#F0E442", "#000000"]


def use_paper_style():
    """Apply the house style. Call once, before creating figures."""
    plt.style.use(["science", "no-latex"])
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
        "font.size": 8,
        "axes.labelsize": 8,
        "axes.titlesize": 8,      # titles are banned on paper figures; kept sane for decks
        "xtick.labelsize": 7,
        "ytick.labelsize": 7,
        "legend.fontsize": 7,
        "axes.prop_cycle": plt.cycler(color=PALETTE),
        "figure.dpi": 150,
        "savefig.dpi": 300,
        "svg.fonttype": "none",   # keep text as text in SVG
        "pdf.fonttype": 42,       # embed TrueType in PDF (editable, ACM-safe)
    })


def fig(width="column", aspect=GOLDEN):
    """New figure at final printed size: width 'column' (3.34in), 'text' (7.0in), or inches."""
    named = {"column": COLUMN, "text": TEXT}
    w = named[width] if width in named else float(width)
    return plt.figure(figsize=(w, w * aspect))


def save_fig(figure, stem, outdir, sources):
    """Export PDF + SVG (vector, for the paper) and PNG (300dpi, for decks/preview).

    sources: list of repo-relative data paths every plotted number came from, or
    ["synthetic-demo"] for demo data (stamped on the PNG and named in the sidecar).
    Writes <stem>.sources.txt next to the figures so provenance survives the export.
    """
    if not sources:
        raise ValueError("save_fig requires sources: name the data files, "
                         "or pass ['synthetic-demo'] for demo data.")
    synthetic = sources == ["synthetic-demo"]
    if synthetic:
        warnings.warn("figure marked synthetic-demo; never file it as a results figure")
        figure.text(0.99, 0.01, "synthetic demo data", ha="right", va="bottom",
                    fontsize=6, color="#888888", style="italic")
    import os
    os.makedirs(outdir, exist_ok=True)
    meta = "sources: " + "; ".join(sources)
    for ext in ("pdf", "svg", "png"):
        figure.savefig(os.path.join(outdir, f"{stem}.{ext}"), bbox_inches="tight",
                       metadata={"Subject": meta} if ext == "pdf" else None)
    with open(os.path.join(outdir, f"{stem}.sources.txt"), "w", encoding="utf-8") as f:
        f.write(meta + "\n")
    return [os.path.join(outdir, f"{stem}.{e}") for e in ("pdf", "svg", "png")]
