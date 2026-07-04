#!/usr/bin/env bash
set -euo pipefail

echo ">>> INICIANDO SECUENCIA DE DESPLIEGUE [PILOTO 4♻️2] <<<"

echo "→ [1/3] Ejecutando Preflight Check..."
./security/scripts/preflight.sh

echo "→ [2/3] Levantando contenedores..."
docker compose up --build -d

echo "→ [3/3] Esperando estabilización (5s)..."
sleep 5
./security/scripts/health.sh

echo "DEPLOY COMPLETADO CON ÉXITO."
