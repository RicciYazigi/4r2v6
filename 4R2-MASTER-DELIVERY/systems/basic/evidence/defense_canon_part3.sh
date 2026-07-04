#!/usr/bin/env bash
set -euo pipefail

PAYLOAD="evidence/payload_dim4.json"

echo "--- 5. Soak Proof (5 iterations, 10s interval) ---"
OUT="evidence/soak_canon_proof.jsonl"
: > "$OUT"
for i in {1..5}; do
  ts="$(date -Is)"
  resp="$(curl -sS -X POST http://localhost:8000/api/coherence/measure -H 'Content-Type: application/json' --data-binary "@$PAYLOAD")"
  printf '%s\t%s\n' "$ts" "$resp" >> "$OUT"
  echo "[$(date +%H:%M:%S)] Iteration $i: OK"
  sleep 2
done
echo "Soak proof complete. Log: $OUT"

echo -e "\n--- 6. Negative Contract (Dimensional Mismatch) ---"
echo "A) physical with 3 elements (expected 500):"
curl -s -i -X POST http://localhost:8000/api/coherence/measure \
  -H 'Content-Type: application/json' \
  -d '{"trace_id":"neg_phys_3","normative":[1,1,1,1],"representational":[1,1,1,1],"informational":[1,1,1,1],"physical":[1200,8,55]}' | grep 'HTTP/'

echo "B) layer mismatch (N=4, I=3) (expected 500):"
curl -s -i -X POST http://localhost:8000/api/coherence/measure \
  -H 'Content-Type: application/json' \
  -d '{"trace_id":"neg_mismatch","normative":[1,1,1,1],"representational":[1,1,1,1],"informational":[1,1,1],"physical":[1200,8,55,12]}' | grep 'HTTP/'
