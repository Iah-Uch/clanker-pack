#!/usr/bin/env bash
# Run a plan one slice at a time, each in a fresh Claude Code context.
# Usage: run-slices.sh PLAN.md [--dry-run]
# PLAN.md holds one slice per line as "- [ ] text". A finished slice becomes "- [x] text".
# Env: SLICE_MODEL (default sonnet), SLICE_EFFORT (default low), SLICE_TIMEOUT (default 900s),
#      SLICE_BUDGET_USD (default 2), GATE_CMD (run once after the last slice).
set -euo pipefail

plan=${1:?usage: run-slices.sh PLAN.md [--dry-run]}
dry=${2:-}
model=${SLICE_MODEL:-sonnet}
effort=${SLICE_EFFORT:-low}
limit=${SLICE_TIMEOUT:-900}
budget=${SLICE_BUDGET_USD:-2}

next_line() { grep -n -m1 -- '- \[ \]' "$plan" | cut -d: -f1 || true; }

while n=$(next_line); [ -n "$n" ]; do
  text=$(sed -n "${n}p" "$plan")
  echo "== slice at line $n: $text"
  [ "$dry" = "--dry-run" ] && { echo "(dry run, stopping)"; exit 0; }
  prompt="Do ONLY this slice from $plan, line $n: ${text#*] }
Read $plan for context. Make the change. Do not run the full test suite; run only checks for the files you touched.
Then change line $n of $plan from '- [ ]' to '- [x]' and add one indented line saying what changed. Stop."
  timeout "$limit" claude -p "$prompt" --model "$model" --effort "$effort" \
    --max-budget-usd "$budget" --permission-mode auto >/dev/null || {
    echo "slice failed or timed out; stopping" >&2; exit 1; }
  if [ "$(sed -n "${n}p" "$plan" | grep -c -- '- \[x\]')" -ne 1 ]; then
    echo "slice did not mark itself done; stopping" >&2; exit 1
  fi
done

echo "== all slices done"
if [ -n "${GATE_CMD:-}" ]; then echo "== gate: $GATE_CMD"; bash -c "$GATE_CMD"; fi
