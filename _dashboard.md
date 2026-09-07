---
title: "Research Dashboard"
type: dashboard
---

# Research Dashboard

Live views over the workspace. Requires the Dataview plugin (Settings > Community plugins).
Nothing here is hand-maintained. It reads the frontmatter and inline fields you already write.

> Note: each project is a **nested subfolder** (`<project>/_project.md`, `<project>/wiki/...`).
> So these queries scan the **whole vault** and filter by `type` / inline fields — do **not**
> add `FROM "."` or `FROM "wiki/..."` (the old root-only sources matched nothing).

## Projects
```dataview
TABLE WITHOUT ID link(file.link, project) AS "Project", stage, venue, deadline,
  choice(deadline AND deadline < date(today), "OVERDUE",
    choice(deadline, (deadline - date(today)).day + " days", "no deadline")) AS "time left",
  last_ingested AS "last ingest"
WHERE type = "project"
SORT deadline ASC
```

## Open action items (by project)
Gathers from each project's `_project.md` **and** every `wiki/feedback/` page (where
`/ingest-feedback` writes "Resulting actions"). Scoped by path so coding-sheet and template
checkboxes elsewhere are excluded. Single source of truth — action items are **not** mirrored
into `_project.md`.

Priority is a leading marker in the task text at its source: 🔴 high, 🟡 medium, 🟢 low.
Unmarked = normal, sorts between 🟡 and 🟢. Items sort high → low inside each project group.
Due dates belong on document lines (paper, IRB) and the rare hard-dated action only — never
write an empty `[due:: ]`. Document lines are tracked in "Documents in flight", not here.
```dataview
TASK
WHERE !completed AND (file.name = "_project" OR contains(file.folder, "feedback")) AND !doc_type
SORT choice(contains(text, "🔴"), 1, choice(contains(text, "🟡"), 2, choice(contains(text, "🟢"), 4, 3))) ASC
GROUP BY split(file.folder, "/")[0]
```

## Due this week
Catches document deadlines and the rare hard-dated action item.
```dataview
TASK
WHERE !completed AND due AND due <= date(today) + dur(7 days)
SORT due ASC
```

## Documents in flight
```dataview
TABLE WITHOUT ID file.folder AS "project", doc.doc_type AS "type", doc.status AS "status", doc.due AS "due"
WHERE type = "project"
FLATTEN file.lists AS doc
WHERE doc.doc_type AND doc.status != "approved" AND doc.status != "submitted"
SORT doc.due ASC
```

## Open questions (the live research agenda)
```dataview
TABLE confidence, file.folder AS "project"
WHERE type = "question" AND status = "hypothesis"
SORT file.mtime DESC
```

## Open feedback (advisor steer, unresolved)
```dataview
TABLE source, meeting, target
WHERE type = "feedback" AND status = "open"
SORT meeting DESC
```

## Recent activity
```dataview
TABLE file.folder AS "project", file.mtime AS "updated"
WHERE type = "log"
SORT file.mtime DESC
LIMIT 10
```

## Standing
- [x] Friday: prep brief for professor meeting (run `/meeting-prep`, skip if cancelled) [due:: 2026-06-05]
