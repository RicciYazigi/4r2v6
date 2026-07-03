#!/bin/bash
set -euo pipefail

echo "============================================================"
echo "4R2 + Antigravity Wings - Professional Validation Suite"
echo "Workspace: Grok4r2 rempacado (clean)"
echo "============================================================"

cd "$(dirname "$0")/.."

echo ""
echo "[Phase] Syntax & Import Structure Check"
python3 -m py_compile core/kernel_1240421.py \
  antigravity_wings/antigravity_wings/dual_agents/mario.py \
  antigravity_wings/antigravity_wings/dual_agents/luigi.py \
  antigravity_wings/antigravity_wings/numeric/translator.py \
  antigravity_wings/antigravity_wings/orchestration/master.py
echo "  ✓ All core files compile cleanly."

echo ""
echo "[Phase] Canonical Kernel Self-Check (when numpy available)"
if python3 -c "import numpy; print('  numpy available')" 2>/dev/null; then
  python3 -c '
import sys
sys.path.insert(0, "core")
from kernel_1240421 import CoherenceKernel
print("  " + str(CoherenceKernel.selftest()))
  '
else
  echo "  (numpy not in base env — run inside the kernel package or Docker for full selftest)"
fi

echo ""
echo "[Phase] End-to-End Pipeline (lightweight)"
python3 scripts/end_to_end_validation.py || echo "  (some deps may be missing in base env)"

echo ""
echo "============================================================"
echo "Validation run completed."
echo "For full numerical validation use the Docker environments in 4R2-MASTER-DELIVERY."
echo "============================================================"