import json
import os
from .constants import CONFIG_PATH

def load_config():
    """Carga la configuración guardada. Retorna dict o None si no existe."""
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error cargando configuración: {e}")
            return None
    return None

def save_config(data):
    """Guarda la configuración en un archivo JSON."""
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Error guardando configuración: {e}")
        return False
