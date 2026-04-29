import flet as ft
from src.core.utils import clean_up_text
from src.domain.models import TransactionRecord
from src.application.acta_service import ActaService
from src.ui.components.common import make_date_row, do_search, show_popup_message

def build_formateo_form(page: ft.Page, service: ActaService) -> ft.Column:
    nombre = ft.TextField(label="Nombres")
    cedula = ft.TextField(label="Cédula")
    fecha, fila_fecha, cal_box = make_date_row(page)

    equipo = ft.TextField(label="Equipo")
    marca = ft.TextField(label="Marca")
    modelo = ft.TextField(label="Modelo")
    codigo = ft.TextField(label="Código")
    ticket = ft.TextField(label="Ticket")
    observaciones = ft.TextField(label="Observaciones", multiline=True, min_lines=2)
    motivo = ft.TextField(
        label="Motivo del Respaldo",
        value="realizar un cambio y/o formateo del equipo",
        multiline=True, min_lines=2,
    )

    search_btn = ft.IconButton(
        icon=ft.Icons.SEARCH, tooltip="Buscar cédula",
        on_click=lambda e: do_search(page, service, nombre, cedula)
    )
    fila_nombre = ft.Row([nombre, search_btn])

    def generar_todo(e):
        from src.domain.models import Person, Device, TicketRecord
        device = Device(
            device_type=clean_up_text(equipo.value),
            brand=clean_up_text(marca.value),
            model=clean_up_text(modelo.value),
            udla_code=clean_up_text(codigo.value)
        )
        person = Person(name=clean_up_text(nombre.value), ci_document=clean_up_text(cedula.value))
        ticket_obj = TicketRecord(ticket=clean_up_text(ticket.value), observations=clean_up_text(observaciones.value))
        date_str = clean_up_text(fecha.value)

        data_entrega = TransactionRecord(
            person=person,
            devices=[device],
            ticket=ticket_obj,
            date=date_str
        )
        data_respaldo = TransactionRecord(
            person=person,
            devices=[],
            ticket=TicketRecord(),
            date=date_str,
            reason=clean_up_text(motivo.value) if motivo.value else "realizar un cambio y/o formateo del equipo"
        )
        data_devolucion = TransactionRecord(
            person=person,
            devices=[device],
            ticket=ticket_obj,
            date=date_str
        )

        success, msg = service.generate_formateo_suite(data_entrega, data_respaldo, data_devolucion)
        show_popup_message(page, msg)

    return ft.Column([
        ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.INFO_OUTLINE, color=ft.Colors.PRIMARY, size=18),
                ft.Text("Este formulario genera 3 actas: Entrega, Respaldo y Devolución.",
                        size=13, italic=True, color=ft.Colors.ON_SURFACE_VARIANT),
            ]),
            bgcolor=ft.Colors.with_opacity(0.08, ft.Colors.PRIMARY),
            border_radius=8, padding=ft.padding.symmetric(horizontal=12, vertical=8),
        ),
        ft.Container(height=4),
        fila_nombre, cedula, fila_fecha, cal_box,
        ft.Divider(),
        ft.Text("Datos del Equipo", size=15, weight=ft.FontWeight.BOLD),
        equipo, marca, modelo, codigo,
        ft.Divider(),
        ticket, observaciones,
        ft.Divider(),
        ft.Text("Respaldo", size=15, weight=ft.FontWeight.BOLD),
        motivo,
        ft.Container(height=8),
        ft.Button("Generar 3 Actas", icon=ft.Icons.LIBRARY_BOOKS, on_click=generar_todo),
    ], scroll=ft.ScrollMode.AUTO, spacing=10)
