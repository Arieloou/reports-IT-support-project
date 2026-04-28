def clean_up_text(texto):
    if not texto:
        return ""
    reemplazos = {
        "á":"a","é":"e","í":"i","ó":"o","ú":"u",
        "Á":"A","É":"E","Í":"I","Ó":"O","Ú":"U",
        "ñ":"n","Ñ":"N",
        "–":"-","—":"-","“":'"',"”":'"'
    }
    for k, v in reemplazos.items():
        texto = texto.replace(k, v)
    return texto

def standardize_name(nombre):
    """Normaliza un nombre: limpia, pasa a minúsculas y ordena las palabras."""
    palabras = clean_up_text(nombre).strip().lower().split()
    palabras.sort()
    return palabras
