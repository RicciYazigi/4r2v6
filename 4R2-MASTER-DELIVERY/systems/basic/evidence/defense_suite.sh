#!/usr/bin/env bash
set -euo pipefail

# --- 4R2 Industrial Defense Suite ---
# Consolidates all audit requirements into a single reportable script.
# Author: AntiGravity / Ricci Yazigi 2026

PAYLOAD="evidence/payload_dim4.json"
mkdir -p evidence

TS="$(date +%Y%m%d_%H%M%S)"
SUMMARY="evidence/audit_summary_${TS}.txt"

echo "=== 4R2 INDUSTRIAL DEFENSE SUITE [PILOT 4♻️2] ===" | tee "$SUMMARY"
echo "Timestamp: $(date -Is)" | tee -a "$SUMMARY"
echo "Project  : systems/basic" | tee -a "$SUMMARY"

# 1. Canonical Payload Initialization
cat > "$PAYLOAD" <<'JSON'
{
  "trace_id": "canon_dim4",
  "normative": [0.85, 0.92, 0.77, 0.81],
  "representational": [0.78, 0.88, 0.70, 0.74],
  "informational": [0.95, 0.91, 0.89, 0.90],
  "physical": [1200, 8, 55, 12]
}
JSON

# --- 1. DETERMINISM ---
echo -e "\n[1/6] TEST: DETERMINISMO DURO (20 iterations)..." | tee -a "$SUMMARY"
DET_OUT="evidence/det_samples_${TS}.txt"
for i in $(seq 1 20); do
  curl -s -X POST http://localhost:8000/api/coherence/measure \
    -H 'Content-Type: application/json' \
    --data-binary "@$PAYLOAD" | grep -o '"C_total":[0-9.]*' | cut -d: -f2 >> "$DET_OUT"
done
UNIQUE_COUNT=$(sort "$DET_OUT" | uniq -c | wc -l | tr -d ' ')
DET_VAL=$(sort "$DET_OUT" | uniq -c)
echo "Unique Values: $UNIQUE_COUNT" | tee -a "$SUMMARY"
echo "Distribution : $DET_VAL" | tee -a "$SUMMARY"

# --- 2. BACKEND/KERNEL PARITY ---
echo -e "\n[2/6] TEST: PARIDAD BACKEND↔KERNEL..." | tee -a "$SUMMARY"
K_RES="evidence/pk_${TS}.json"
B_RES="evidence/pb_${TS}.json"
curl -s -X POST http://localhost:8000/api/coherence/measure -H 'Content-Type: application/json' --data-binary "@$PAYLOAD" > "$K_RES"
curl -s -X POST http://localhost:4000/api/coherence/measure -H 'Content-Type: application/json' --data-binary "@$PAYLOAD" > "$B_RES"
K_VAL=$(grep -o '"C_total":[0-9.]*' "$K_RES" | cut -d: -f2)
B_VAL=$(grep -o '"C_total":[0-9.]*' "$B_RES" | cut -d: -f2)
echo "Kernel (8000) : $K_VAL" | tee -a "$SUMMARY"
echo "Backend (4000): $B_VAL" | tee -a "$SUMMARY"
if [ "$K_VAL" == "$B_VAL" ]; then echo "STATUS: MATCH ✅" | tee -a "$SUMMARY"; else echo "STATUS: MISMATCH ❌" | tee -a "$SUMMARY"; fi

