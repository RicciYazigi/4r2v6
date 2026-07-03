# TEST_MATRIX.md — Reconciliación de Test Suites

## Objetivo

Este documento mapea las diferentes suites de tests mencionadas en el proyecto:

- **22/22 tests** (Motor Kernel): tests unitarios del kernel Python 1240421
- **42/42 tests** (Sistema completo): tests de integración (Kernel + Backend + Frontend)

---

## Suite 1: Kernel Unit Tests (22/22)

**Ubicación**: `tests/test_kernel_1240421.py` (en repo del Motor, NO en este exoesqueleto)

**Comando**:
```bash
pytest tests/test_kernel_1240421.py -v
```

**Alcance**:
- Tests unitarios del kernel Python
- Validación de métricas de coherencia
- Pruebas de Landauer loss
- Validación matemática de 4R2 components

**Estado**: ✅ 22/22 passing (según IMPLEMENTATION_SUMMARY.md)

---

## Suite 2: Sistema Completo (42/42)

**Ubicación**: Distribuida (Motor + Gateway + Backend)

**Alcance**:
- Endpoints FastAPI (`/api/coherence/measure`, `/api/coherence/landauer`, `/api/coherence/loss-4r2`)
- Backend Node.js + DB (MySQL/Drizzle)
- Frontend integration
- Full pipeline tests

**Estado**: ✅ 42/42 passing (según COMPLETE_SPEC.md)

---

## Suite 3: Exoesqueleto Unit & Contract Tests

**Ubicación**: `tests/`

**Comando**:
```bash
python -m pytest tests/ -v
```

**Cobertura**:
- `test_contracts.py`: Validación de Dataclasses y tipos API.
- `test_api_basic.py`: Contratos de endpoints FastAPI.
- `test_resilience_hardened.py`: Circuit Breaker y Guardrails.
- `test_runtime_operator.py`: Ejecución dual y lógica de fusibles.
- `test_smoke.py`: Carga de paquetes y pipeline demo.

**Estado**: ✅ Todos los tests pasando (Audit-Grade).

---

## Matriz de Responsabilidades

| Suite | Qué valida | Repo | Estado |
|-------|-----------|------|--------|
| Kernel 22/22 | Fórmulas y métricas 4R2 | Motor privado | ✅ PASS |
| Sistema 42/42 | End-to-end (API + DB) | Monorepo | ✅ PASS |
| Exoesqueleto | Integridad + Auditoría | `antigravity_wings/` | ✅ CERTIFICADO |

---

## Verificación de Integridad

El estado canónico de estos tests está sellado en el [CANON_MANIFEST.json](CANON_MANIFEST.json). Todo cambio requiere actualización del hash y aprobación dual.
