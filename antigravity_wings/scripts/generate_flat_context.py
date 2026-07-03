import os
from pathlib import Path

# Configuración
ROOT_DIR = Path(__file__).parent.parent
OUTPUT_FILE = ROOT_DIR / "docs" / "ANTIGRAVITY_WINGS_V1.0_FLAT.md"

# Extensiones a incluir
EXTENSIONS = {".py", ".md", ".json", ".js", ".html", ".css", ".yml", ".yaml", ".toml"}

# Directorios a excluir
EXCLUDE_DIRS = {
    ".git", "__pycache__", ".pytest_cache", "runtime_data", 
    "profiles_store", "venv", ".venv", "node_modules", "dist", "build"
}

# Archivos específicos a excluir
EXCLUDE_FILES = {
    "package-lock.json", "yarn.lock", "startup_error.txt", 
    "test_log.txt", "pilot_result.log", "ANTIGRAVITY_WINGS_V1.0_FLAT.md"
}

def generate_flat_file():
    print(f"Generando Flat Pack en: {OUTPUT_FILE}")
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        # Header del documento
        out.write("# ANTIGRAVITY WINGS v1.0 - FLAT CONTEXT\n")
        out.write("> **GENERADO AUTOMÁTICAMENTE PARA NOTEBOOKLM**\n")
        out.write("> **FECHA:** 08/01/2026\n\n")
        out.write("Este documento contiene el código fuente completo del sistema Antigravity Wings v1.0-CANONICAL, aplanado para análisis de contexto.\n\n")
        out.write("---\n\n")

        # Recorrer el árbol
        for root, dirs, files in os.walk(ROOT_DIR):
            # Filtrar directorios in-place
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            
            for file in files:
                if file in EXCLUDE_FILES:
                    continue
                
                file_path = Path(root) / file
                
                if file_path.suffix not in EXTENSIONS:
                    continue
                
                # Calcular ruta relativa
                rel_path = file_path.relative_to(ROOT_DIR)
                
                print(f"Agregando: {rel_path}")
                
                # Escribir encabezado de archivo
                out.write(f"## ARCHIVO: {rel_path}\n")
                out.write("```" + file_path.suffix.lstrip(".") + "\n")
                
                try:
                    content = file_path.read_text(encoding="utf-8")
                    out.write(content)
                except Exception as e:
                    out.write(f"[ERROR LEYENDO ARCHIVO: {e}]")
                
                out.write("\n```\n\n")
                out.write("---\n\n")

    print("✅ Flat Pack generado exitosamente.")

if __name__ == "__main__":
    generate_flat_file()
