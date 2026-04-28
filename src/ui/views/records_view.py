import flet as ft
from src.application.acta_service import ActaService

def build_records_view(page: ft.Page, service: ActaService, content_area_updater) -> ft.Column:
    records = service.get_generated_records_history()

    if not records:
        empty = ft.Column([
            ft.Icon(ft.Icons.FOLDER_OPEN, size=64, color=ft.Colors.ON_SURFACE_VARIANT),
            ft.Text("No hay actas generadas aún.", size=16, color=ft.Colors.ON_SURFACE_VARIANT),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=12, alignment=ft.MainAxisAlignment.CENTER)
        
        return ft.Column([
            ft.Text("Actas Generadas", size=24, weight=ft.FontWeight.BOLD),
            ft.Container(content=empty, expand=True, alignment=ft.Alignment(0, 0)),
        ], expand=True)

    list_items = []
    for r in records:
        tipo_color = ft.Colors.BLUE if "ENTREGA" in r["tipo"] else ft.Colors.TEAL
        tipo_label = "Entrega" if "ENTREGA" in r["tipo"] else "Respaldo"

        tile = ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.PICTURE_AS_PDF, color=ft.Colors.RED_400, size=32),
                ft.Column([
                    ft.Text(r["nombre"], size=14, weight=ft.FontWeight.W_500, max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                    ft.Row([
                        ft.Container(
                            content=ft.Text(tipo_label, size=11, color=ft.Colors.WHITE),
                            bgcolor=tipo_color, border_radius=4,
                            padding=ft.padding.symmetric(horizontal=6, vertical=2),
                        ),
                        ft.Text(r["fecha"], size=12, color=ft.Colors.ON_SURFACE_VARIANT),
                    ], spacing=8),
                ], spacing=2, expand=True),
                ft.IconButton(
                    icon=ft.Icons.OPEN_IN_NEW, tooltip="Abrir PDF",
                    on_click=lambda e, path=r["ruta"]: service.open_record(path),
                ),
            ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.padding.symmetric(horizontal=12, vertical=8),
            border=ft.border.all(1, ft.Colors.with_opacity(0.12, ft.Colors.ON_SURFACE)),
            border_radius=10,
        )
        list_items.append(tile)

    def refresh(e):
        content_area_updater()

    return ft.Column([
        ft.Row([
            ft.Text("Actas Generadas", size=24, weight=ft.FontWeight.BOLD),
            ft.Container(expand=True),
            ft.IconButton(icon=ft.Icons.REFRESH, tooltip="Refrescar", on_click=refresh),
        ]),
        ft.Text(f"{len(records)} documento(s) encontrado(s)", size=13, color=ft.Colors.ON_SURFACE_VARIANT),
        ft.Container(height=4),
        ft.Column(list_items, scroll=ft.ScrollMode.AUTO, spacing=6, expand=True),
    ], expand=True)
