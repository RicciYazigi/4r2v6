#!/usr/bin/env bash
set -euo pipefail

# ARS-20260104-0001: Evidence Traceability Indexer
# This script seals the evidence directory by documenting all artifacts and their hashes.

EVIDENCE_DIR="evidence"
mkdir -p "$EVIDENCE_DIR"

TS="$(date +%Y%m%d_%H%M%S)"
INDEX_FILE="${EVIDENCE_DIR}/evidence_index_${TS}.txt"

{
  echo "=========================================="
  echo "  4R2 PILOT: EVIDENCE TRACEABILITY INDEX"
  echo "=========================================="
  echo "TRACE_ID   : ARS-20260104-0001"
  echo "CREATED_UTC: $(date -u -Is)"
  echo "PROJECT    : systems/basic"
  echo "DEPLOY_ID  : basic_1240421_pilot"
  echo "------------------------------------------"
  echo
  echo "[SECTION 1: FILE LISTING]"
  ls -la "$EVIDENCE_DIR" | grep '^-'
  echo
  echo "[SECTION 2: SHA256 HASHES]"
  (cd "$EVIDENCE_DIR" && sha256sum * 2>/dev/null | grep -v "evidence_index_" | sort) 
  echo
  echo "[SECTION 3: SYSTEM SNAPSHOT]"
  docker inspect -f '{{.Name}} RestartCount={{.RestartCount}} OOMKilled={{.State.OOMKilled}}' \
    basic-frontend-1 basic-backend-1 basic-kernel-1 2>/dev/null || echo "Docker containers not accessible via name (using basic prefix)"
  echo "------------------------------------------"
  echo "END OF INDEX"
} > "$INDEX_FILE"

echo "Evidence sealed: $INDEX_FILE"
