"""
Notas de Ciencia de Alto Valor - Reforzadas desde Brain_Artifacts/Auditoria_Forense_v4.1.md y Brutal_V40.md

Fundamento:
- Landauer: E = k_B * T * ln(2) por bit borrado irreversible.
- Aplicación en 4R2: Prevenir el coste midiendo CCE antes de la decisión.
- Papers 2026:
  * Paccou: Barrera térmica real de 10^36 a 10^40 FLOPs para computación masiva.
  * Whitelam (GTC): Denoising físico permite latencias bajas sin esperar convergencia total.
- Pesos NRIF: N=6, R=8, I=12, **F=16** (prioridad física para "Stillness").
- Factor 42: 1²+2²+4²+0²+4²+2²+1² = 42 como huella digital inmutable.

C_total y Landauer impact:
- Elevar w_IF hace que C_total sea más sensible a desalineación física → triggers más tempranos de Stillness.
- Landauer se mantiene aditivo en la loss, pero el régimen dinámico (CCA) lo ajusta según irreversibilidad.
"""
print("Notas de ciencia v5.2 cargadas. Ver backup para referencias completas.")