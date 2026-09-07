---
description: Draft output (paper section, report, paragraph) from the wiki, voice-matched and cited
---
Draft: $ARGUMENTS

Before writing, decide the output type and its status policy:
- Paper results or findings text: use `finding` pages ONLY. If a needed claim is only a
  `hypothesis`, stop and tell me. Do not state a hypothesis as a result.
- Proposal, future work, or RQ motivation: `hypothesis` allowed, but label each as planned or
  expected, not established.
- Progress report or advisor update: both allowed, each claim tagged with its status.

Then read index.md and grep to the relevant pages. Do not load the whole wiki.

Write the draft:
- Match my voice in _schema/voice.md.
- List the wiki pages and raw sources the draft draws on in the frontmatter `sources:` field. Do
  not put inline source markers in the prose.
- LaTeX output (paper sections headed `\section`, bound for Overleaf) must escape every special
  character in the prose or it will not compile: write `\_` not `_`, `\%` not `%`, and likewise
  `\&`, `\#`, `\$`. The repeat offenders here are coded slot labels (`User\_state`,
  `Personal\_history`) and every percentage (`30.1\%`). Leave real LaTeX alone: command names,
  the `~` tie before `\ref`, and any `%` meant as a source comment.
- Save to drafts/ in this project with a dated filename. Never write prose drafts into wiki/.

Voice gate:
- Run `python3 tools/voice-lint.py <draft-file>` from the workspace root (W1, the mechanical
  layer, report-only). Apply the mechanical fixes it surfaces, per the Writing Quality Check
  output rule; surface the judgment calls to the researcher.
- Run the voice.md `# Writing Quality Check` self-review as before. W1 does not replace it.
- If the draft is bound for a gate (advisor meeting, submission, rebuttal), offer the W2
  cross-family pass: `tools/voice-check.sh <draft-file>` (one OpenRouter call, non-Anthropic
  model, council plumbing and its participant-data guard: the script refuses P-ID documents
  unless the researcher approves the exact document with --approved). W2 output is critique,
  hypothesis grade: apply nothing from it without researcher review.

After writing, if the draft exposed a gap or a new synthesis, offer to file it in wiki/questions/
as a hypothesis, or a finding only if it rests on data. The draft itself stays in drafts/.
