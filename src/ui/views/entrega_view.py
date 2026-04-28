import flet as ft
from src.core.utils import clean_up_text
from src.domain.models import DatosActa
from src.application.acta_service import ActaService
from src.ui.components.common import make_date_row, do_search, show_popup_message

def build_entrega_form(page: ft.Page, service: ActaService) -> ft.Column:
    nombre = ft.TextField(label="Nombres")
    cedula = ft.TextField(label="Cédula")
    fecha, fila_fecha, cal_box = make_date_row(page)
    
    equipo = ft.TextField(label="Equipo")
    marca = ft.TextField(label="Marca")
    modelo = ft.TextField(label="Modelo")
    codigo = ft.TextField(label="Código")

    equipo2 = ft.TextField(label="Equipo 2")
    marca2 = ft.TextField(label="Marca 2")
    modelo2 = ft.TextField(label="Modelo 2")
    codigo2 = ft.TextField(label="Código 2")
    activo2_fields = ft.Column([equipo2, marca2, modelo2, codigo2], visible=False)

    def toggle_a2(e):
        activo2_fields.visible = a2_check.value
        page.update()

    a2_check = ft.Checkbox(label="Agregar segundo activo", value=False, on_change=toggle_a2)
    ticket = ft.TextField(label="# Ticket")
    observaciones = ft.TextField(label="Observaciones", multiline=True, min_lines=2)

    search_btn = ft.IconButton(
        icon=ft.Icons.SEARCH, tooltip="Buscar cédula",
        on_click=lambda e: do_search(page, service, nombre, cedula)
    )
    fila_nombre = ft.Row([nombre, search_btn])

    def generar(e):
        data = DatosActa(
            nombre=clean_up_text(nombre.value),
            cedula=clean_up_text(cedula.value),
            fecha=clean_up_text(fecha.value),
            equipo=clean_up_text(equipo.value),
            marca=clean_up_text(marca.value),
            modelo=clean_up_text(modelo.value),
            codigo=clean_up_text(codigo.value),
            ticket=clean_up_text(ticket.value),
            observaciones=clean_up_text(observaciones.value),
        )
        if a2_check.value:
            data.equipo2 = clean_up_text(equipo2.value)
            data.marca2 = clean_up_text(marca2.value)
            data.modelo2 = clean_up_text(modelo2.value)
            data.codigo2 = clean_up_text(codigo2.value)
            
        success, msg = service.generate_entrega(data)
        show_popup_message(page, msg)

    return ft.Column([
        fila_nombre, cedula, fila_fecha, cal_box,
        ft.Divider(),
        ft.Text("Activo 1", size=15, weight=ft.FontWeight.BOLD),
        equipo, marca, modelo, codigo,
        a2_check, activo2_fields,
        ft.Divider(),
        ticket, observaciones,
        ft.Container(height=8),
        ft.Button("Generar Acta de Entrega", icon=ft.Icons.PICTURE_AS_PDF, on_click=generar),
    ], scroll=ft.ScrollMode.AUTO, spacing=10)
