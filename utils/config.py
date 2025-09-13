import json
import os

def cargar_config(path="config.json"):
    """Carga la configuración desde un archivo JSON."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"No se encontró el archivo de configuración: {path}")

    with open(path, "r", encoding="utf-8") as f:
        config = json.load(f)

    return config