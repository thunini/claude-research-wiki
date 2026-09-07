#!/bin/bash
# W2: cross-family voice/style check, "council of one" (adopted 2026-08-21, W-menu).
# One OpenRouter call: a non-Anthropic model reads _schema/voice.md + the document and
# returns violations (mechanical + judgment) plus a judgment-layer read. Pre-gate use:
# run before a document faces an advisor meeting, submission, or rebuttal.
#
# Guards, per the llm-council hard rule (participant data never enters the council):
# - Refuses paths under raw/study/ or raw/interviews/.
# - Refuses documents containing P-ID patterns (P1..P99) unless the researcher approves
#   the exact document for sending, expressed with --approved.
# The researcher sees/names the document before it leaves the machine (council protocol
# step 2); invoking this script on a named file IS that approval for clean documents.
#
# Key: read at runtime from the llm-council repo's gitignored .env. Never stored, never
# printed. Model + max_tokens mirror the council config (empty-ballot lesson: 8192).
set -euo pipefail

DOC="${1:?usage: voice-check.sh <document.md> [--approved]}"
APPROVED="${2:-}"
VOICE="$(dirname "$0")/../_schema/voice.md"
ENVF="$HOME/Desktop/Codes/llm-council/.env"

case "$DOC" in
  *raw/study/*|*raw/interviews/*) echo "REFUSED: participant-data location." >&2; exit 2;;
esac
if grep -qE '\bP[0-9]{1,2}\b' "$DOC" && [ "$APPROVED" != "--approved" ]; then
  echo "REFUSED: document contains P-ID patterns. If the researcher has reviewed this exact" >&2
  echo "document and approves sending it, re-run with --approved." >&2
  exit 2
fi

KEY=$(grep '^OPENROUTER_API_KEY=' "$ENVF" | cut -d= -f2- | tr -d '"'"'")
[ -n "$KEY" ] || { echo "no OPENROUTER_API_KEY in $ENVF" >&2; exit 1; }

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
DOC="$DOC" VOICE="$VOICE" python3 - > "$TMP/payload.json" <<'EOF'
import json, os
voice = open(os.environ["VOICE"], encoding="utf-8").read()
doc = open(os.environ["DOC"], encoding="utf-8").read()
system = ("You are an independent writing-style reviewer for a researcher's document. Apply ONLY "
"the rule file below (a voice guide plus its Writing Quality Check). Report violations grouped "
"by category. For each: a short verbatim quote (under 15 words), the category, whether it is "
"MECHANICAL (rule applies without judgment) or JUDGMENT (requires editorial judgment), and a "
"one-line suggested fix. Do not invent rules beyond the file. After the violations, add a "
"section 'Judgment-layer read': 3-6 sentences on burstiness, structural monotony, hedge "
"honesty, and register fit against the samples in the rule file. Be terse and concrete. "
"If a rule category has no violations, say so in one line.\n\n=== RULE FILE ===\n" + voice)
print(json.dumps({"model": "openai/gpt-5.6-sol", "max_tokens": 8192, "messages": [
    {"role": "system", "content": system},
    {"role": "user", "content": "Document to check (markdown, YAML frontmatter is data, not prose):\n\n" + doc}]}))
EOF

curl -sS --max-time 180 -X POST https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" \
  --data @"$TMP/payload.json" -o "$TMP/resp.json"

python3 - "$TMP/resp.json" <<'EOF'
import json, sys
r = json.load(open(sys.argv[1]))
if "choices" not in r:
    print("API error:", json.dumps(r)[:500]); sys.exit(1)
print(r["choices"][0]["message"]["content"])
u = r.get("usage", {})
print(f"\n---USAGE--- prompt={u.get('prompt_tokens')} completion={u.get('completion_tokens')} model={r.get('model')}")
EOF
