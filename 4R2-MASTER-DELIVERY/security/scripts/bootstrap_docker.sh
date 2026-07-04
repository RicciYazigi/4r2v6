#!/bin/bash
echo ">>> Iniciando Docker [WSL2 Context] <<<"

# Si es Docker nativo en Linux/WSL
if command -v systemctl >/dev/null 2>&1; then
    sudo systemctl start docker
fi

echo "Esperando a que el daemon esté listo..."
for i in {1..30}; do
    if docker ps >/dev/null 2>&1; then
        echo "Docker está LISTO."
        exit 0
    fi
    echo "Todavía iniciando... ($i/30)"
    sleep 5
done

echo "FAIL: No se pudo conectar a Docker. Asegúrate de que el servicio esté corriendo en Windows o WSL2."
exit 1
