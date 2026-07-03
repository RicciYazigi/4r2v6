#!/usr/bin/env bash
set -euo pipefail

PAYLOAD="evidence/payload_dim4.json"
OUT="evidence/soak_120min_$(date +%Y%m%d_%H%M%S).jsonl"

echo "Launching 120-minute soak (1 req/min)... Log: $OUT"

for i in $(seq 1 120); do
  ts="$(date -Is)"
  resp=$(curl -sS -X POST http://localhost:8000/api/coherence/measure \
    -H 'Content-Type: application/json' --data-binary "@$PAYLOAD" || echo '{"error":"curl_failed"}')
  printf '%s\t%s\n' "$ts" "$resp" >> "$OUT"
  sleep 60
done &

echo "Soak process backgrounded successfully."
