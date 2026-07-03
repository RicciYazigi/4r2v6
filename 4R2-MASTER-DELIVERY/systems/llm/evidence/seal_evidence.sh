#!/bin/bash
# 4R2 LLM Evidence Sealer - Audit-Grade
TRACE_ID=$1

if [ -z "$TRACE_ID" ]; then
    echo "Usage: ./seal_evidence.sh <trace_id>"
    exit 1
fi

EVIDENCE_DIR="."
INDEX_FILE="evidence_index_$(date +%Y%m%d_%H%M%S).txt"

echo "🛡️ Sealing Evidence for Trace: ${TRACE_ID}"
echo "------------------------------------------" > "$INDEX_FILE"
echo "4R2 LLM AUDIT INDEX - $(date)" >> "$INDEX_FILE"
echo "TRACE: ${TRACE_ID}" >> "$INDEX_FILE"
echo "------------------------------------------" >> "$INDEX_FILE"

# 1. JSONL Logs
JSONL_FILE="${EVIDENCE_DIR}/${TRACE_ID}.jsonl"
if [ -f "$JSONL_FILE" ]; then
    SHA=$(sha256sum "$JSONL_FILE" | cut -d' ' -f1)
    SIZE=$(du -h "$JSONL_FILE" | cut -f1)
    echo "[LOGS] ${TRACE_ID}.jsonl | SHA-256: ${SHA} | Size: ${SIZE}" >> "$INDEX_FILE"
else
    echo "[ERROR] JSONL file not found" >> "$INDEX_FILE"
fi

# 2. Database Snapshot
DB_FILE="./db-bridge/storage/runs.db"
if [ -f "$DB_FILE" ]; then
    SHA=$(sha256sum "$DB_FILE" | cut -d' ' -f1)
    echo "[DB] runs.db | SHA-256: ${SHA}" >> "$INDEX_FILE"
fi

# 3. Infrastructure State
echo "[OPS] Docker State:" >> "$INDEX_FILE"
docker compose ps >> "$INDEX_FILE"

echo "✅ Registry Sealed: ${INDEX_FILE}"
cat "$INDEX_FILE"
