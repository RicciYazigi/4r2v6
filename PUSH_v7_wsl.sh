#!/usr/bin/env bash
# ============================================================================
# 4R2 v7.0.0 — PUSH ÚNICO desde WSL (Richie). Copia/pega este bloque completo.
# El sandbox no puede escribir en .git (permisos del mount); por eso lo corres tú.
# Commits locales libres; el push a remoto lo haces con este script.
# ============================================================================
set -e
cd "/mnt/c/Users/USER/Documents/4R2 repo maestro jul2026"

# 0) Limpiar lock huérfano que pudo dejar el sandbox
rm -f .git/index.lock

# 1) Entorno + verificación local completa (todo debe salir 0)
python3 -m venv .venv 2>/dev/null || true
source .venv/bin/activate 2>/dev/null || true
pip install -e ".[service,dev]" -q
python -m pytest -q                                   # 102 passed
python scripts/check_release_coherence.py             # RELEASE COHERENCE: PASS
make parity                                           # 1
make determinism                                      # PASS
python scripts/eval_e1_e4.py   | grep '"veto_accuracy_kernel_LBB": 1.0'
python scripts/eval_e2_e3.py   | grep '"incidents_grave_or_adv_ALLOW": 0'
python benchmarks/public_benchmark.py                 # acceptability 1.0
python scripts/frontier_calibrate.py >/dev/null                    # regenera config no-degenerado
python -c "import json;h=json.load(open('evidence/frontier_v7_config.json'))['h'];assert h['a']>0.05 and h['b']>0.05 and h['g']<0.05,h;print('config both-axes OK:',{k:round(v,3) for k,v in h.items() if isinstance(v,(int,float))})"
python self_test.py                                   # SELF-TEST: OK (exit 0)
python scripts/generate_evidence_index.py --evidence-dir evidence --output evidence_index.json
python examples/quickstart.py                         # ALLOW / FLAG / BLOCK
sha256sum evidence/*.json                             # comparar con FRONTIER_REPORT §7

# 2) Rama de trabajo (todo el v7 vive aquí; main queda intacto hasta tu PR)
git checkout v7-frontier-wip 2>/dev/null || git checkout -b v7-frontier-wip

# 3) Stage de TODO (add -A; .gitignore excluye .venv, __pycache__, *.egg-info)
git add -A

# 4) Commit único de todo el ciclo v7 (Frontier + capa de producto)
git commit -m "release: v7.0.0 — Frontier defenses + product layer (SDK+sidecar+coherence+benchmark); kernel math frozen at 6.1.0

FRONTIER (opt-in core/frontier_v7.py; kernel v6.1.0 congelado):
- H(x) breach-energy score calibrado por Fisher en AMBOS ejes (a≈b, g→0); generaliza el LBB
- JS camouflage + Shannon OOD; control Fisher-vs-angular (KEEP angular)
- detector de negacion endurecido cableado a produccion (eval_e2_e3.verifiability)
- 2 vulnerabilidades simetricas cazadas y cerradas: (1-C_IF) [ADR-0008] y hueco eje C_RI
- camuflaje 100%->55% simetrico N-R y R-I; FPR alta-ver 0.0; negacion 93.3%->0%

PRODUCTO (four_r2/; kernel math intacto):
- SDK Guardrail fail-closed (nunca lanza), HashingEmbedder determinista, calibrate_theta, MetricsRegistry
- sidecar FastAPI (/health /v1/evaluate /metrics + X-API-Key); Dockerfile.sidecar + compose
- VER grounding fuse (F[0]<0.15) cierra verifiability-inflation
- benchmark held-out reproducible (acceptability 1.0, theta* 0.3971), SHA-256 encadenado
- check_release_coherence (una sola historia de version); pyproject 4.0.0->7.0.0 + extras
- docs: LIMITATIONS, THREAT_MODEL, VERSIONING_POLICY, INTEGRATION, DATA_ROOM_CHECKLIST, MIGRATION, arXiv v7, ADR-0008

AUDIT FIX (ciclo 10): frontier_v7_config.json estaba degenerado (a=0, ciego al eje N-R) por\ncalibrar sobre E2 puro; corregido -> pesos ambos ejes (a=0.499 b=0.501 g=0) + threshold E2 (0.453),\ndegeneracy_check PASS, 3 tests de integridad que corren el pipeline REAL y atan el artefacto sellado.\nRaiz organizada (docs historicos a archive/docs_legacy/).\n\nVERIFICADO: 102/102 tests (65 core + 22 SDK + 15 frontier), coherence PASS, parity 1,
determinism PASS, benchmark acceptability 1.0, self-test exit 0, evidence_index 11 artefactos.
Docker build ND en sandbox (verificar en host)."

# 5) Tag de release
git tag v7.0.0 2>/dev/null || echo "tag v7.0.0 ya existe (omito)"

# 6) (Opcional) Docker real en host — única pieza ND en el sandbox
# docker compose -f docker-compose.sidecar.yml up -d && curl -s localhost:8472/health

# 7) Push de la rama + el tag
git push -u origin v7-frontier-wip
git push origin v7.0.0
echo "== PUSH COMPLETO. Abre el PR v7-frontier-wip -> main tras tu revisión. =="
