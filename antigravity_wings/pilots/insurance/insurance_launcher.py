# pilots/insurance/launcher.py

"""
Launcher específico para el Piloto de Seguros.
Configura el entorno para 'Claims Fast-Track'.
"""

import os
import uvicorn
from pathlib import Path

# 1. Configurar Variables de Entorno para este Piloto
os.environ["AGW_ENV"] = "pilot_insurance"
os.environ["AGW_RUNTIME_ROOT"] = "./runtime_insurance"
os.environ["AGW_API_KEY"] = "ins_pilot_secret_123"
os.environ["SYSTEM_STATUS_FILE"] = "insurance_status.json"

# BRUTAL REAL MODE: Force real path.
# Use the main AGW orchestrator with LocalCanonical real kernel.
# No mocks in default execution.
current_dir = Path(__file__).resolve().parent
os.environ.pop("MOTOR_PATH", None)  # remove any mock
os.environ["USE_REAL_MOTOR"] = "1"
print("[BRUTAL] Insurance pilot configured for real motor path (LocalCanonical)")

# Configurar Circuit Breaker relajado para Seguros (imágenes pesadas)
os.environ["AGW_CB_TIMEOUT"] = "30.0" 

def main():
    print(">>> Starting INSURANCE PILOT (Claims Fast-Track) <<<")
    print(f"Runtime Root: {os.environ['AGW_RUNTIME_ROOT']}")
    print(f"Motor: {os.environ['MOTOR_CLASS']} from {os.environ['MOTOR_PATH']}")
    
    # Importar app DESPUÉS de setear env vars, para que settings.py las lea
    from antigravity_wings.api.server import app
    
    uvicorn.run(app, host="0.0.0.0", port=8001) # Puerto distinto al default

if __name__ == "__main__":
    main()
