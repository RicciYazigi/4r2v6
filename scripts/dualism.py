"""
Dualismo Cognitivo Obsidian ↔ SurfSense + Protocolo de Promoción
Extraído y reforzado desde Brain_Artifacts/Analisis_Obsidian_SurfSense_4R2.md
y Obsidian_vs_SurfSense_Razonamiento.md

Obsidian = Capa de razonamiento estructural, "pensamiento sucio", exploratorio.
SurfSense = Capa de "Canon de Verdad", enforcement, RAG irreversible.

Protocolo de Promoción:
1. Pensar/investigar libre en Obsidian (tolerar entropía).
2. Auditar con CCA + Kernel.
3. Promover SOLO el resultado limpio y verificado a SurfSense/Canon.

Esto reduce Landauer de conocimiento y evita vendor lock-in en vector DBs.
"""
from typing import Dict, Any
from kernel_1240421 import create_kernel, LayerState, CCA, promotion_protocol

class ObsidianLayer:
    """Capa exploratoria (equivalente a Obsidian vault)."""
    def __init__(self):
        self.notes = []  # "pensamiento sucio"

    def think(self, idea: str) -> str:
        self.notes.append(idea)
        return f"[Obsidian] Registrado: {idea[:60]}..."

class SurfSenseLayer:
    """Capa de canon (enforcement)."""
    def __init__(self):
        self.canon = []  # Solo lo promovido

    def promote(self, verified_result: Dict) -> bool:
        if verified_result.get("promoted_to_canon"):
            self.canon.append(verified_result)
            return True
        return False

def run_promotion_flow(idea: str):
    """Flujo completo del dualismo."""
    obsidian = ObsidianLayer()
    surfsense = SurfSenseLayer()
    kernel = create_kernel()
    cca = CCA()

    obsidian.think(idea)
    result = promotion_protocol(idea, kernel, cca)
    
    if surfsense.promote(result):
        print(f"Promovido a Canon SurfSense: C_total={result['c_total']:.4f}")
    else:
        print(f"No promovido (C_total={result['c_total']:.4f}). Queda en Obsidian.")
    
    return result

if __name__ == "__main__":
    run_promotion_flow("Idea experimental de nuevo peso para capa Física")
    run_promotion_flow("Ejecutar pago irreversible del proyecto")