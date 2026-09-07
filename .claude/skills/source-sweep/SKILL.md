---
name: source-sweep
description: Run the useful-source gatherer - sweep Hacker News, the open web, and X for how other researchers and developers build agentic research setups (or a given topic), spot-check the findings, and present a ranked digest for discussion. Use when asked to "sweep sources", "run the gatherer", or "what are others doing with their setups".
---

# Source sweep (the useful-source gatherer)

The gatherer READS and PROPOSES; it never edits wiki pages, config, or contracts. Adoptions
happen in discussion afterward and land in the decisions ledger (decisions/2026-08.md holds
the lineage), never directly from a sweep.

## Scope

- Hacker News via the Algolia API (hn.algolia.com/api/v1/search): free and reliable; verify
  promising hits by fetching the thread.
- Open web via WebSearch/WebFetch: blogs, GitHub repos, writeups. Prefer originals over
  aggregators; SEO listicles and product marketing rank low or are excluded.
- X via the pay-per-use API: recent search only, bearer auth. Costs real money (see budget).
- Reddit and Bluesky are OUT: both measured server-side 403 from this environment
  (2026-08-21). Revisit only if access changes; do not retry them every run.

## Run shape

1. Topic: from the invocation argument; default is "agentic research workspace setups"
   (research wikis, CLAUDE.md conventions, agent memory, multi-model verification).
2. Launch two Sonnet background sweep agents (Tier 1 legwork): one HN-native (Algolia search
   plus thread reads, including one buzz-class query per run), one open-web. Both prompts
   carry the honesty contract: report ONLY pages actually fetched this session; never invent
   URLs, titles, dates, or numbers; verify the shape of each response (an HTTP 200 can carry
   an empty body, an error payload, or a fetch summarizer's guess), so a page counts as read
   only when its content matches what is reported; list failed endpoints under "dead ends"; mark partial or
   snippet-only reads as such.
3. Registry diff (runs in CI because the cloud sandbox cannot reach openrouter.ai): the diff
   runs in
   `.github/workflows/registry-diff.yml` (Mondays 00:15 UTC, open egress) via
   `tools/registry_diff.py`, which commits the snapshot and the report
   `_workspace-notes/sweeps/.registry-diff-latest.md`. A sweep READS that report and folds
   its added/removed models into the digest's buzz section; it never fetches openrouter.ai
   itself in cloud runs. Fail-loud: if the report's generated date is more than 8 days
   old, the digest says the B2 guarantee is not in force. Local sessions may run
   `tools/registry_diff.py` directly for a live diff. This deterministic diff, and never
   social chatter, is the guarantee against missing a model drop (motivating cases: Ox
   Alpha's appearance 2026-08, and its removal caught by the first diff, 2026-09-01).
4. X leg, run in the main session via Bash:
   - Token: `security find-generic-password -s x-api-bearer-token -w` (macOS Keychain).
     Never echo credentials, never write them to any file, never send them anywhere except
     api.x.com.
   - Endpoint: GET https://api.x.com/2/tweets/search/recent (covers roughly the last 7 days
     only), with `tweet.fields=created_at,public_metrics`.
   - Queries: two or three keyword VARIANTS per topic, each
     anchored on a different term (e.g. one on "claude code", one on "AGENTS.md", one on
     "research wiki") so recall does not hinge on a single phrasing. Every variant ends with
     `has:links -is:retweet lang:en`; has:links pre-filters for posts that point at a repo or
     writeup, which is where run 1's only real lead came from. Follow t.co links of
     promising posts and verify the target page before reporting it.
   - Buzz variant: one variant per run uses model-drop vocabulary
     (OpenRouter, stealth model, "new model" plus coding or agent terms) instead of setup
     vocabulary. Read buzz results engagement-sorted; buzz behaves opposite to the setup
     topic, where low-engagement items held the gems.
   - Skip user expansions (`expansions=author_id`): user objects bill separately at $0.010
     each, and `https://x.com/i/web/status/<id>` links posts without needing usernames.
   - Budget: X bills $0.005 per post READ (Posts: Read, priced 2026-08-21). Spread the reads
     across the variants (max_results 10-25 each); hard per-run ceiling 50 posts TOTAL across
     all variants (about $0.25). The $5/month cap is enforced in the X Developer Console.
     After each run, report posts read and the computed cost, and note that the Console
     billing page is the ground truth, not the estimate.
   - Public posts only. Never fetch user timelines, DMs, or follower data; never post,
     like, or reply. HTTP 402 means credits are depleted: stop the X leg, say so, and
     continue the free legs.
   - Cloud sessions: the Keychain is unreachable there, so skip this leg entirely and note
     the skip in the digest.
4b. Cloud egress reality (measured 2026-08-31): github.com is reachable; openrouter.ai,
   hn.algolia.com, news.ycombinator.com, arxiv.org, and most blog domains are blocked at
   the proxy. In cloud, the HN leg falls back to site-restricted WebSearch and writes
   points and dates as "unrecorded". Whenever any leg is blocked, skipped, or degraded,
   the digest OPENS with a "## Run integrity" section saying exactly what did not run.
   Never present a degraded run as a full sweep.
5. Spot-check before presenting (Tier 1 output is unverified): re-fetch at least the top 3
   items and confirm the claims attributed to them. Drop or flag anything that fails.
6. Digest to chat: ranked items grouped by adoptable theme; each with URL, date, what they
   built, the adoptable idea mapped to an existing workspace mechanism, and evidence of
   substance. Buzz items (new models, tools) get their own section: verify every buzz item
   against its primary registry page before
   filing, with pricing and the data-policy line quoted from the registry, never from the
   post; link the standing conclusions (stealth models are council-ineligible per the
   llm-council fail-closed invariant, transient, measured against and never built on)
   instead of re-deriving them per item. Close with dead ends and a one-line honest signal
   read. A quiet sweep says so plainly; never manufacture findings.
7. Filing: after presenting the digest in chat, file it to
   `_workspace-notes/sweeps/YYYY-MM-DD-<topic-slug>.md`. The file is Obsidian-read, so one
   item per source line and no hard wraps, with full frontmatter (title, type: reference,
   status: reference, created, updated, sources: the swept URLs). Mark re-fetched items
   [verified]; keep unverified claims flagged in the file. Filing is provenance, not
   adoption: adoptions still go through discussion and the decisions ledger.

## Hard rules

- Run on explicit researcher invocation (/source-sweep or an unambiguous "run the
  gatherer/sweep" ask), or as the ONE sanctioned scheduled run: the weekly Monday cloud
  routine. Never start a sweep proactively because the
  conversation is merely topical. The X leg never runs from any schedule: it needs the local
  Keychain and spends real money, so cloud runs skip it, say so in the digest, and leave X
  coverage to local invocations. If an unscheduled sweep seems useful, propose it and wait
  for a yes. Scheduled or not, a sweep only ever proposes: adoption stays a researcher
  decision made in discussion and recorded in the ledger.
- Never edit wiki/, raw/, project config, or command/skill contracts from a sweep. A sweep
  writes exactly one file, its digest; the registry snapshot and diff report under
  `_workspace-notes/sweeps/` are CI-owned and never touched by a sweep.
- Sweep queries are topic queries. Nothing participant-adjacent ever goes into a search box.
- Numbers in the digest quote the fetched page. If a metric was not on the page, write
  "unrecorded", never a plausible value.
