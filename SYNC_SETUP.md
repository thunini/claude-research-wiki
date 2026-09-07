# Sync & Tooling Setup

## 1. Stop syncing the vault through Google Drive

Move the vault out of the Google Drive folder. Drive's consumer sync is unsafe for active app
data and the hidden `.obsidian` config, and editing from two machines causes duplicate files and
silent reversion to older versions. This is a known, recurring failure, not an edge case. Your
lab PC to home PC sync should run on git instead.

## 2. Git as the sync (Mac M1 + Windows 11)

Git is the right tool here, and its manual push/pull is a feature for a wiki, since you snapshot
deliberately instead of letting a background daemon fight you.

1. Create a **private** remote (a private GitHub repo is fine).
2. On both machines: install git, `git clone` the repo to a normal local path (not inside Drive).
3. Session start: `git pull`. Session end: `git add -A && git commit -m "..." && git push`.
4. The included `.gitattributes` forces LF line endings so Mac and Windows do not churn the diff.
5. The included `.gitignore` drops `.obsidian/workspace.json`, which changes constantly per
   machine and would otherwise conflict every sync.

Open the same cloned folder as your Obsidian vault on both machines. Same files, git-synced, no
Drive involved.

## 3. IRB data caution

Do not push identifiable participant data to a cloud remote unless your IRB approves cloud
storage. The schema already de-identifies to participant IDs, but transcripts in `raw/study/`
can still be sensitive. If your IRB restricts where data may live, uncomment the `*/raw/study/`
line in `.gitignore` and keep that data on lab-approved storage, syncing only the wiki and
de-identified material. Confirm against your actual IRB before the first study collects data.

## 4. Claude Code on both machines

macOS (M1) runs Claude Code natively. On Windows 11, confirm whether you are on the native build
or WSL, and keep the cloned vault on a normal filesystem path either way. Node.js is required on
both.

## 5. Citation manager: use Zotero

You have none and asked if one helps. It does, specifically at the draft-to-Docs boundary. Zotero
is free, open, and runs on Mac and Windows. The fit:
- The browser connector captures papers; the PDF goes to `raw/papers/`.
- Better BibTeX gives each paper a stable cite key.
- `/draft` emits source markers using those keys.
- The Zotero Google Docs plugin inserts live, formatted citations in your manuscript, with ACM
  styles for CHI, IMWUT, and CSCW.

That keeps every sentence in the Google Doc traceable back to a wiki page and a Zotero entry.
