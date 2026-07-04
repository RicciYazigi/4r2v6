# launcher.py

"""
Launcher maestro para antigravity_wings.

Levanta el servidor FastAPI (API + Cockpit) en localhost:8000.

Uso:
    python launcher.py

Requiere:
    - uvicorn instalado (`pip install uvicorn[standard] fastapi`).
"""

import uvicorn
import os
import sys

# Asegurar que el directorio actual esté en el path para resolver antigravity_wings
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main() -> None:
    uvicorn.run(
        "antigravity_wings.api.server:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
    )


if __name__ == "__main__":
    main()
