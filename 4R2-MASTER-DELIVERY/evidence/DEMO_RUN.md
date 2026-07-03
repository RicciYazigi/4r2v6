# DEMO RUN: "The Hammer" (Canon v1.0)
**Trace ID**: RICCI-LOCK-20260116

Este documento detalla el procedimiento para generar evidencia técnica inmutable y verificable.

## Pasos para ejecutar la Demo
1. **Iniciar el motor**:
   ```bash
   python systems/basic/packages/kernel/api_fastapi.py
   ```
2. **Lanzar la petición de coherencia**:
   Se puede usar el script de PowerShell proporcionado en `smoke_test.ps1` o ejecutar:
   ```powershell
   $req = Get-Content -Raw evidence/request.json
   Invoke-RestMethod -Uri "http://localhost:8000/api/coherence/measure" -Method Post -Body $req -ContentType "application/json"
   ```

## Artefactos Generados
- **request.json**: Entrada enviada al motor (vectores de las 4 capas).
- **response.json**: Salida del motor (C_total, landauer_cost, etc.).
- **HASH.txt**: Identificador SHA256 para asegurar que la evidencia no ha sido manipulada.

## Verificación de Consistencia
Al ejecutar la demo dos veces con el mismo `trace_id` y `inputs`, los resultados de coherencia serán idénticos. Solo el `timestamp` variará, lo cual es el comportamiento esperado para la trazabilidad temporal.

---
*Locked by Antigravity AI*
