from typing import Tuple, List
from src.domain.models import TransactionRecord, Person
from src.infrastructure.persistence.excel_repository import ExcelRepository
from src.infrastructure.services.pdf_service import DocumentService
from src.infrastructure.services.file_system import FileSystemService

class ActaService:
    def __init__(self):
        self.excel_repo = ExcelRepository()

    def search_personas(self, nombre: str) -> List[Person]:
        """Busca personas en la base de datos de Excel."""
        return self.excel_repo.get_personas_by_name(nombre)

    def generate_entrega(self, data: TransactionRecord) -> Tuple[bool, str]:
        """Genera el acta de entrega y guarda el registro."""
        try:
            ruta_pdf = DocumentService.generate_acta_entrega(data)
            self.excel_repo.save_transaction_record(data)
            FileSystemService.open_file(ruta_pdf)
            return True, "Acta de Entrega generada correctamente."
        except Exception as e:
            return False, f"Error al generar Acta de Entrega: {str(e)}"

    def generate_respaldo(self, data: TransactionRecord) -> Tuple[bool, str]:
        """Genera el acta de respaldo."""
        try:
            ruta_pdf = DocumentService.generate_acta_respaldo(data)
            FileSystemService.open_file(ruta_pdf)
            return True, "Acta de Respaldo generada correctamente."
        except Exception as e:
            return False, f"Error al generar Acta de Respaldo: {str(e)}"

    def generate_formateo_suite(self, data_entrega: TransactionRecord, data_respaldo: TransactionRecord, data_devolucion: TransactionRecord) -> Tuple[bool, str]:
        """Genera el conjunto de actas para un caso de formateo/cambio."""
        generados = []
        errores = []

        # 1. Entrega
        try:
            ruta_entrega = DocumentService.generate_acta_entrega(data_entrega)
            self.excel_repo.save_transaction_record(data_entrega)
            FileSystemService.open_file(ruta_entrega)
            generados.append("Entrega")
        except Exception as e:
            errores.append(f"Entrega: {e}")

        # 2. Respaldo
        try:
            ruta_respaldo = DocumentService.generate_acta_respaldo(data_respaldo)
            FileSystemService.open_file(ruta_respaldo)
            generados.append("Respaldo")
        except Exception as e:
            errores.append(f"Respaldo: {e}")

        # 3. Devolución
        try:
            ruta_devolucion = DocumentService.generate_acta_devolucion(data_devolucion)
            FileSystemService.open_file(ruta_devolucion)
            generados.append("Devolución")
        except Exception as e:
            errores.append(f"Devolución: {e}")

        msg = ""
        if generados:
            msg += f"Generados exitosamente: {', '.join(generados)}."
        if errores:
            msg += f"\nErrores: {'; '.join(errores)}."

        success = len(errores) == 0
        return success, msg.strip()

    def get_generated_records_history(self) -> List[dict]:
        """Obtiene el historial de actas generadas."""
        return FileSystemService.get_all_generated_records()

    def open_record(self, path: str):
        """Abre un documento específico."""
        FileSystemService.open_file(path)
