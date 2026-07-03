#!/usr/bin/env bash
set -euo pipefail

mkdir -p evidence

# 1. Canonical Payload
cat > evidence/payload_dim4.json <<'JSON'
{
  "trace_id": "canon_dim4",
  "normative": [0.85, 0.92, 0.77, 0.81],
  "representational": [0.78, 0.88, 0.70, 0.74],
  "informational": [0.95, 0.91, 0.89, 0.90],
  "physical": [1200, 8, 55, 12]
}
JSON

# 2. Determinism (20 counts)
echo "--- 1. Determinism (Kernel 8000) ---"
for i in $(seq 1 20); do
  curl -s -X POST http://localhost:8000/api/coherence/measure \
    -H 'Content-Type: application/json' \
    --data-binary @evidence/payload_dim4.json \
  | grep -o '"C_total":[0-9.]*' | cut -d: -f2
done | sort | uniq -c

# 3. Parity (Backend 4000 vs Kernel 8000)
echo -e "\n--- 2. Parity (8000 vs 4000) ---"
K="evidence/parity_kernel_canon.json"
B="evidence/parity_backend_canon.json"
curl -s -X POST http://localhost:8000/api/coherence/measure -H 'Content-Type: application/json' --data-binary @evidence/payload_dim4.json > "$K"
curl -s -X POST http://localhost:4000/api/coherence/measure -H 'Content-Type: application/json' --data-binary @evidence/payload_dim4.json > "$B"

K_VAL=$(grep -o '"C_total":[0-9.]*' "$K" | cut -d: -f2)
B_VAL=$(grep -o '"C_total":[0-9.]*' "$B" | cut -d: -f2)
echo "Kernel : $K_VAL"
echo "Backend: $B_VAL"
[ "$K_VAL" == "$B_VAL" ] && echo "MATCH: YES" || echo "MATCH: NO"
