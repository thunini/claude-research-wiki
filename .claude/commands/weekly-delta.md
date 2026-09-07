---
description: Summarize what changed in the wiki over the past week, grounded in git, organized by research meaning
---
Produce a weekly delta summary for: $ARGUMENTS (a project folder, or the workspace root for all active projects; default to the current project). Cover the last 7 days unless I give a different window.

Ground the delta in git, not memory. Never report a change you cannot see in the repo.

1. Get the objective delta:
   - Find the commit from about 7 days ago: `git rev-list -1 --before="7 days ago" HEAD`. If no commit is that old, summarize all history to date and say so.
   - Diff it against HEAD: `git diff --stat <commit>..HEAD` for the file-level picture, and `git log --since="7 days ago" --oneline` for the commit narrative.
   - Inspect the changed wiki files. Attend to frontmatter `status:` changes, pages created in the window, `wiki/questions/` changes, `wiki/feedback/` status changes, and task lines (`- [ ] ... [due:: ...]`).
   - Cross-check the `wiki/log.md` entries dated in the window. If log.md and git disagree, trust git and note the discrepancy.
   - If git shows no changes in the window, say so plainly. Do not invent activity.

2. Write a **TL;DR** at the top: at most five bullets covering the week's most important changes, ordered by significance (promotions to finding first). This block is what the weekly loop posts to Slack, so keep it self-contained and free of file paths.

3. Below the TL;DR, the full summary, organized by research meaning, not by filename, under these headings (omit any that are empty):
   - **New findings.** Pages added or promoted to `finding`. For any hypothesis-to-finding promotion, name it and cite the evidence that justified it, so I can sanity-check the promotion.
   - **New questions and hypotheses.** Changes in `wiki/questions/`.
   - **Literature added.** New `reference` pages or ingested papers.
   - **Feedback.** Advisor or peer feedback newly opened, and any flipped from open to addressed.
   - **Tasks.** Completed, newly added, and now overdue.
   - **Drafts.** Anything produced in `drafts/`.
   - **Revisions.** Pages whose confidence dropped, were contradicted, or were archived.

4. Close with two forward lines: the unresolved open questions, the overdue or imminent tasks, and the deadline proximity from `_project.md` (for example the CHI countdown).

Formatting — no hard-wrapping: one paragraph or bullet per source line, per the schema's Line-wrapping rule (the Slack CI renders every newline literally, so a mid-sentence wrap corrupts the posted digest).

Write the report to `drafts/weekly/YYYY-MM-DD-weekly-delta.md` (create `drafts/weekly/` if it does not exist), status `hypothesis`, in my voice (see `_schema/voice.md`; run its `# Writing Quality Check` section on the report before saving). Korean terms preserved with a short gloss. Never edit wiki content, with one exception: the run's single dated log.md entry recording that the report was written (shared with the same run's /lint entry). When `wiki/standing-items.md` exists, cite carried judgment items as `SI-n` rather than re-deriving their prose. This command writes the report only; the weekly loop is what posts the TL;DR to Slack.

At the workspace root, do this per active project and add a three-line cross-project roll-up at the top.
