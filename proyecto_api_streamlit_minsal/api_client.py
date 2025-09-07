
import requests

# Endpoints oficiales publicados en datos.gob.cl (MINSAL - MIDAS/Farmanet)
# Listado total de farmacias del país
URL_LOCALES = "https://midas.minsal.cl/farmacia_v2/WS/getLocales.php"
# Farmacias de turno (día actual)
URL_TURNOS = "https://midas.minsal.cl/farmacia_v2/WS/getLocalesTurnos.php"

def get_locales(timeout=60):
    """Obtiene el listado de farmacias del país (JSON).
    No requiere parámetros.
    """
    r = requests.get(URL_LOCALES, timeout=timeout)
    r.raise_for_status()
    return r.json()

def get_turnos(timeout=60):
    """Obtiene el listado de farmacias de turno del día (JSON).
    Documentado por datos.gob.cl como recurso JSON sin parámetros.
    """
    r = requests.get(URL_TURNOS, timeout=timeout)
    r.raise_for_status()
    return r.json()
