# 4♻️2 COHERENCE ENGINE

## EJECUTAR SISTEMA

```bash
./EJECUTAR_AHORA.sh
```

Selecciona opción y abre http://localhost:5173

## CONTENIDO

### Sistemas (2)
- **basic/** - Demo rápida (recomendado para empezar)
- **enhanced/** - Producción con Safety Monitor

### Tests
- **tests/** - 24 tests del kernel
- Ejecutar: `cd tests && ./run_all_tests.sh`

### Evidencia
- **evidence/** - Fuzzing N=2000
- 35.7% token savings validado
- 0% false positives

### Demos
- **demos/** - Scripts Python ejecutables

## VALIDACIÓN

Tu kernel_1240421.py está en:
- `systems/basic/packages/kernel/kernel_1240421.py`
- `systems/enhanced/packages/kernel/kernel_1240421.py`

Ambos idénticos, 349 líneas, 100% preservado.

## DETENER

```bash
cd systems/basic  # o enhanced
docker-compose down
```