# --- 3. CONCURRENCY ---
echo -e "\n[3/6] TEST: CARGA CONCURRENTE (200 req, P20)..." | tee -a "$SUMMARY"
CODES="evidence/load_codes_${TS}.txt"
seq 1 200 | xargs -n1 -P20 -I{} bash -lc "
  code=\$(curl -s -o /dev/null -w \"%{http_code}\" -X POST http://localhost:4000/api/coherence/measure \
    -H \"Content-Type: application/json\" --data-binary @${PAYLOAD} || echo \"000\")
  echo \"\$code\"
" | tee "$CODES" > /dev/null
ERR_COUNT=$(grep -v '^200$' "$CODES" | wc -l | tr -d ' ')
OK_COUNT=$(grep '^200$' "$CODES" | wc -l | tr -d ' ')
echo "Hits OK: $OK_COUNT" | tee -a "$SUMMARY"
echo "Errors : $ERR_COUNT" | tee -a "$SUMMARY"

# --- 4. LATENCY PROFILING ---
echo -e "\n[4/6] TEST: PERFIL DE LATENCIA (50 req)..." | tee -a "$SUMMARY"
LAT="evidence/latencies_${TS}.txt"
for i in $(seq 1 50); do
  curl -s -o /dev/null -w "%{time_total}\n" -X POST http://localhost:8000/api/coherence/measure -H 'Content-Type: application/json' --data-binary "@$PAYLOAD" >> "$LAT"
done
COUNT=$(wc -l < "$LAT" | tr -d ' ')
P50_IDX=$(( (COUNT + 1) / 2 ))
P95_IDX=$(( (COUNT*95 + 99) / 100 ))
[ "$P50_IDX" -lt 1 ] && P50_IDX=1
[ "$P95_IDX" -lt 1 ] && P95_IDX=1
[ "$P95_IDX" -gt "$COUNT" ] && P95_IDX="$COUNT"
P50=$(sort -n "$LAT" | sed -n "${P50_IDX}p")
P95=$(sort -n "$LAT" | sed -n "${P95_IDX}p")
MAX=$(sort -n "$LAT" | tail -n1)
echo "Latency (p50): $P50 s" | tee -a "$SUMMARY"
echo "Latency (p95): $P95 s" | tee -a "$SUMMARY"
echo "Latency (max): $MAX s" | tee -a "$SUMMARY"

# --- 5. SOAK PROOF ---
echo -e "\n[5/6] TEST: SOAK PROOF (5 iterations, 10s interval)..." | tee -a "$SUMMARY"
SOAK_LOG="evidence/soak_proof_${TS}.jsonl"
for i in $(seq 1 5); do
  ts="$(date -Is)"
  resp=$(curl -sS -X POST http://localhost:8000/api/coherence/measure -H 'Content-Type: application/json' --data-binary "@$PAYLOAD")
  printf '%s\t%s\n' "$ts" "$resp" >> "$SOAK_LOG"
  echo "Iteration $i... OK"
  [ $i -lt 5 ] && sleep 10
done
echo "Logs saved to $SOAK_LOG" | tee -a "$SUMMARY"

# --- 6. NEGATIVE CONTRACT ---
echo -e "\n[6/6] TEST: CONTRATO NEGATIVO (Expected 500s)..." | tee -a "$SUMMARY"
CODE_NEG1=$(curl -s -o /dev/null -w "%{http_code}" -X POST http://localhost:8000/api/coherence/measure -H 'Content-Type: application/json' -d '{"physical":[1,2,3]}')
CODE_NEG2=$(curl -s -o /dev/null -w "%{http_code}" -X POST http://localhost:8000/api/coherence/measure -H 'Content-Type: application/json' -d '{"normative":[1,1,1,1],"informational":[1,1]}')
echo "Mismatch Physical (3 vs 4): $CODE_NEG1" | tee -a "$SUMMARY"
echo "Mismatch Layer (4 vs 2)   : $CODE_NEG2" | tee -a "$SUMMARY"

echo -e "\n=== RESUMEN FINAL DE AUDITORÍA ===" | tee -a "$SUMMARY"
if [ "$UNIQUE_COUNT" -eq 1 ] && [ "$ERR_COUNT" -eq 0 ] && [ "$K_VAL" == "$B_VAL" ]; then
    echo "ESTADO FINAL: VERDE DEFENSIBLE (PASS) 🟢" | tee -a "$SUMMARY"
else
    echo "ESTADO FINAL: REVISIÓN REQUERIDA (FAIL) 🔴" | tee -a "$SUMMARY"
fi
echo "Artifacts preserved in systems/basic/evidence/" | tee -a "$SUMMARY"
