#!/usr/bin/env bash
set -euo pipefail

GUARDIAN_HOME="${HOME}/.guardian"
PREFLIGHT_DIR="${GUARDIAN_HOME}/preflight"
TS="$(date -u +%Y%m%d_%H%M%S)"
MANIFEST="${PREFLIGHT_DIR}/manifest_${TS}.json"
PROJECT_ROOT="$(pwd)"

FILES=(
  "docker-compose.yml"
  "server/systems/kernel_1240421.py"
  "server/systems/api_fastapi.py"
)

MIN_MEM_GB=2
MIN_DISK_GB=10

mkdir -p "$PREFLIGHT_DIR"

fail() { echo "FAIL: $1" >&2; exit 2; }
warn() { echo "WARN: $1" >&2; exit 1; }

# 0) Guardian Gate (Soft-Fail para piloto)
if [[ -x "${GUARDIAN_HOME}/guardian.sh" ]]; then
  if ! "${GUARDIAN_HOME}/guardian.sh" check >/dev/null 2>&1; then
    fail "Guardian detectado pero no está ACTIVE"
  else
    GUARDIAN_STATUS="ACTIVE"
  fi
else
  GUARDIAN_STATUS="MISSING"
  echo "INFO: Guardian no detectado. Operando en modo standalone."
fi

# 1) Hashes (integridad)
declare -A hashes
for f in "${FILES[@]}"; do
  [[ ! -f "${PROJECT_ROOT}/${f}" ]] && fail "Archivo crítico faltante: ${f}"
  hashes["$f"]="$(sha256sum "${PROJECT_ROOT}/${f}" | awk '{print $1}')"
done

# 2) Recursos (nativo bash)
MEM_FREE_KB="$(awk '/MemAvailable/ {print $2}' /proc/meminfo)"
MEM_FREE_GB_INT=$(( MEM_FREE_KB / 1024 / 1024 ))

DISK_FREE_GB_RAW="$(df -B1G "${PROJECT_ROOT}" | awk 'NR==2 {print $4}')"
DISK_FREE_GB_INT="$(echo "$DISK_FREE_GB_RAW" | tr -d 'G')"

(( MEM_FREE_GB_INT < MIN_MEM_GB )) && warn "Memoria insuficiente: ~${MEM_FREE_GB_INT}GB (min ${MIN_MEM_GB}GB)"
(( DISK_FREE_GB_INT < MIN_DISK_GB )) && warn "Disco insuficiente: ${DISK_FREE_GB_INT}GB (min ${MIN_DISK_GB}GB)"

# 3) Manifest (orden estable)
{
  echo "{"
  echo "  \"timestamp\": \"$(date -u +%FT%TZ)\","
  echo "  \"project_root\": \"${PROJECT_ROOT}\","
  echo "  \"guardian_status\": \"${GUARDIAN_STATUS}\","
  echo "  \"files\": {"
  for f in "${FILES[@]}"; do
    echo "    \"$f\": \"${hashes[$f]}\","
  done | sed '$ s/,$//'
  echo "  },"
  echo "  \"resources\": {"
  echo "    \"mem_free_gb_approx\": ${MEM_FREE_GB_INT},"
  echo "    \"disk_free_gb\": ${DISK_FREE_GB_INT}"
  echo "  }"
  echo "}"
} > "$MANIFEST"

echo "PREFLIGHT OK (Gate: ${GUARDIAN_STATUS}) → $MANIFEST"
exit 0
