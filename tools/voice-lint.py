#!/usr/bin/env python3
"""W1: deterministic voice-lint (adopted 2026-08-21; C3 single-source rework 2026-08-26,
decisions/2026-08.md).

Checks the MECHANICAL layer of _schema/voice.md on a commissioned document. Report-only:
prints findings with line numbers, changes nothing. Judgment items (burstiness, Rule of
Three, register fit) stay with the W2 cross-family pass (tools/voice-check.sh).

Single source: the banned vocabulary is PARSED AT RUNTIME from _schema/voice.md's Writing
Quality Check §1 ("Hard bans:" and "Context flags:" lines). There is no term list in this
file, so the list cannot drift. If the parse fails, this script exits loudly rather than
linting with a partial list (fail-closed).

Tiering (C3, corpus-measured 2026-08-26): hard bans are violations; context flags are
surfaced for judgment because legitimate uses exist (statistical "robust", the noun
"underscore"). Hits on lines containing quotation marks get a [check-quoted] note, since
quoted material is exempt per voice.md.

Scope reminder: researcher-commissioned documents only. Wiki knowledge pages and
bookkeeping are exempt; never run this to retro-rewrite existing wiki pages.
"""
import os, re, sys

VOICE_MD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_schema", "voice.md")
HYPHEN_CHAIN = re.compile(r"\b[A-Za-z]+(?:-[A-Za-z]+){2,}\b")
THROAT = re.compile(r"^(It is|There are|This )\b")
LINK_TARGET = re.compile(r"\]\([^)]*\)")          # ](path) - strip targets, keep display text
DISPLAY_SLUG = re.compile(r"\[([^\]]*-[^\]]*-[^\]]*)\]")  # [two-plus-hyphen display text]


def load_canonical_lists():
    text = open(VOICE_MD, encoding="utf-8").read()
    def parse(prefix):
        m = re.search(rf"^{prefix}:\s*(.+)$", text, re.MULTILINE)
        return [t.strip() for t in m.group(1).split(",") if t.strip()] if m else []
    hard, ctx = parse("Hard bans"), parse("Context flags")
    if len(hard) < 5 or len(ctx) < 1:
        sys.exit(f"voice-lint: FAILED to parse the canonical list from {VOICE_MD} "
                 f"(hard={len(hard)}, context={len(ctx)}). Fix the 'Hard bans:' / "
                 "'Context flags:' lines in voice.md before linting; refusing to run "
                 "with a partial list.")
    return hard, ctx


def main(path):
    hard_terms, ctx_terms = load_canonical_lists()
    lines = open(path, encoding="utf-8").read().splitlines()
    body_start = 0
    if lines and lines[0] == "---":
        for i in range(1, len(lines)):
            if lines[i] == "---":
                body_start = i + 1
                break
    cats = {"em-dash": [], "semicolon": [], "banned-term (hard)": [],
            "context-flag (judge, not a violation)": [], "throat-clearing": [],
            "hyphen-chain (prose)": [], "slug-as-display-text": []}
    en_dash = 0
    in_code = False
    prev_blank = True
    for n, line in enumerate(lines, 1):
        if n <= body_start:
            prev_blank = True
            continue
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        quoted_note = " [check-quoted]" if re.search(r'["“”]', line) else ""
        if "—" in line:
            cats["em-dash"].append((n, line.count("—")))
        en_dash += line.count("–")
        no_url = re.sub(r"https?://\S+", "", line)
        if ";" in no_url:
            cats["semicolon"].append((n, no_url.count(";")))
        low = line.lower()
        for term in hard_terms:
            if re.search(r"\b" + re.escape(term).replace(r"\ ", r"\s+") + r"\b", low):
                cats["banned-term (hard)"].append((n, term + quoted_note))
        for term in ctx_terms:
            if re.search(r"\b" + re.escape(term) + r"\w*\b", low):
                cats["context-flag (judge, not a violation)"].append((n, term + quoted_note))
        if prev_blank and THROAT.match(line.strip()):
            cats["throat-clearing"].append((n, line.strip()[:60]))
        for m in DISPLAY_SLUG.finditer(line):
            cats["slug-as-display-text"].append((n, m.group(1)))
        prose = LINK_TARGET.sub("]", line)
        prose = re.sub(r"\[\[[^\]]*\]\]", "", prose)
        for m in HYPHEN_CHAIN.finditer(prose):
            cats["hyphen-chain (prose)"].append((n, m.group(0)))
        prev_blank = (line.strip() == "")
    violations = 0
    for cat, hits in cats.items():
        if not hits:
            continue
        print(f"[{cat}] {len(hits)} hit(s):")
        for h in hits[:25]:
            print(f"  line {h[0]}: {h[1]}")
        if len(hits) > 25:
            print(f"  ... and {len(hits)-25} more")
        if not cat.startswith("context-flag"):
            violations += len(hits)
    if violations == 0:
        print("voice-lint: clean (mechanical layer).")
    print(f"\nVIOLATIONS: {violations}  (context flags are counted separately; "
          f"en-dashes, informational: {en_dash})")


if __name__ == "__main__":
    main(sys.argv[1])
