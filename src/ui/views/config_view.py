import flet as ft
from src.core.config import save_config
from src.core.constants import SEDES
from src.ui.components.common import show_popup_message

def build_config_view(page: ft.Page, current_config: dict, on_config_saved) -> ft.Column:
    nombre_tecnico = ft.TextField(
        label="Nombre y Apellidos del Técnico",
        hint_text="Ej: Juan Pérez López",
        value=current_config.get("nombre_tecnico", ""),
        capitalization=ft.TextCapitalization.WORDS,
    )
    
    sede_dropdown = ft.Dropdown(
        label="Sede (Campus)", hint_text="Seleccione su campus",
        options=[ft.dropdown.Option(s) for s in SEDES],
        value=current_config.get("sede", None), width=300,
    )
    
    error_text = ft.Text("", color=ft.Colors.RED, visible=False)

    def guardar(e):
        if not nombre_tecnico.value or not nombre_tecnico.value.strip():
            error_text.value = "Debe ingresar su nombre y apellidos."
            error_text.visible = True
            page.update()
            return
            
        if not sede_dropdown.value:
            error_text.value = "Debe seleccionar una sede."
            error_text.visible = True
            page.update()
            return

        config_data = {
            "nombre_tecnico": nombre_tecnico.value.strip(),
            "sede": sede_dropdown.value,
        }
        
        if save_config(config_data):
            on_config_saved(config_data)
            show_popup_message(page, "Configuración guardada.")
        else:
            show_popup_message(page, "Error al guardar la configuración.")

    return ft.Column([
        ft.Text("Configuración", size=24, weight=ft.FontWeight.BOLD),
        ft.Text("Datos del técnico responsable.", size=13, color=ft.Colors.ON_SURFACE_VARIANT),
        ft.Divider(height=20),
        nombre_tecnico,
        sede_dropdown,
        error_text,
        ft.Container(height=12),
        ft.Button("Guardar", icon=ft.Icons.SAVE, on_click=guardar),
    ], spacing=12)
