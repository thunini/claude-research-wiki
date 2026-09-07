---
description: Scaffold a new project wiki under the workspace schema
---
Create a new project folder named "$ARGUMENTS" in this workspace, mirroring the structure of
`cumpa-latency-fillers/`. First ask me for the RQ, project title, target venue, deadline, the
Drive links (master meeting-notes doc, slides deck), and a prior-work link, then fill them in.

1. Make the raw/ subfolders: notes, study, system, papers, assets.
2. Make the wiki/ subfolders: questions, themes, concepts, comparisons, system, design, methods,
   feedback (where /ingest-feedback writes), papers (where paper-ingest files reference pages).
3. Make drafts/ — where /draft, /meeting-prep, /weekly-delta, and gap memos write. Prose drafts
   never go into wiki/.
4. Create _project.md. The dashboard's Dataview queries read it, so the frontmatter is
   load-bearing and must use exactly these keys:
   ---
   type: project
   project: <full project title>
   stage: early
   venue: <target venue, or TBD>
   deadline: <YYYY-MM-DD, or TBD>
   drive_master: <master meeting-notes doc URL>
   drive_slides: <slides deck URL>
   last_ingested:
   ---
   Body sections:
   - `## Documents` — one line per document in flight, e.g.
     `- [ ] <doc> [doc_type:: paper] [status:: planning] [due:: YYYY-MM-DD]`. Add `[due:: ]`
     only when a real deadline exists; never write it empty.
   - `## Tasks` — with the standing note that action items are tracked at their source (each
     wiki/feedback/ page's "Resulting actions" checklist), never mirrored here; a task lands
     here only if it belongs to no specific feedback page.
   - `## Links` — pointers to the Drive docs above and any prior-work wiki.
5. Create the project CLAUDE.md with sections: What this study is, Target (venue and deadline),
   Prior work (reference, do not copy), Current data status, Project-specific conventions.
   Do NOT restate the schema; it loads from the parent.
6. Create wiki/index.md (the router, type overview) and wiki/log.md (type log,
   reverse-chronological: newest entry at the top, prepended under the `# Log` heading) with an
   init entry.
7. Add a row to ../projects.md (the hand-maintained cross-project table). The live
   _dashboard.md needs no edit; it picks the project up from the _project.md frontmatter.
