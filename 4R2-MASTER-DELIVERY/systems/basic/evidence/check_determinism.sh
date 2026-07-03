#!/usr/bin/env bash
set -euo pipefail

PAYLOAD="evidence/payload_dim4.json"
OUT="evidence/determinism_$(date +%Y%m%d_%H%M%S).txt"

echo "Running 20 sequential requests to verify determinism..."
for i in $(seq 1 20); do
  curl -s -X POST http://localhost:8000/api/coherence/measure \
    -H 'Content-Type: application/json' \
    --data-binary "@$PAYLOAD" | grep -o '"C_total":[0-9.]*' | cut -d: -f2
done | tee "$OUT" | sort | uniq -c

echo "Check complete. Output in $OUT"
