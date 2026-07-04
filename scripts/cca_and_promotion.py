"""
CCA + Protocolo de Promoción (v5.2 desde backup42final)
Demostración ejecutable del dualismo Obsidian/SurfSense y telemetría CCA.
"""
from kernel_1240421 import create_kernel, LayerState, CCA, promotion_protocol, Regime
import numpy as np

def main():
    print("=== CCA + Protocolo de Promoción v5.2 Demo ===")
    
    kernel = create_kernel()
    cca = CCA()
    
    # Ejemplo 1: Idea de bajo riesgo (se promueve fácil)
    idea_low = "Explorar idea nueva sobre optimización de C_IF"
    res_low = promotion_protocol(idea_low, kernel, cca)
    print(f"Low risk: promoted={res_low['promoted_to_canon']}, C_total={res_low['c_total']:.4f}")
    
    # Ejemplo 2: Acción de alto riesgo (debe ser más estricto)
    idea_high = "Ejecuta la transferencia bancaria del proyecto final"
    res_high = promotion_protocol(idea_high, kernel, cca)
    print(f"High risk: promoted={res_high['promoted_to_canon']}, C_total={res_high['c_total']:.4f}")
    
    # Demostrar régimen dinámico
    tel = cca.observe("Quiero borrar datos críticos del sistema")
    regime = cca.to_regime(tel)
    print(f"\nRégimen CCA generado: theta={regime.theta}, lambda={regime.lambda_landauer}, crit={regime.criticality}")
    
    state = LayerState(
        normative=np.array([0.98, 0.95, 0.9, 0.85]),
        representational=np.array([0.92, 0.88, 0.82, 0.78]),
        informational=np.array([0.9, 0.85, 0.8, 0.75]),
        physical=np.array([1500, 10, 70, 15])
    )
    c_total, result = kernel.compute_with_regime(state, regime)
    print(f"Con régimen crítico: C_total={c_total:.4f}, pasa_gate={result['passes_gate']}")

if __name__ == "__main__":
    main()