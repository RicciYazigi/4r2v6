# RUNBOOK: PILOT 4R2 MOTOR (Canon v1.0)

Este documento detalla los pasos para ejecutar y verificar el motor de coherencia 4R2 en un entorno limpio.

## 1. Precondiciones
- **Python**: 3.9+ (Recomendado 3.10)
- **Dependencias**: `fastapi`, `uvicorn`, `pydantic`, `numpy`
- **Variables de Entorno**: (Ninguna requerida para modo básico)

## 2. Instalación
Desde la raíz del repositorio (`4R2-MASTER-DELIVERY`):
```bash
pip install -r systems/basic/packages/kernel/requirements.txt
```

## 3. Inicio del Servidor
Ejecutar el siguiente comando para iniciar la API de coherencia:
```bash
python systems/basic/packages/kernel/api_fastapi.py
```
El servidor estará disponible en `http://localhost:8000`.

## 4. Verificación (Healthcheck)
```bash
curl http://localhost:8000/health
```
**Resultado esperado**: `{"status": "healthy"}`

## 5. Ejecución de Pruebas
Para ejecutar las pruebas unitarias del núcleo:
```bash
pytest tests/
```
**Resultado esperado**: Todos los tests en verde (PASSED).

## 6. Resolución de Fallos
- **Error `ModuleNotFoundError: No module named 'src'`**: Asegúrate de estar en el directorio `systems/basic/packages/kernel/` o añadirlo al `PYTHONPATH`.
- **Puerto 8000 ocupado**: Cambia el puerto en `api_fastapi.py` o usa la bandera `--port`.

---
*Generated for Ricci-Lock-20260116*
