import flet as ft
from src.core.config import load_config
from src.application.acta_service import ActaService
from src.ui.views.entrega_view import build_entrega_form
from src.ui.views.respaldo_view import build_respaldo_form
from src.ui.views.formateo_view import build_formateo_form
from src.ui.views.records_view import build_records_view
from src.ui.views.config_view import build_config_view

class AppNavigation:
    def __init__(self, page: ft.Page, service: ActaService):
        self.page = page
        self.service = service
        self.tech_config = load_config() or {"nombre_tecnico": "", "sede": ""}
        
        self.header_name = ft.Text(self.tech_config["nombre_tecnico"], weight=ft.FontWeight.W_500)
        self.header_sede = ft.Text(f"Sede: {self.tech_config['sede']}", size=12, color=ft.Colors.ON_SURFACE_VARIANT)
        self.content_area = ft.Container(expand=True, padding=20)

    def _update_config(self, new_config: dict):
        self.tech_config = new_config
        self.header_name.value = self.tech_config["nombre_tecnico"]
        self.header_sede.value = f"Sede: {self.tech_config['sede']}"
        self.page.update()

    def build_new_acta_view(self) -> ft.Column:
        tabs = ft.Tabs(
            length=3,
            selected_index=0,
            animation_duration=300,
            expand=True,
            content=ft.Column([
                ft.TabBar(
                    tabs=[
                        ft.Tab(label="Entrega", icon=ft.Icons.ASSIGNMENT_TURNED_IN),
                        ft.Tab(label="Respaldos", icon=ft.Icons.CLOUD_UPLOAD),
                        ft.Tab(label="Formateo / Cambio", icon=ft.Icons.SYNC_ALT),
                    ],
                ),
                ft.TabBarView(
                    expand=True,
                    controls=[
                        ft.Container(content=build_entrega_form(self.page, self.service), padding=20),
                        ft.Container(content=build_respaldo_form(self.page, self.service), padding=20),
                        ft.Container(content=build_formateo_form(self.page, self.service), padding=20),
                    ],
                ),
            ], expand=True),
        )
        return ft.Column([
            ft.Text("Nueva Acta", size=24, weight=ft.FontWeight.BOLD),
            ft.Text("Seleccione el tipo de acta y complete el formulario.",
                    size=13, color=ft.Colors.ON_SURFACE_VARIANT),
            ft.Container(height=4),
            tabs,
        ], expand=True)

    def show_view(self, index: int):
        if index == 0:
            self.content_area.content = self.build_new_acta_view()
        elif index == 1:
            self.content_area.content = build_records_view(self.page, self.service, lambda: self.show_view(1))
        elif index == 2:
            self.content_area.content = build_config_view(self.page, self.tech_config, self._update_config)
        self.page.update()

    def build(self) -> ft.Row:
        rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            min_extended_width=200,
            group_alignment=-0.9,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.Icons.ADD_CIRCLE_OUTLINE,
                    selected_icon=ft.Icons.ADD_CIRCLE,
                    label="Nueva Acta",
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.FOLDER_OUTLINED,
                    selected_icon=ft.Icons.FOLDER,
                    label="Actas Generadas",
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.SETTINGS_OUTLINED,
                    selected_icon=ft.Icons.SETTINGS,
                    label="Configuración",
                ),
            ],
            on_change=lambda e: self.show_view(e.control.selected_index),
        )

        header = ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.DESCRIPTION, color=ft.Colors.PRIMARY),
                ft.Text("Sistema de Actas", size=18, weight=ft.FontWeight.BOLD),
                ft.Container(expand=True),
                ft.Column([self.header_name, self.header_sede], spacing=0,
                          horizontal_alignment=ft.CrossAxisAlignment.END),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.padding.symmetric(horizontal=20, vertical=10),
            bgcolor=ft.Colors.SURFACE_CONTAINER,
            border_radius=ft.border_radius.only(bottom_left=15, bottom_right=15),
            margin=ft.margin.only(bottom=10)
        )

        # Initialize default view
        self.show_view(0)

        main_layout = ft.Column([
            header,
            self.content_area,
        ], expand=True, spacing=0)

        return ft.Row(
            [
                rail,
                ft.VerticalDivider(width=1),
                main_layout,
            ],
            expand=True,
        )
