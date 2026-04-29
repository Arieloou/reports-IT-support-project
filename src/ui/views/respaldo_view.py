import flet as ft
from src.core.utils import clean_up_text
from src.domain.models import TransactionRecord
from src.application.acta_service import ActaService
from src.ui.components.common import make_date_row, do_search, show_popup_message

def build_respaldo_form(page: ft.Page, service: ActaService) -> ft.Column:
    nombre = ft.TextField(label="Nombres")
    cedula = ft.TextField(label="Cédula")
    fecha, fila_fecha, cal_box = make_date_row(page)
    
    motivo = ft.TextField(
        label="Motivo del Respaldo",
        hint_text="Ej: realizar un cambio y/o formateo del equipo",
        multiline=True, min_lines=2,
    )

    search_btn = ft.IconButton(
        icon=ft.Icons.SEARCH, tooltip="Buscar cédula",
        on_click=lambda e: do_search(page, service, nombre, cedula)
    )
    fila_nombre = ft.Row([nombre, search_btn])

    def generar(e):
        from src.domain.models import Person, TicketRecord
        data = TransactionRecord(
            person=Person(name=clean_up_text(nombre.value), ci_document=clean_up_text(cedula.value)),
            devices=[],
            ticket=TicketRecord(),
            date=clean_up_text(fecha.value),
            reason=clean_up_text(motivo.value) if motivo.value else "realizar un cambio y/o formateo del equipo"
        )
        
        success, msg = service.generate_respaldo(data)
        show_popup_message(page, msg)

    return ft.Column([
        fila_nombre, cedula, fila_fecha, cal_box,
        ft.Divider(),
        motivo,
        ft.Container(height=8),
        ft.Button("Generar Acta de Respaldo", icon=ft.Icons.CLOUD_UPLOAD, on_click=generar),
    ], scroll=ft.ScrollMode.AUTO, spacing=10)
