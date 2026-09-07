---
name: triage
description: Work through the standing judgment calls the weekly lints keep re-reporting — present each held item with concrete options, record the decision in a per-project ledger (wiki/standing-items.md), and apply what was approved. Use when asked to "clear the lint backlog", "go through the open items", decide held flags, or when the same items recur across weekly reports.
---

# Triage

Kills the workspace's #1 recurring toil: lints re-derive and re-type the same held judgment
items in near-identical prose every week (newest lints hold 4 in cumpa, 6 in acg, 6 in woz,
several re-reported for a month — consecutive lint reports are ~95% identical). Each item needs a human decision that never
happens between runs, because no artifact accumulates the decision state. This skill is that
artifact plus the decision session.

Division of labor: /lint FINDS and holds; /triage DECIDES and applies. This skill never scans
the wiki for new defects — its inputs are what lint already reported.

## The ledger — `wiki/standing-items.md` (per project)
Frontmatter like log.md (title, `type: log`, created, updated — no status; the exemption is
codified in the workspace CLAUDE.md's accepted-exceptions list, so lints will not re-flag it). One section per item:

    ## SI-<n> — <short name>
    - First flagged: YYYY-MM-DD (lint or log reference)
    - Evidence: <paths, one line>
    - Why held: <the judgment call in one line>
    - Options: <2-4 concrete resolutions, including "keep holding" with a revisit condition>
    - Decision: — (verbatim researcher decision + date, once made)
    - Applied: — (what was changed, once applied)

IDs are stable and never reused. Decided items stay in the ledger (move to a `## Resolved`
tail section) — the ledger is also the record of why things are the way they are.

## Steps
1. **Collect.** The held-items section of the newest `drafts/weekly/*-lint.md` — headed
   "Reported, not changed" in cumpa, "Open items (re-reported...)" in acg, "Still open
   (judgment calls...)" plus the tracked-contradictions section in woz; match the section by
   meaning (items lint reported but did not change), not by one heading string — plus carried
   flags in recent log.md entries, and the existing ledger. Dedupe into stable SI-IDs. New
   items get the next ID; vanished items get noted, not deleted.
2. **Present, one at a time.** Each item: the one-line hold reason, the evidence paths, and
   2-4 concrete options with their consequences ("promote index.md to finding status" /
   "keep hypothesis until the thesis positions it" / ...). Interactive sessions ask per item;
   non-interactive runs (cloud) only sync the ledger and decide NOTHING.
3. **Record verbatim.** The researcher's words go in the Decision line with the date.
   "Keep holding" is a first-class outcome — record it with its revisit condition so future
   lints stop re-arguing it.
4. **Apply what was approved.** Mechanical changes are made now (status flips, banner removal,
   wording fixes), each logged. Non-mechanical follow-ups (a source must be read, data must
   land) become tasks at their source — a feedback page's Resulting actions or `_project.md ##
   Tasks` — never a mirror.
5. **Promotion candidates** are triage items like any other, but the promotion gate is
   unchanged: analyzed data + explicit instruction. When the instruction is given here, this
   skill performs the full promotion mechanics: frontmatter status flip, body bold-label
   update, index.md roster, the owning question page's status, and a log.md entry naming the
   evidence.
6. **Close.** Prepend a log.md entry (`triage — N decided, M applied, K held`), bump the
   ledger's `updated:`.

## Contract with the weekly loop
Once the ledger exists, /lint and /weekly-delta cite items as `SI-n (held, see
standing-items)` instead of re-deriving the prose — one line per item, not a paragraph. This
rule also lives in the workspace CLAUDE.md so cloud runs pick it up. If a lint finds the
ledger contradicting reality (an Applied item that regressed), that is a NEW finding, reported
normally.

Tier 2. The decision session never runs headless; a non-interactive (cloud) run may only
perform the step-1 ledger sync.
