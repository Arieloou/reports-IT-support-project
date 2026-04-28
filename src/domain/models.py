from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

class TipoActa(Enum):
    ENTREGA = "ENTREGA"
    RESPALDO = "RESPALDO"
    DEVOLUCION = "DEVOLUCION"

@dataclass
class Persona:
    nombre: str
    cedula: str

@dataclass
class Equipo:
    equipo: str = ""
    marca: str = ""
    modelo: str = ""
    codigo: str = ""

@dataclass
class DatosActa:
    nombre: str
    fecha: str
    cedula: str = ""
    
    # Activo 1
    equipo: str = ""
    marca: str = ""
    modelo: str = ""
    codigo: str = ""
    
    # Activo 2
    equipo2: str = ""
    marca2: str = ""
    modelo2: str = ""
    codigo2: str = ""
    
    ticket: str = ""
    observaciones: str = ""
    motivo: str = "realizar un cambio y/o formateo del equipo" # Default para respaldo
    
    def to_dict(self) -> dict:
        return {
            "nombre": self.nombre,
            "cedula": self.cedula,
            "fecha": self.fecha,
            "equipo": self.equipo,
            "marca": self.marca,
            "modelo": self.modelo,
            "codigo": self.codigo,
            "equipo2": self.equipo2,
            "marca2": self.marca2,
            "modelo2": self.modelo2,
            "codigo2": self.codigo2,
            "ticket": self.ticket,
            "observaciones": self.observaciones,
            "motivo": self.motivo
        }
