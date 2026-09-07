---
title: "Chat Register: Phrasing Rules for Agent-Session Chat Output"
type: reference
status: reference
created: 2026-08-12
updated: 2026-08-27 (R6 broadened to all grammatical forms of the "A, not B" contrast, with researcher examples. 2026-08-23: R6 adopted: no contrastive "A, not B" appositions in chat. Prior updates: 2026-08-20 rule 9 provisional note struck, voice.md section moved above personalization for numeric order; 2026-08-13 personalization R1–R5 adopted: linked splits, one idea per sentence in discussion, verdict first, paragraphs for reasoning, established Korean terms stand alone)
---

# Chat Register: Phrasing Rules for Agent-Session Chat Output

Adopted 2026-08-12 (researcher decision: adopt the hybrid subset, file it here). This file governs the phrasing of chat output in agent sessions, meaning the conversation itself, not any file. It draws a working subset from two standards: the writing mechanics of ASD-STE100 Issue 8 and the register conventions of the Google Developer Documentation Style Guide. It has the same standing as `collaboration-style.md`: it guides phrasing only and never overrides the workspace CLAUDE.md, the schema, project CLAUDE.md files, or command contracts. Files keep their own rules: wiki pages follow the schema, commissioned documents follow `_schema/voice.md`, bookkeeping keeps its register.

## Scope

- The register applies to substantive chat turns: answers, discussion, status summaries, option menus, and the phrasing of confirmation-gate output (content carve-out below).
- It does not apply to narration fragments between tool calls. The terseness rule (2026-07-30) governs those and stays unchanged.
- It does not apply to anything written to a file.

## Rules

From the Google guide:

1. Address the researcher as "you". Write in active voice and present tense where the meaning allows.
2. Write "can" for ability, "might" for possibility, "must" for requirement. Do not write "may".
3. Do not write: simply, just (as a minimizer), easily, "please note", utilize, or leverage as a verb. The banned list in the `_schema/voice.md` Writing Quality Check also applies to chat.
4. Put one action in each numbered step. Put each runnable shell command in its own bash block. Write descriptive link text and link file paths.

From ASD-STE100:

5. Write one instruction per sentence in instructions and numbered steps. In discussion, the unit is one idea, and one idea can hold a cause and its effect in the same sentence, up to about 30 words (amended 2026-08-13, R2).
6. Keep instruction sentences near 20 words and discussion sentences near 30. Split a long sentence instead of subordinating. This is a target, not a cap.
7. Keep noun clusters to three nouns or fewer. Unpack a longer cluster with prepositions.
8. Use one term per concept per session. Do not cycle synonyms. Reuse the term the wiki page or the researcher used.

From `_schema/voice.md`, extended to chat:

9. No em dashes and no semicolons in chat. Do not substitute a comma splice. Split the sentence.

Personalization (adopted 2026-08-13, researcher decision, all five):

10. Linked splits (R1). When a sentence splits, the follow-on sentence keeps the logical connector. "Because", "so", "but", "for example", and "which means" are allowed sentence openers. A split that silences the logic between its pieces is a violation.
11. Verdict first (R3). The first sentence of a substantive turn answers the question or states the outcome. Reasons follow.
12. Paragraphs for reasoning, bullets for enumerables (R4). Discussion runs in short connected paragraphs of two to four sentences. Bullets and tables serve only genuinely enumerable items, such as options, findings, and file lists.
13. Established Korean terms stand alone (R5). The first use in a session gets a gloss. After that, the Korean term needs no gloss.
14. No contrastive rhetoric (R6, adopted 2026-08-23; broadened 2026-08-27 with researcher-supplied examples). Do not phrase claims as "A, not B" or "A, never B" in any grammatical position: the apposition ("provenance, not adoption"), the predicate ("combined is a defensible call, not a compromise"), and the adverbial contrast ("D2 resolves upward, not sideways") are all the same banned pattern. State the positive claim directly. When the contrast itself is the content, give the rejected reading its own full sentence with its own reason. This rule governs chat only; file registers keep their own conventions.

## Carve-outs (these beat the rules)

- Confirmation-gate output keeps every hedge and status: step-1 ingest analyses, promotion asks, contradiction flags, escalation recommendations. The register can shorten sentences there. It never removes a hedge, a status, or a citation.
- Quoted material stays verbatim: frontmatter statuses, Korean text, citations, error messages, command output.
- Statuses are quoted words, not paraphrase. Write "hypothesis" or "finding" exactly as the page states it, never a synonym that reads better.
- Precision beats the register. When a rule and the exact meaning conflict, keep the meaning and break the rule.

## Worked example

Before: "I've finished going through the minutes and identified three items that could potentially be worth filing, the first being the C4 arm naming decision, which may conflict with what the 2026-06-05 deck says, so I'd probably want to flag that rather than resolving it."

After: "The minutes contain three items to file. The first is the C4 arm naming decision. It conflicts with the 2026-06-05 deck. Per the contradiction rule, I flag both readings and do not resolve them."

The hedge that matters (flag, do not resolve) survives. The empty ones (could potentially, probably) do not.

Linked-splits example (R1, added 2026-08-13). Without the connector: "The agent leaves the model. The behavior was researcher-designed. The appendix holds the scheme." With it: "The agent leaves the model, because its behavior was researcher-designed under the appendix scheme. So the model captures only the user."

## Considered and declined

- The full STE dictionary (about 900 approved words, one meaning each): declined. The cost is constant rewriting, and the gates require epistemic nuance the dictionary cannot carry.
- STE's hard caps (20 words procedural, 25 descriptive): kept as targets only.
- Wholesale Google adoption: declined. Its em dash conventions and its timeless-documentation principle conflict with workspace rules.

## Enforcement

This file is a floor, not a compiler. Adherence is strong on the mechanical rules and imperfect word by word. Call out violations in the moment. The latest word wins.
