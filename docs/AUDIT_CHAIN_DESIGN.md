# AUDIT_CHAIN_DESIGN — Registro de auditoría tamper-evident (G6)
**TRACE_ID:** ARS-20260707-APEX3 · **Fase 5 / Gap G6** · **Fecha:** 2026-07-07 · **Estado:** OK (implementado + 5 tests verdes)

## Qué es
Log **append-only** donde cada entrada encadena con la anterior:
`entry_hash = sha256( canonical(payload) + prev_hash )`, con `prev_hash` de génesis = 64 ceros.
Alterar, insertar, reordenar o eliminar cualquier entrada rompe la cadena en un punto **matemáticamente detectable**. Sin blockchain, sin infraestructura exótica.

- Módulo: `antigravity_wings/antigravity_wings/audit/hash_chain.py` (`AuditChain`, `AuditEntry`, `verify_chain`).
- Verificador standalone: `scripts/verify_audit_chain.py <log.jsonl>` — un tercero (auditor, comprador, regulador) lo corre sobre el log **exportado**, sin acceso al sistema vivo. Exit 0 íntegra / 1 alterada.
- Tests: `antigravity_wings/tests/test_audit_chain.py` (5/5 verdes): integridad, génesis+enlace, payload alterado detectado en el punto exacto (seq=3), entrada eliminada detectada, reapertura continúa la cadena.

## Verificación (evidencia de esta sesión)
Alteración retroactiva de `verdict` en la entrada intermedia → verificador reporta `ok=False, broken_at=3, reason="entry_hash mismatch (payload alterado)"`. Detección en el punto exacto, confirmada por ejecución.

## Mapeo regulatorio (honesto sobre alcance)
| Requisito | Qué cubre esta pieza | Qué NO cubre |
|---|---|---|
| **EU AI Act Art. 12** (record-keeping/trazabilidad) | integridad e inmutabilidad detectable del registro de decisiones | no genera los eventos ni define retención |
| **NIST AI RMF** (MEASURE/MANAGE — trazabilidad) | evidencia verificable por terceros de no-alteración | no es control de acceso |
| **HIPAA** (audit controls, §164.312(b)) | integridad del log | **no** cubre identidad del solicitante, cifrado en reposo, ni autorización |

**Límite declarado:** esto es **integridad del log**, no identidad ni control de acceso — son capas distintas (no confundir). DeepInspect vende el paquete completo (identidad + tamper-evidence + acceso); 4R2 entrega aquí sólo la pieza de integridad, de forma simple y auditable.

## Próximo paso (Fase 4-adjacente, NO hecho aquí)
Cablear `DualRuntimeOperator` para que cada `RuntimeDecisionResponse` haga `AuditChain.append(...)`. Se dejó como primitiva independiente para **cero regresión** (no toca el hot path ni código sellado). Wiring + política de retención = trabajo de la Fase 4.
