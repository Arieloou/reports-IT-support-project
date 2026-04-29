from src.domain.models import TicketRecord
from src.domain.models import Device
from src.domain.models import Person
import flet as ft
from src.core.utils import clean_up_text
from src.domain.models import TransactionRecord
from src.application.acta_service import ActaService
from src.ui.components.common import make_date_row, do_search, show_popup_message

def build_entrega_form(page: ft.Page, service: ActaService) -> ft.Column:
    nombre = ft.TextField(label="Nombres")
    cedula = ft.TextField(label="Cédula")
    fecha, fila_fecha, cal_box = make_date_row(page)
    
    devices_list_col = ft.Column()
    device_forms = []

    def create_device_form(index):
        equipo = ft.TextField(label=f"Equipo {index}")
        marca = ft.TextField(label=f"Marca {index}")
        modelo = ft.TextField(label=f"Modelo {index}")
        codigo = ft.TextField(label=f"Código {index}")
        serie = ft.TextField(label=f"Número de Serie {index}")
        
        return {
            "equipo": equipo, "marca": marca, "modelo": modelo, "codigo": codigo, "serie": serie,
            "ui": ft.Column([
                ft.Text(f"Activo {index}", size=15, weight=ft.FontWeight.BOLD),
                equipo, marca, modelo, codigo, serie,
                ft.Divider()
            ])
        }

    def add_device(e):
        if len(device_forms) < 10:
            idx = len(device_forms) + 1
            new_form = create_device_form(idx)
            device_forms.append(new_form)
            devices_list_col.controls.append(new_form["ui"])
            if len(device_forms) >= 10:
                add_btn.disabled = True
            page.update()

    # Agregar el primer equipo por defecto
    first_form = create_device_form(1)
    device_forms.append(first_form)
    devices_list_col.controls.append(first_form["ui"])

    add_btn = ft.ElevatedButton("Agregar equipo (+)", icon=ft.Icons.ADD, on_click=add_device)

    ticket = ft.TextField(label="# Ticket")
    observaciones = ft.TextField(label="Observaciones", multiline=True, min_lines=2)

    search_btn = ft.IconButton(
        icon=ft.Icons.SEARCH, tooltip="Buscar cédula",
        on_click=lambda e: do_search(page, service, nombre, cedula)
    )
    fila_nombre = ft.Row([nombre, search_btn])

    def generar(e):
        devices = []
        for df in device_forms:
            d_type = clean_up_text(df["equipo"].value)
            brand = clean_up_text(df["marca"].value)
            model = clean_up_text(df["modelo"].value)
            udla = clean_up_text(df["codigo"].value)
            serial = clean_up_text(df["serie"].value)
            if d_type or brand or model or udla or serial:
                devices.append(Device(
                    device_type=d_type,
                    brand=brand,
                    model=model,
                    udla_code=udla,
                    serial_number=serial
                ))
        
        data = TransactionRecord(
            person=Person(name=clean_up_text(nombre.value), ci_document=clean_up_text(cedula.value)),
            devices=devices,
            ticket=TicketRecord(ticket=clean_up_text(ticket.value), observations=clean_up_text(observaciones.value)),
            date=clean_up_text(fecha.value),
        )
            
        success, msg = service.generate_entrega(data)
        show_popup_message(page, msg)

    return ft.Column([
        fila_nombre, cedula, fila_fecha, cal_box,
        ft.Divider(),
        devices_list_col,
        add_btn,
        ft.Divider(),
        ticket, observaciones,
        ft.Container(height=8),
        ft.Button("Generar Acta de Entrega", icon=ft.Icons.PICTURE_AS_PDF, on_click=generar),
    ], scroll=ft.ScrollMode.AUTO, spacing=10)
