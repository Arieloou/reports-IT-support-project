import flet as ft
from datetime import datetime, timezone
from typing import Callable, List
from src.domain.models import Person
from src.application.acta_service import ActaService

def show_popup_message(page: ft.Page, texto: str):
    """Muestra un mensaje emergente básico en la página."""
    def close_popup(e):
        dialogo.open = False
        page.update()
        
    dialogo = ft.AlertDialog(
        title=ft.Text("Estado"),
        content=ft.Text(texto),
        actions=[ft.TextButton("Aceptar", on_click=close_popup)],
    )
    page.overlay.append(dialogo)
    dialogo.open = True
    page.update()

def make_date_row(page: ft.Page) -> tuple[ft.TextField, ft.Row, ft.Container]:
    """Crea un campo de fecha con calendario inline."""
    fecha = ft.TextField(
        label="Fecha", read_only=True,
        value=datetime.now().strftime("%d/%m/%Y")
    )
    
    picker = ft.CupertinoDatePicker(
        date_picker_mode=ft.CupertinoDatePickerMode.DATE,
        value=datetime.now(tz=timezone.utc),
        first_date=datetime(2020, 1, 1, tzinfo=timezone.utc),
        last_date=datetime(2030, 12, 31, tzinfo=timezone.utc),
        on_change=lambda e: _set_fecha(e, fecha, page),
    )
    
    cal_box = ft.Container(
        content=picker, height=150,
        border=ft.border.all(1, ft.Colors.OUTLINE),
        border_radius=10, padding=5, visible=False,
    )

    def _toggle(e):
        cal_box.visible = not cal_box.visible
        page.update()

    def _set_fecha(e, f, p):
        sel = e.control.value
        if sel:
            f.value = sel.strftime("%d/%m/%Y")
            p.update()

    btn = ft.IconButton(icon=ft.Icons.CALENDAR_MONTH, tooltip="Seleccionar fecha", on_click=_toggle)
    row = ft.Row([fecha, btn])
    return fecha, row, cal_box

def show_individual_options_list(page: ft.Page, matches: List[Person], nombre_field: ft.TextField, cedula_field: ft.TextField):
    """Muestra coincidencias para que el usuario elija."""
    def seleccionar(e, cedula_sel: str, nombre_sel: str):
        cedula_field.value = cedula_sel
        nombre_field.value = nombre_sel
        dialogo.open = False
        page.update()

    opciones = []
    for match in matches:
        opciones.append(
            ft.TextButton(
                content=ft.Text(f"{match.name}  —  {match.ci_document}"),
                on_click=lambda e, c=match.ci_document, n=match.name: seleccionar(e, c, n),
            )
        )

    def close_list(e):
        dialogo.open = False
        page.update()

    dialogo = ft.AlertDialog(
        title=ft.Text("Seleccione una Persona"),
        content=ft.Column(opciones, tight=True, scroll=ft.ScrollMode.AUTO),
        actions=[ft.TextButton("Cancelar", on_click=close_list)],
    )
    page.overlay.append(dialogo)
    dialogo.open = True
    page.update()

def do_search(page: ft.Page, service: ActaService, nombre_field: ft.TextField, cedula_field: ft.TextField):
    """Ejecuta la búsqueda de cédula por nombre usando el servicio."""
    if not nombre_field.value or not nombre_field.value.strip():
        show_popup_message(page, "Ingrese un nombre para buscar.")
        return
        
    results = service.search_personas(nombre_field.value)
    
    if not results:
        show_popup_message(page, "No se encontró información.")
    else:
        show_individual_options_list(page, results, nombre_field, cedula_field)
