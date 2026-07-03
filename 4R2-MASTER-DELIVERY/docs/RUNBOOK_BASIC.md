# RUNBOOK_BASIC - Red Bull Wings / 4R2 Motor

Este manual detalla los pasos para poner en marcha el Motor 4R2.

## Pre-requisitos
- Python 3.9+
- Docker & Docker Compose (Recomendado)

## Opción A: Ejecución vía Docker (Producción)
1.  Navegar a: `systems/enhanced/`
2.  Ejecutar:
    ```bash
    docker-compose up --build -d
    ```
3.  Verificar que el servicio `kernel` esté arriba en el puerto `8000`.

## Opción B: Ejecución Standalone (Desarrollo/Pruebas)
1.  Navegar a: `systems/enhanced/packages/kernel`
2.  Instalar dependencias:
    ```bash
    pip install -r requirements.txt
    ```
3.  Lanzar el API:
    ```bash
    python api_fastapi.py
    ```

## Verificación de Ejecución
Ejecutar el siguiente comando para comprobar que el motor responde correctamente:

```bash
curl -X POST http://localhost:8000/api/coherence/measure \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer test-token" \
     -d '{
       "normative": [1.0, 0.0, 0.5],
       "representational": [1.0, 0.0, 0.5],
       "informational": [1.0, 0.0, 0.5],
       "physical": [100.0, 4.0, 10.0, 5.0]
     }'
```

**Resultado esperado (C_total near 0)**:
```json
{
  "C_NR": 0.0,
  "C_RI": 0.0,
  "C_IF": ...,
  "C_total": ...,
  "timestamp": "..."
}
```

---
**Nota**: El motor está diseñado para ser agnóstico al dominio. Los pesos por defecto son equitativos (1/3) para cada capa de coherencia.
