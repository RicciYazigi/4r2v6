#!/usr/bin/env bash
set -euo pipefail

PAYLOAD="evidence/payload_dim4.json"
TS="$(date +%Y%m%d_%H%M%S)"
ERR="evidence/load_err_$TS.txt"
OK="evidence/load_ok_$TS.txt"
LAT="evidence/latency_$TS.txt"

echo "Starting Concurrent Load Test: 200 requests, P=20..."
seq 1 200 | xargs -n1 -P20 -I{} bash -lc "
  code=\$(curl -s -o /dev/null -w \"%{http_code}\" -X POST http://localhost:8000/api/coherence/measure \
    -H \"Content-Type: application/json\" --data-binary @$PAYLOAD || echo \"000\")
  echo \"\$code\"
" | tee evidence/load_codes_$TS.txt > /dev/null

grep -v '^200$' evidence/load_codes_$TS.txt > "$ERR" || true
grep '^200$' evidence/load_codes_$TS.txt > "$OK" || true

echo "Errors: $(wc -l < \"$ERR\")"
echo "Success: $(wc -l < \"$OK\")"

echo "Running 50 requests for latency profiling..."
for i in $(seq 1 50); do
  curl -s -o /dev/null -w "%{time_total}\n" \
    -X POST http://localhost:8000/api/coherence/measure \
    -H 'Content-Type: application/json' \
    --data-binary "@$PAYLOAD"
done | tee "$LAT" > /dev/null

# Basic p50/p95 using sort/awk
NUMS=$(sort -n "$LAT")
COUNT=$(echo "$NUMS" | wc -l)
P50_IDX=$((COUNT / 2))
P95_IDX=$((COUNT * 95 / 100))

P50=$(echo "$NUMS" | sed -n "${P50_IDX}p")
P95=$(echo "$NUMS" | sed -n "${P95_IDX}p")
MAX=$(echo "$NUMS" | tail -n1)

echo "n=$COUNT"
echo "p50=$P50"
echo "p95=$P95"
echo "max=$MAX"
