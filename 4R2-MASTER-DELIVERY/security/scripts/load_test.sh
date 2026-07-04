#!/usr/bin/env bash
set -euo pipefail

PAY='{"trace_id":"load_001","normative":[0.85,0.92,0.77,0.81],"representational":[0.78,0.88,0.70,0.74],"informational":[0.95,0.91,0.89,0.90],"physical":[1200,8,55,12]}'

echo "Starting Concurrent Load Test: 200 requests, P=20..."
time seq 1 200 | xargs -n1 -P20 -I{} \
  curl -s -o /dev/null -w "%{http_code}\n" -X POST http://localhost:4000/api/coherence/measure \
  -H 'Content-Type: application/json' \
  -d "$PAY" | sort | uniq -c

echo "Load test complete."
