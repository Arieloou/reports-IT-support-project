import flet as ft
from src.application.acta_service import ActaService
from src.ui.app import AppNavigation

def main(page: ft.Page):
    page.title = "Sistema de Actas - IT Support"
    page.window_width = 960
    page.window_height = 720
    page.padding = 0
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.INDIGO)

    # Inicializar servicios de aplicación
    service = ActaService()

    # Inicializar UI
    app = AppNavigation(page, service)
    
    page.add(app.build())

if __name__ == "__main__":
    ft.app(target=main)