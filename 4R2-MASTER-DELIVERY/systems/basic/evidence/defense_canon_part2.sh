#!/usr/bin/env bash
set -euo pipefail

PAYLOAD="evidence/payload_dim4.json"

echo "--- 3. Concurrency (Backend 4000 - 200 req, P20) ---"
seq 1 200 | xargs -n1 -P20 -I{} bash -lc "
  code=\$(curl -s -o /dev/null -w \"%{http_code}\" -X POST http://localhost:4000/api/coherence/measure \
    -H \"Content-Type: application/json\" --data-binary @$PAYLOAD || echo \"000\")
  echo \"\$code\"
" | sort | uniq -c

echo -e "\n--- 4. Latency Profiling (Kernel 8000 - 50 req) ---"
LAT="evidence/latency_canon.txt"
for i in $(seq 1 50); do
  curl -s -o /dev/null -w "%{time_total}\n" \
    -X POST http://localhost:8000/api/coherence/measure \
    -H 'Content-Type: application/json' \
    --data-binary "@$PAYLOAD"
done > "$LAT"

# p50 / p95 logic (sed/awk)
NUMS=$(sort -n "$LAT")
COUNT=$(echo "$NUMS" | wc -l)
P50_IDX=$((COUNT / 2))
P95_IDX=$((COUNT * 95 / 100))
[ "$P95_IDX" -eq 0 ] && P95_IDX=1

P50=$(echo "$NUMS" | sed -n "${P50_IDX}p")
P95=$(echo "$NUMS" | sed -n "${P95_IDX}p")
MAX=$(echo "$NUMS" | tail -n1)

echo "n  : $COUNT"
echo "p50: $P50 s"
echo "p95: $P95 s"
echo "max: $MAX s"
