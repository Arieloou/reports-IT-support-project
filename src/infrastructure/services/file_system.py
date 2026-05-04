import os
import platform
import subprocess
from pathlib import Path
from datetime import datetime
import sys
from typing import List, Dict, Optional
from src.core.constants import RECORD_FOLDERS

class FileSystemService:
    @staticmethod
    def get_records_path(route_name: str) -> Optional[str]:
        """
        Devuelve la ruta absoluta de la carpeta 'route_name' del usuario actual.
        Crea la carpeta si no existe.
        """
        try:
            home = Path.home() 
            possible_paths = [
                home / "Documents" / route_name,
                home / "Documentos" / route_name 
            ]
            
            for path in possible_paths:
                if path.parent.exists() and path.parent.is_dir():
                    path.mkdir(exist_ok=True)
                    return str(path.resolve())
            
            # Fallback if Documents doesn't exist
            fallback_path = home / route_name
            fallback_path.mkdir(exist_ok=True)
            return str(fallback_path.resolve())
        
        except Exception as e:
            print(f"Error al obtener/crear la carpeta {route_name}: {e}", file=sys.stderr)
            return None

    @staticmethod
    def open_file(ruta: str):
        """Abre un archivo (PDF, XLSX, etc.) usando la aplicación predeterminada del sistema."""
        if not os.path.exists(ruta):
            print(f"File not found: {ruta}")
            return
            
        sistema = platform.system()
        try:
            if sistema == "Windows":
                os.startfile(ruta)
            elif sistema == "Darwin":
                subprocess.call(["open", ruta])
            else:
                subprocess.call(["xdg-open", ruta])
        except Exception as e:
            print(f"Error opening file {ruta}: {e}")

    @staticmethod
    def get_all_generated_records() -> List[Dict]:
        """Escanea las carpetas de actas y retorna lista de diccionarios con info de cada PDF."""
        records = []
        for folder_name in RECORD_FOLDERS:
            folder = FileSystemService.get_records_path(folder_name)
            if not folder or not os.path.exists(folder):
                continue

            for f in os.listdir(folder):
                if not f.lower().endswith((".pdf", ".xlsx")) or f.startswith("~$"):
                    continue

                full_path = os.path.join(folder, f)
                try:
                    mod_time = os.path.getmtime(full_path)
                    mod_date = datetime.fromtimestamp(mod_time)
                    records.append({
                        "nombre": f,
                        "ruta": str(full_path),
                        "fecha": mod_date.strftime("%d/%m/%Y %H:%M"),
                        "tipo": folder_name,
                    })
                except Exception as e:
                    print(f"Error reading metadata for {f}: {e}")
                            
        records.sort(key=lambda x: os.path.getmtime(x["ruta"]), reverse=True)
        return records
