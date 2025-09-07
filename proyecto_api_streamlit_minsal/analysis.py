
import pandas as pd

# Campos comunes que suelen estar presentes en la API de farmacias del MINSAL.
# La app detecta dinámicamente; esta lista es solo para ayudas y orden sugerido.
POSSIBLE_COLUMNS = [
    'local_id','local_nombre','comuna_nombre','localidad_nombre','local_direccion',
    'fk_region','fk_comuna','local_lat','local_lng','funcionamiento_hora_apertura',
    'funcionamiento_hora_cierre','funcionamiento_dia','telefono','local_telefono',
    'fecha','cadena','local_email'
]

def to_dataframe(json_obj):
    """Convierte la salida JSON (lista de dicts) a DataFrame, con columnas ordenadas cuando es posible."""
    if isinstance(json_obj, dict) and 'data' in json_obj:
        data = json_obj['data']
    else:
        data = json_obj
    df = pd.DataFrame(data)
    # Reordenar columnas con las comunes al inicio
    cols = list(df.columns)
    ordered = [c for c in POSSIBLE_COLUMNS if c in cols] + [c for c in cols if c not in POSSIBLE_COLUMNS]
    return df[ordered]

def coerce_types(df: pd.DataFrame):
    """Intenta convertir tipos útiles (numéricos, fechas/horas)."""
    for c in ['fk_region','fk_comuna','local_lat','local_lng']:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors='coerce')

    # fecha (si viene)
    if 'fecha' in df.columns:
        df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')

    # Horas como strings HH:MM -> convertir a datetime.time
    for c in ['funcionamiento_hora_apertura','funcionamiento_hora_cierre']:
        if c in df.columns:
            # Normalizar valores vacíos o 'null'
            s = df[c].astype(str).str.strip().str.replace('--','', regex=False)
            df[c] = pd.to_datetime(s, errors='coerce').dt.time
    return df

def resumen_basico(df: pd.DataFrame):
    """Retorna conteos útiles si existen las columnas esperadas."""
    out = {}
    if 'local_id' in df.columns:
        out['total_locales'] = int(df['local_id'].nunique())
    else:
        out['total_locales'] = int(len(df))
    if 'comuna_nombre' in df.columns:
        out['comunas_cubiertas'] = int(df['comuna_nombre'].nunique())
    if 'fk_region' in df.columns:
        out['regiones_cubiertas'] = int(df['fk_region'].nunique())
    if 'cadena' in df.columns:
        out['cadenas'] = int(df['cadena'].nunique())
    return out

def top_por_categoria(df: pd.DataFrame, cat_col: str, top_k=15):
    g = df.groupby(cat_col, dropna=False).size().reset_index(name='conteo')
    g = g.sort_values('conteo', ascending=False).head(top_k)
    return g

def abrir_vs_cerrar_promedio(df: pd.DataFrame, by_col='cadena'):
    """Si existen las columnas de horarios, calcula promedios por categoría."""
    if not {'funcionamiento_hora_apertura','funcionamiento_hora_cierre'}.issubset(df.columns):
        return None
    tmp = df.copy()
    for c in ['funcionamiento_hora_apertura','funcionamiento_hora_cierre']:
        tmp[c] = pd.to_datetime(tmp[c], errors='coerce')
    # Duración de jornada (si fecha no viene, asumimos mismo día)
    tmp['duracion_horas'] = (tmp['funcionamiento_hora_cierre'] - tmp['funcionamiento_hora_apertura']).dt.total_seconds() / 3600.0
    res = tmp.groupby(by_col, dropna=False)['duracion_horas'].mean().reset_index()
    res = res.dropna().sort_values('duracion_horas', ascending=False)
    return res
