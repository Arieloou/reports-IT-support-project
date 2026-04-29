import os
from openpyxl import Workbook, load_workbook
from src.core.utils import standardize_name
from src.core.constants import DATA_FILE_PATH
from src.domain.models import Person, TransactionRecord
from typing import List

class ExcelRepository:
    def __init__(self, file_path: str = DATA_FILE_PATH):
        self.file_path = file_path

    def get_personas_by_name(self, nombre_buscar: str) -> List[Person]:
        """Busca personas por nombre en el archivo de Excel."""
        if not os.path.exists(self.file_path):
            return []

        try:
            wb = load_workbook(self.file_path, read_only=True)
            if "PERSONAS" not in wb.sheetnames:
                wb.close()
                return []
            
            ws = wb["PERSONAS"]
            palabras_buscar = standardize_name(nombre_buscar)
            
            if not palabras_buscar:
                wb.close()
                return []

            possible_matches = []
            for fila in ws.iter_rows(min_row=2, values_only=True):
                if fila[0] is None:
                    continue
                palabras_fila = standardize_name(str(fila[0]))

                if set(palabras_buscar).issubset(palabras_fila):
                    possible_matches.append(Person(name=str(fila[0]), ci_document=str(fila[1])))
            
            wb.close()
            return possible_matches
        except Exception as e:
            print(f"Error reading Excel for search: {e}")
            return []

    def save_transaction_record(self, data: TransactionRecord) -> bool:
        """Guarda el registro de un acta generada en el Excel."""
        try:
            if os.path.exists(self.file_path):
                wb = load_workbook(self.file_path)
                ws = wb["REGISTROS"]
            else:
                wb = Workbook()
                ws = wb["REGISTROS"]
                ws.append([
                    "NOMBRE", "CEDULA", "FECHA",
                    "EQUIPO", "MARCA", "MODELO", "CODIGO", "SERIE",
                    "TICKET", "OBSERVACIONES"
                ])

            for device in data.devices:
                ws.append([
                    data.person.name,
                    data.person.ci_document,
                    data.date,
                    device.device_type,
                    device.brand,
                    device.model,
                    device.udla_code,
                    device.serial_number,
                    data.ticket.ticket,
                    data.ticket.observations,
                ])
            
            wb.save(self.file_path)
            return True
        except Exception as e:
            print(f"Error saving to Excel: {e}")
            return False

    def save_new_person(self, data: Person) -> bool:
        """Guarda el registro de una nueva persona en el Excel."""
        try:
            if os.path.exists(self.file_path):
                wb = load_workbook(self.file_path)
                ws = wb["PERSONAS"]
            else:
                wb = Workbook()
                ws = wb["PERSONAS"]
                ws.append([
                    "NOMBRE", "CEDULA"
                ])

            ws.append([
                data.name,
                data.ci_document,
            ])

            wb.save(self.file_path)
            return True
        except Exception as e:
            print(f"Error saving to Excel: {e}")
            return False
