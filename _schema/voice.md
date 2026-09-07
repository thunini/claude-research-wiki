# Voice

Rules for any prose drafted for me. The /draft command reads this. Go through Writing Quality Check everytime before producing output.

Scope (researcher decision, 2026-07-10): these rules govern every researcher-commissioned document, meaning anything the researcher asks to have drafted, whether it lands in drafts/ or is filed as a wiki page (for example a revision-plan page). Routine wiki bookkeeping (log entries, index wiring, tracker upkeep, lint and weekly-delta reports) keeps the wiki's existing register and is exempt. Never retro-rewrite existing wiki pages to match this file without an explicit instruction.

## Hard rules
- No em dashes. No semicolons.
- No hyphen-chained phrases (added 2026-07-14). Never fuse a multi-word phrase into one hyphenated compound ("shift-to-vigilance", "continuous-primary", "flag-not-migrate") and never use wiki-slug names as words in prose or as link display text ("age-specificity-vs-first-use-baseline", "mental-model-components"). Write the phrase out plainly, or name the thing in plain words. Conventional two-word compound modifiers stay ("low-stakes lab", "inter-rater reliability", "mixed-effects model").
- Start sentences and paragraphs with action, not throat-clearing.
- No filler. The canonical banned-vocabulary list lives in the Writing Quality Check §1 below (single source since 2026-08-26; tools/voice-lint.py parses it from there).
- Long sentences only when necessary. Default to straightforward sentences.
- No "A is B, not C" or "It's A, not B" patterned sentences. 

## Academic register
- Direct and precise. Claim first, hedge second, and only where the evidence warrants it.
- Match the target venue when I name one (CHI, IMWUT, CSCW).
- Every empirical claim names what supports it. No unsupported assertions.

## Samples

Paste two or three short paragraphs of my own published or drafted prose below. The drafter should match their rhythm and vocabulary, not just the rules above. Update these as my writing evolves.

(Public copy: the three sample paragraphs are removed because they are manuscript text. The private file holds two to three short paragraphs of the researcher's own prose here.)

# Writing Quality Check

A self-review checklist /draft runs after producing prose, on top of voice.md. It catches the patterns that make writing read as machine-generated. These are good-writing rules, not detection evasion. Adapted from the Writing Quality Check idea in Academic Research Skills by Cheng-I Wu (github.com/Imbad0202/academic-research-skills, CC-BY-NC 4.0).

## 1. Banned and high-frequency AI terms

VOCAB LIST (single source, adopted 2026-08-26 after a corpus measurement; the two lines below are parsed by tools/voice-lint.py, so keep the "Hard bans:" and "Context flags:" prefixes and the comma-separated form).

Hard bans: delve, dive deep, in order to, it is important to note, it's worth noting, in today's world, navigate the landscape, tapestry, testament to, realm, multifaceted, crucial, pivotal, foster, moreover, furthermore, in conclusion, ledger, canonical, gazetteer, load-bearing, verdict

Context flags: robust, leverage, underscore, comprehensive

Hard bans are removed on sight; replace with the plain word or cut. Context flags have legitimate uses (statistical "robust", the noun "leverage", "underscore" as the `_` character, genuine comprehensiveness) — the measured false positives were exactly these — so they are surfaced for judgment, never auto-flagged as violations. Quoted material is exempt throughout (verbatim reviewer critique, participant quotes, cited text).

## 2. Punctuation

Em dashes: zero. Semicolons: zero. (voice.md hard rules.) Do not substitute the banned dash with a comma splice. Split the sentence instead. Hyphen chains: flag any invented compound that fuses three or more words or a prepositional phrase ("shift-to-vigilance"), and any wiki-slug name appearing as a word in prose or as link display text. Rewrite as the plain phrase. Standard two-word compound modifiers pass.

## 3. Openers

No throat-clearing. Start with the action or the claim. Flag any paragraph that opens with "It is", "There are", "This", or a wind-up clause before the point.

## 4. Structural monotony

Rule of Three: flag reflexive three-item lists ("X, Y, and Z") used for rhythm rather than because there are exactly three things. Vary the count. Uniform paragraphs: flag a run of paragraphs all the same length. Real argument has uneven paragraphs. Synonym cycling: flag swapping synonyms to avoid repeating a key term. In research writing, repeat the precise term. "Slot" stays "slot", not "parameter", then "field", then "element".

## 5. Burstiness

Check sentence-length variation. A stretch of same-length sentences reads as generated. Mix short declaratives with longer ones, but keep long sentences only where they earn it (voice.md).

## 6. Claim honesty (research-specific)

Every empirical claim names its support, or it is cut. No hedge-stacking ("may potentially suggest"). State the claim and its one honest qualifier.

## Output

Report violations by category with the offending text and a fix. Apply mechanical fixes (banned terms, dashes) directly. Surface judgment calls (Rule of Three, burstiness) for the user.