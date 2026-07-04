#!/usr/bin/env bash
set -euo pipefail

PAY='{"trace_id":"det_001","normative":[0.85,0.92,0.77,0.81],"representational":[0.78,0.88,0.70,0.74],"informational":[0.95,0.91,0.89,0.90],"physical":[1200,8,55,12]}'

echo "Running 20 sequential requests to verify determinism..."
for i in $(seq 1 20); do
  curl -s -X POST http://localhost:8000/api/coherence/measure \
    -H 'Content-Type: application/json' \
    -d "$PAY" | grep -o '"C_total":[0-9.]*' | cut -d: -f2
done | sort | uniq -c

echo "Check complete."
