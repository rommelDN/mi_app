# Archivo para cargar configuraciones desde archivo JSON

# Importa el módulo json para leer y parsear el archivo JSON
import json
# Importa el módulo os para verificar la existencia de archivos y rutas
import os

def cargar_config(path="config.json"):
    """
    Carga la configuración desde un archivo JSON.

    :param path: Ruta al archivo de configuración JSON.
    """
    # Valida si el archivo existe
    if not os.path.exists(path):
        raise FileNotFoundError(f"No se encontró el archivo de configuración: {path}")

    # Abre el archivo en modo lectura con codificación UTF-8
    with open(path, "r", encoding="utf-8") as f:
        # Transforma el contenido del archivo en un diccionario Python
        config = json.load(f)

    # Devuelve la configuración cargada
    return config