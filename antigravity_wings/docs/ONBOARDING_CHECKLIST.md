# ONBOARDING_CHECKLIST.md — Nuevo Cliente

Esta checklist guía el proceso de alta de un nuevo cliente en el exoesqueleto `antigravity_wings`.

---

## Fase 1: Configuración de Entorno
- [ ] Definir `client_id` (ej. `bank_omega`).
- [ ] Crear directorio base en `runtime_data/sessions/bank_omega` (opcional, el sistema lo crea).
- [ ] Generar API Key específica para el cliente o usar la global por ahora.

## Fase 2: Observación (DataSources)
- [ ] Identificar fuentes de datos (Logs, APIs de Riesgo, DBs).
- [ ] Implementar clases `DataSource` personalizadas si es necesario.
- [ ] Registrar las fuentes en el configurador del orquestador.

## Fase 3: Perfilado Inicial (Modo Cold)
- [ ] Ejecutar una llamada de prueba para generar el primer `ClientProfile`.
- [ ] Verificar que la **Tomografía** (grafo estructural) sea correcta.
- [ ] Revisar reportes de **Luz/Sombra** iniciales para detectar sesgos obvios.

## Fase 4: Configuración de Fusibles (FuseSpecs)
- [ ] Ajustar umbrales en `FuseConfigGenerator` para el nuevo cliente.
- [ ] Definir qué componentes son críticos (decisión STOP) vs informativos.

## Fase 5: Conexión con el Motor
- [ ] Verificar que el Motor (Black Box) soporte las features del nuevo cliente.
- [ ] Ajustar los **Guardrails** (rangos válidos de features).
- [ ] Configurar el **Circuit Breaker** (latencia máxima aceptable para este cliente).
**NOTA HISTÓRICA / ACTUALIZADO 2026-06-23**: Default real (LocalCanonical desde core/ o RealMotor). Mock solo tests aislados. Ver CANON_SPEC y kernel.

## Fase 6: Validación en Cockpit
- [ ] Realizar una petición a `POST /analyze/{client_id}`.
- [ ] Verificar que aparezca en la tabla de **Sesiones Activas**.
- [ ] Comprobar que la latencia del paso `motor` sea estable.

## Fase 7: Cierre de Seguridad
- [ ] Verificar la integridad de la evidencia cargando el `HASH.txt` de la sesión.
- [ ] Asegurar que el `trace_id` se propaga correctamente a los logs del cliente.

---

**Resultado final**: El cliente está operativo, auditable y protegido por el exoesqueleto.
