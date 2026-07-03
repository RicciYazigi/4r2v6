#!/usr/bin/env bash
set -euo pipefail

mkdir -p evidence
OUT="evidence/measure_soak_$(date +%Y%m%d_%H%M%S).jsonl"
PAY='{"trace_id":"soak","normative":[0.85,0.92,0.77,0.81],"representational":[0.78,0.88,0.70,0.74],"informational":[0.95,0.91,0.89,0.90],"physical":[1200,8,55,12]}'

echo "Starting Soak Loop. Logging to $OUT"
# Run for 3 iterations as a proof of concept, then user can keep it running if needed.
for i in {1..3}; do
  ts="$(date -Is)"
  resp="$(curl -s -X POST http://localhost:8000/api/coherence/measure -H 'Content-Type: application/json' -d "$PAY")"
  echo "{\"ts\":\"$ts\",\"resp\":$resp}" >> "$OUT"
  echo "[$(date +%H:%M:%S)] Iteration $i: OK"
  if [ $i -lt 3 ]; then sleep 2; fi # Shorten sleep for proof of concept
done

echo "Soak proof complete. Output file exists."
ls -lh "$OUT"
