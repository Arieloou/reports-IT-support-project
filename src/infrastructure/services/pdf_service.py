import os
import tempfile
from docx import Document
from docx2pdf import convert
from openpyxl import load_workbook
import platform
from typing import Optional

from src.core.constants import TEMPLATE_PATH, TEMPLATE_RESPALDO_PATH, TEMPLATE_DEVOLUCION_PATH, MESES
from src.domain.models import DatosActa
from src.infrastructure.services.file_system import FileSystemService

class DocumentService:
    @staticmethod
    def _set_cell_text(cell, text: str):
        """Escribe texto en una celda de tabla sin perder el formato de párrafo existente."""
        if not cell.paragraphs:
            cell.add_paragraph()
            
        paragraph = cell.paragraphs[0]
        if paragraph.runs:
            paragraph.runs[0].text = text
            for run in paragraph.runs[1:]:
                run.text = ""
        else:
            paragraph.add_run(text)

    @staticmethod
    def generate_acta_entrega(data: DatosActa) -> Optional[str]:
        """Genera un PDF rellenando la plantilla DOCX 'ACTA ENTREGA.docx'."""
        try:
            doc = Document(TEMPLATE_PATH)

            # --- Párrafo 1: Declaración ---
            p1 = doc.paragraphs[1]
            p1.runs[2].text = data.nombre + " "
            p1.runs[5].text = " " + data.cedula + " "

            # --- Párrafo 15: Fecha ---
            partes_fecha = data.fecha.split("/")
            if len(partes_fecha) == 3:
                dia, mes_num, anio = partes_fecha
                p15 = doc.paragraphs[15]
                p15.runs[1].text = dia
                p15.runs[3].text = MESES.get(int(mes_num), "___")
                p15.runs[5].text = anio

            # --- Tabla 0: Bienes entregados ---
            t0 = doc.tables[0]
            DocumentService._set_cell_text(t0.rows[0].cells[1], data.equipo)
            DocumentService._set_cell_text(t0.rows[1].cells[1], data.marca)
            DocumentService._set_cell_text(t0.rows[2].cells[1], data.modelo)
            DocumentService._set_cell_text(t0.rows[3].cells[1], data.codigo)

            DocumentService._set_cell_text(t0.rows[0].cells[2], data.equipo2)
            DocumentService._set_cell_text(t0.rows[1].cells[2], data.marca2)
            DocumentService._set_cell_text(t0.rows[2].cells[2], data.modelo2)
            DocumentService._set_cell_text(t0.rows[3].cells[2], data.codigo2)

            DocumentService._set_cell_text(t0.rows[4].cells[1], data.ticket)
            DocumentService._set_cell_text(t0.rows[5].cells[1], data.fecha)
            DocumentService._set_cell_text(t0.rows[6].cells[1], data.observaciones)

            # --- Tabla 1: Firma ---
            t1 = doc.tables[1]
            DocumentService._set_cell_text(t1.rows[1].cells[1], data.nombre)
            DocumentService._set_cell_text(t1.rows[2].cells[1], data.cedula)

            # --- Guardar ---
            nombre_archivo = "".join(c for c in f"ACTA ENTREGA {data.nombre}" if c not in r'\/:*?"<>|')
            route = FileSystemService.get_records_path("ACTAS DE ENTREGA")
            if not route:
                raise Exception("Could not create output directory")

            temp_dir = tempfile.gettempdir()
            temp_docx = os.path.join(temp_dir, f"{nombre_archivo}.docx")
            output_pdf = os.path.join(route, f"{nombre_archivo}.pdf")

            doc.save(temp_docx)
            convert(temp_docx, output_pdf)

            if os.path.exists(temp_docx):
                os.remove(temp_docx)

            return output_pdf
        except Exception as e:
            print(f"Error generating acta de entrega: {e}")
            raise

    @staticmethod
    def generate_acta_respaldo(data: DatosActa) -> Optional[str]:
        """Genera un PDF rellenando la plantilla de respaldo."""
        try:
            doc = Document(TEMPLATE_RESPALDO_PATH)

            partes_fecha = data.fecha.split("/")
            if len(partes_fecha) == 3:
                dia, mes, anio = partes_fecha
                p4 = doc.paragraphs[4]
                p4.runs[3].text = dia
                p4.runs[5].text = mes
                p4.runs[7].text = anio
                p4.runs[8].text = ""

            p7 = doc.paragraphs[7]
            p7.runs[3].text = data.nombre + " "

            p11 = doc.paragraphs[11]
            p11.runs[2].text = data.nombre
            p11.runs[4].text = data.motivo or "realizar un cambio y/o formateo del equipo"
            p11.runs[5].text = ""
            p11.runs[6].text = "."

            p18 = doc.paragraphs[18]
            p18.runs[2].text = data.nombre

            nombre_archivo = "".join(c for c in f"ACTA RESPALDO {data.nombre}" if c not in r'\/:*?"<>|')
            route = FileSystemService.get_records_path("ACTAS DE RESPALDO")
            if not route:
                raise Exception("Could not create output directory")

            temp_dir = tempfile.gettempdir()
            temp_docx = os.path.join(temp_dir, f"{nombre_archivo}.docx")
            output_pdf = os.path.join(route, f"{nombre_archivo}.pdf")

            doc.save(temp_docx)
            convert(temp_docx, output_pdf)

            if os.path.exists(temp_docx):
                os.remove(temp_docx)

            return output_pdf
        except Exception as e:
            print(f"Error generating acta de respaldo: {e}")
            raise

    @staticmethod
    def generate_acta_devolucion(data: DatosActa) -> Optional[str]:
        """Genera el Excel de devolución y lo devuelve (la ruta)."""
        try:
            nombre_archivo = "".join(c for c in f"ACTA DEVOLUCION {data.nombre}" if c not in r'\/:*?"<>|')
            route = FileSystemService.get_records_path("ACTAS DE DEVOLUCION")
            if not route:
                raise Exception("Could not create output directory")
                
            wb = load_workbook(TEMPLATE_DEVOLUCION_PATH)
            # Add mapping logic if the template has specific cells to fill
            # Currently it just saves a copy based on the original code
            
            output_xlsx = os.path.join(route, f"{nombre_archivo}.xlsx")
            wb.save(output_xlsx)
            return output_xlsx
        except Exception as e:
            print(f"Error generating acta de devolucion: {e}")
            raise
