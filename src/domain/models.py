from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

class ActaType(Enum):
    ENTREGA = "ENTREGA"
    RESPALDO = "RESPALDO"
    DEVOLUCION = "DEVOLUCION"

@dataclass
class Person:
    nombre: str
    cedula: str

@dataclass
class Device:
    device_type: str = ""
    brand: str = ""
    model: str = ""
    udla_code: str = ""
    serial_number: str = ""

@dataclass
class TransactionRecord:
    device: str = ""
    brand: str = ""
    model: str = ""
    udla_code: str = ""
    serial_number: str = ""

    def to_dict(self) -> dict:
        return {
            "device": self.device,
            "brand": self.brand,
            "model": self.model,
            "udla_code": self.udla_code,
            "serial_number": self.serial_number,
        }

@dataclass
class TicketRecord:
    ticket: str = ""
    observations: str = ""

    def to_dict(self) -> dict:
        return {
            "ticket": self.ticket,
            "observations": self.observations,
        }


@dataclass
class NewPersonRecord:
    nombre: str
    fecha: str
    cedula: str = ""
    
    def to_dict(self) -> dict:
        return {
            "nombre": self.nombre,
            "cedula": self.cedula,
        }
