# Diseño de Pilotos Operativos - Antigravity Wings v1.0

Este documento define la arquitectura de integración para 3 pilotos reales, demostrando la versatilidad del exoesqueleto sin comprometer la propiedad intelectual del Motor.

## Objetivo
Demostrar la capacidad de "Black Box Hosting" en sectores regulados.

---

## 1. Piloto Banca: "Transaction Guardian"

**Escenario:** Aprobación de transferencias SWIFT internacionales de alto valor (> $50k).
**Reto:** Latencia baja (< 200ms), cero falsos positivos en bloqueo (STOP).

### Configuración del Exoesqueleto

- **DataSource:** flujos JSON de pasarela de pagos.
- **Circuit Breaker:** Agresivo. `timeout=150ms`. Si el Motor tarda, fallback a `DEGRADE` (revisión humana posterior) para no bloquear dinero legítimo.
- **Fusibles (FuseSpecs):**
  - **Hard Stop:** Si `destination_country` está en lista negra OFAC.
  - **Soft Warn:** Si `amount > avg_history * 3`.
- **Agentes Duales:**
  - **Luz:** Busca consistencia en patrones de gasto histórico.
  - **Sombra:** Busca anomalías de geolocalización o "smurfing" (muchos pagos pequeños previos).

**Resultado esperado:**
- Reducción del 40% en falsos positivos de fraude.
- Auditoría firmada de por qué se aprobó cada transacción grande.

### Integración Técnica
```python
# Pseudo-código de launcher
export MOTOR_CLASS=FraudDetectionModel
export AGW_ENV=prod_bank
export CIRCUIT_TIMEOUT=0.15
```

---

## 2. Piloto Seguros: "Claims Fast-Track"

**Escenario:** Siniestros de Auto (fotos de choque + reporte PDF).
**Reto:** Proceso asíncrono, evidencia multimedia, consistencia narrativa.

### Configuración del Exoesqueleto

- **DataSource:** API REST que recibe URLs de imágenes y texto OCR.
- **Notebook Bridge:** CRÍTICO. Genera un resumen narrativo cruzando la versión del conductor vs. el reporte policial (OCR).
- **Circuit Breaker:** Relajado (`timeout=30s`).
- **Fusibles:**
  - **Hard Stop:** Si la póliza está vencida (regla determinista externa al motor).
  - **Escalate:** Si el daño estimado > valor del auto (pérdida total).
- **Agentes Duales:**
  - **Luz:** Valida que la descripción coincida con los daños visuales.
  - **Sombra:** Busca metadatos de fotos inconsistentes (fecha/hora) o fotos reutilizadas de internet.

**Resultado esperado:**
- Aprobación automática ("Fast Track") del 60% de reclamos simples en < 5 min.
- Evidence Package listo para juicio si hay disputa.

---

## 3. Piloto Salud: "Remote Triage Assistant"

**Escenario:** Pre-diagnóstico en telemedicina (chat + constantes vitales).
**Reto:** Privacidad absoluta (HIPAA/GDPR), riesgo de vida.

### Configuración del Exoesqueleto

- **Privacidad:**
  - `DataSource` anonimiza PII antes de que entre al pipeline (scrubbing de nombres).
  - `ClientProfile` usa hashes de pacientes, nunca nombres reales.
- **Motor:** Modelo de clasificación de urgencia (1-5).
- **Circuit Breaker:** Redundante. Si falla, fallback inmediato a "Llamar a Humano".
- **Fusibles:**
  - **Hard Stop:** Si hay palabras clave de emergencia ("infarto", "no respira", "sangrado masivo"). El exoesqueleto fuerza `ESCALATE` (llamar ambulancia) sin consultar al Motor.
  - **Soft Warn:** Si faltan datos vitales (presión, temperatura).
- **Agentes Duales:**
  - **Luz:** Resume síntomas para el médico.
  - **Sombra:** Busca contraindicaciones medicamentosas en el historial (si está disponible).

**Resultado esperado:**
- "Second Opinion" segura para enfermeros de triaje.
- Trazabilidad legal de por qué se asignó tal prioridad.

---

## Próximos Pasos (Roadmap de Implementación)

1. Crear carpetas `pilots/bank`, `pilots/insurance`, `pilots/health`.
2. Crear `mock_data` para cada uno.
3. Configurar 3 `launcher.py` distintos con variables de entorno específicas.
