#!/usr/bin/env bash
set -euo pipefail

ENDPOINTS=(
  "http://localhost:3000/health"
  "http://localhost:8000/health"
)

echo "Health Check Status:"
ALL_OK=true

for url in "${ENDPOINTS[@]}"; do
  code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 2 "$url" || echo "ERR")
  if [[ "$code" == "200" ]]; then
    echo "  OK   $url"
  else
    echo "  FAIL $url (Código: $code)"
    ALL_OK=false
  fi
done

if [[ "$ALL_OK" == true ]]; then
  echo "SYSTEM HEALTH: GREEN"
  exit 0
else
  echo "SYSTEM HEALTH: RED"
  exit 1
fi
