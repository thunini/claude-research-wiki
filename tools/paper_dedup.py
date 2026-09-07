#!/usr/bin/env python3
"""P5: BibTeX-key dedup check before a key is trusted (adopted 2026-09-01,
decisions/2026-09.md). Called by the paper-ingest workflow with the CANDIDATE paper's
key, title, and DOI; checks against every key already known to the project (raw/papers
PDFs, wiki paper pages, reference lists). Mistake #13 is the standing case: one key per
work, and duplicates are flagged, never silently resolved.

Usage: python3 tools/paper_dedup.py <project> --key K [--title "T"] [--doi D]
Report-only; exit code 0 always. Resolution: with --doi or --title the candidate is checked
against Crossref (then OpenAlex) keylessly, verifying the payload shape, so a DOI is confirmed
to exist and a title can find its DOI before a key is minted. Never re-keys anything. cumpa's dual raw-key/wiki-slug convention is a known
class (researcher ruling pending, 2026-09-01) and is reported as INFO, never as a clash.
"""
import argparse
import difflib
import json
import os
import re
import subprocess
import urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOI_RE = re.compile(r"\b10\.\d{4,9}/[^\s\"']+")


def norm_doi(d):
    d = d.rstrip(".,;]")
    # trailing ) belongs to surrounding prose only when unbalanced (DOIs like
    # 10.1016/S0010-0277(02)00017-3 legitimately contain parens)
    while d.endswith(")") and d.count(")") > d.count("("):
        d = d[:-1]
    return d.lower()


UA = "research-workspace-paper-dedup (curl)"


def _get(url):
    try:
        out = subprocess.run(["curl", "-sS", "--max-time", "20", "-A", UA, url],
                             capture_output=True, text=True, check=True)
        return json.loads(out.stdout)
    except Exception as e:  # network, non-JSON, HTTP error bodies
        return {"_error": f"{type(e).__name__}: {str(e)[:80]}"}


def resolve(doi="", title=""):
    """Keyless resolution against Crossref, then OpenAlex. Returns a list of report lines.
    Verifies the SHAPE of each payload, never just that a body came back."""
    lines = []
    if doi:
        d = norm_doi(doi)
        cr = _get(f"https://api.crossref.org/works/{urllib.parse.quote(d, safe='')}")
        msg = cr.get("message") if isinstance(cr, dict) else None
        if isinstance(msg, dict) and msg.get("title"):
            t = msg["title"][0]
            yr = (msg.get("issued", {}).get("date-parts") or [[None]])[0][0]
            auth = ", ".join(f"{a.get('family','')}" for a in msg.get("author", [])[:3])
            lines.append(f"RESOLVED (Crossref): {t} | {auth} | {yr} | {msg.get('container-title', [''])[0]}")
            if title and difflib.SequenceMatcher(None, title.lower(), t.lower()).ratio() < 0.6:
                lines.append(f"  WARNING: candidate title does not match the DOI's registered title (ratio < 0.6); check the DOI.")
        else:
            oa = _get(f"https://api.openalex.org/works/doi:{urllib.parse.quote(d, safe='')}")
            if isinstance(oa, dict) and oa.get("title"):
                lines.append(f"RESOLVED (OpenAlex): {oa['title']} | {oa.get('publication_year')} | {(oa.get('primary_location') or {}).get('source', {}) and (oa['primary_location']['source'] or {}).get('display_name','')}")
            else:
                lines.append(f"UNRESOLVED: DOI {d} not found at Crossref or OpenAlex (Crossref: {cr.get('_error') or cr.get('status', 'no title in payload')}). Treat the DOI as unverified.")
    elif title:
        cr = _get("https://api.crossref.org/works?rows=3&query.bibliographic=" + urllib.parse.quote(title))
        items = ((cr.get("message") or {}).get("items") or []) if isinstance(cr, dict) else []
        good = [i for i in items if i.get("title") and i.get("DOI")]
        if good:
            lines.append("Crossref candidates for the title (confirm one before minting a key):")
            for i in good:
                t = i["title"][0]; r = difflib.SequenceMatcher(None, title.lower(), t.lower()).ratio()
                yr = (i.get("issued", {}).get("date-parts") or [[None]])[0][0]
                lines.append(f"  ~{r:.2f} | {t[:80]} | {yr} | doi:{i['DOI']}")
        else:
            lines.append(f"Crossref title lookup returned no usable items ({cr.get('_error') or 'empty or malformed payload'}); resolve the DOI by hand before keying.")
    return lines


def known_keys(proj):
    seen = {}
    rp = os.path.join(ROOT, proj, "raw", "papers")
    if os.path.isdir(rp):
        for fn in os.listdir(rp):
            if fn.endswith(".pdf"):
                seen.setdefault(fn[:-4], set()).add("raw/papers")
            if fn in ("reference-list.md", "references.bib"):
                txt = open(os.path.join(rp, fn), encoding="utf-8", errors="replace").read()
                for k in re.findall(r"@\w+\{([^,\s]+),", txt) + re.findall(r"\b([a-z][a-z-]*\d{4}[a-z][a-z]+)\b", txt):
                    seen.setdefault(k, set()).add(fn)
    wp = os.path.join(ROOT, proj, "wiki", "papers")
    titles, dois = {}, {}
    if os.path.isdir(wp):
        for fn in os.listdir(wp):
            if not fn.endswith(".md"):
                continue
            key = fn[:-3]
            seen.setdefault(key, set()).add("wiki/papers")
            txt = open(os.path.join(wp, fn), encoding="utf-8", errors="replace").read()
            m = re.search(r'^title:\s*"?(.+?)"?\s*$', txt, re.M)
            if m:
                titles[key] = m.group(1).lower()
            for d in DOI_RE.findall(txt):
                dois.setdefault(norm_doi(d), set()).add(key)
    return seen, titles, dois


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--key", required=True)
    ap.add_argument("--title", default="")
    ap.add_argument("--doi", default="")
    ap.add_argument("--no-resolve", action="store_true", help="skip Crossref/OpenAlex lookups (offline)")
    a = ap.parse_args()
    seen, titles, dois = known_keys(a.project)
    findings = []
    if a.key in seen:
        findings.append(f"EXACT: key '{a.key}' already exists in {sorted(seen[a.key])} - same work? Use the existing key; never mint a second.")
    stem = re.match(r"^([a-z-]+\d{4})", a.key)
    if stem:
        mates = [k for k in seen if k != a.key and k.startswith(stem.group(1))]
        if mates:
            findings.append(f"STEM: same author+year as existing {mates} - verify these are different works before trusting the new key.")
    if a.doi:
        d = norm_doi(a.doi)
        if d in dois:
            findings.append(f"DOI CLASH: {d} already cited under key(s) {sorted(dois[d])} - this IS the same work; use that key.")
    if a.title:
        t = a.title.lower()
        for k, kt in titles.items():
            r = difflib.SequenceMatcher(None, t, kt).ratio()
            if r > 0.85 and k != a.key:
                findings.append(f"TITLE ~{r:.2f}: near-duplicate of '{k}' ({kt[:60]}) - verify before minting a new key.")
    if not a.no_resolve and (a.doi or a.title):
        findings.extend(resolve(a.doi, a.title))
    if findings:
        print(f"paper-dedup [{a.project}] candidate '{a.key}':")
        for f_ in findings:
            print(f"  {f_}")
        print("  Rule (mistake #13): flag, never silently resolve; renames are researcher-gated.")
    else:
        print(f"paper-dedup [{a.project}] candidate '{a.key}': clean ({len(seen)} known keys checked).")


if __name__ == "__main__":
    main()
