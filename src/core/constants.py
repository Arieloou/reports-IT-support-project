import os

TEMPLATE_PATH = os.path.join("Report Templates", "ACTA ENTREGA.docx")
TEMPLATE_RESPALDO_PATH = os.path.join("Report Templates", "ACTA RESPALDO DE LA INFORMACIÓN DIGITAL.docx")
TEMPLATE_DEVOLUCION_PATH = os.path.join("Report Templates", "ACTA DEVOLUCIÓN.xlsx")
CONFIG_PATH = "config.json"
# DATA_FILE_PATH = "DATA.xlsx"
DATA_FILE_PATH = "//snfile01/Publico/Ariel/DATA.xlsx"

RECORD_FOLDERS = ["ACTAS DE ENTREGA", "ACTAS DE RESPALDO", "ACTAS DE DEVOLUCION"]

SEDES = ["UDLAPARK", "ARENA", "COLÓN"]

MESES = {
    1: "enero", 2: "febrero", 3: "marzo", 4: "abril",
    5: "mayo", 6: "junio", 7: "julio", 8: "agosto",
    9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre"
}
