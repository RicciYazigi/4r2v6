#!/usr/bin/env bash
set -euo pipefail

PAYLOAD="evidence/payload_dim4.json"
K="evidence/parity_kernel_$(date +%Y%m%d_%H%M%S).json"
B="evidence/parity_backend_$(date +%Y%m%d_%H%M%S).json"

echo "Checking parity between Kernel (8000) and Backend (4000)..."
curl -s -X POST http://localhost:8000/api/coherence/measure -H 'Content-Type: application/json' --data-binary "@$PAYLOAD" | tee "$K" > /dev/null
curl -s -X POST http://localhost:4000/api/coherence/measure -H 'Content-Type: application/json' --data-binary "@$PAYLOAD" | tee "$B" > /dev/null

K_VAL=$(grep -o '"C_total":[0-9.]*' "$K" | cut -d: -f2)
B_VAL=$(grep -o '"C_total":[0-9.]*' "$B" | cut -d: -f2)

echo "C_total kernel : $K_VAL"
echo "C_total backend: $B_VAL"

if [ "$K_VAL" == "$B_VAL" ]; then
    echo "MATCH: YES"
else
    echo "MATCH: NO"
fi
