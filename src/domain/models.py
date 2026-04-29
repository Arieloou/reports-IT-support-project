from datetime import datetime
from typing import List
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

class ActaType(Enum):
    ENTREGA = "ENTREGA"
    RESPALDO = "RESPALDO"
    DEVOLUCION = "DEVOLUCION"

@dataclass
class Person:
    name: str
    ci_document: str = ""

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "ci_document": self.ci_document,
        }

@dataclass
class Device:
    device_type: str = ""
    brand: str = ""
    model: str = ""
    udla_code: str = ""
    serial_number: str = ""

# Clase que engloba una transacción
@dataclass
class TransactionRecord:
    person: Person
    devices: List[Device]
    ticket: TicketRecord
    date: datetime.date
    reason: str = ""

    def to_dict(self) -> dict:
        return {
            "name": self.person.name,
            "ci_document": self.person.ci_document,
            "devices": self.devices,
            "ticket": self.ticket.ticket,
            "observations": self.ticket.observations,
            "date": self.date.strftime("%d/%m/%Y"),
            "reason": self.reason,
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