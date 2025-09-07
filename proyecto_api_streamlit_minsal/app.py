
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from api_client import get_locales, get_turnos
from analysis import to_dataframe, coerce_types, resumen_basico, top_por_categoria, abrir_vs_cerrar_promedio
from charts import bar_top, line_by_date

st.set_page_config(page_title="Farmacias MINSAL - Análisis API", layout="wide")
st.title("Análisis y presentación de datos utilizando APIs en Python")
st.caption("Fuente: Ministerio de Salud (MIDAS/Farmanet). Endpoints publicados en datos.gob.cl")

with st.sidebar:
    st.header("Fuente de datos")
    fuente = st.radio("Selecciona endpoint", ["Listado de farmacias", "Farmacias de turno (hoy)"])
    if st.button("Cargar datos"):
        try:
            if fuente == "Listado de farmacias":
                data = get_locales()
            else:
                data = get_turnos()
            df = to_dataframe(data)
            df = coerce_types(df)
            st.session_state["df"] = df
            st.session_state["fuente"] = fuente
            st.success(f"Registros cargados: {len(df)}")
        except Exception as e:
            st.error(f"Error al consultar API: {e}")

if "df" in st.session_state:
    df = st.session_state["df"]
    fuente = st.session_state["fuente"]

    st.subheader("Vista previa")
    st.dataframe(df.head(50), use_container_width=True)

    st.subheader("Filtros")
    cols = st.columns(4)
    # Filtros comunes si existen
    with cols[0]:
        region_sel = None
        if "fk_region" in df.columns:
            regiones = ["(todas)"] + sorted([str(x) for x in df["fk_region"].dropna().unique()])
            region_pick = st.selectbox("Región (fk_region)", regiones)
            if region_pick != "(todas)":
                region_sel = int(region_pick)
    with cols[1]:
        comuna_sel = None
        if "comuna_nombre" in df.columns:
            comunas = ["(todas)"] + sorted(df["comuna_nombre"].dropna().unique().tolist())
            comuna_pick = st.selectbox("Comuna", comunas)
            if comuna_pick != "(todas)":
                comuna_sel = comuna_pick
    with cols[2]:
        cadena_sel = None
        if "cadena" in df.columns:
            cadenas = ["(todas)"] + sorted(df["cadena"].dropna().unique().tolist())
            cadena_pick = st.selectbox("Cadena", cadenas)
            if cadena_pick != "(todas)":
                cadena_sel = cadena_pick
    with cols[3]:
        texto = st.text_input("Buscar texto (nombre/dirección)")

    dff = df.copy()
    if region_sel is not None and "fk_region" in dff.columns:
        dff = dff[dff["fk_region"] == region_sel]
    if comuna_sel is not None and "comuna_nombre" in dff.columns:
        dff = dff[dff["comuna_nombre"] == comuna_sel]
    if cadena_sel is not None and "cadena" in dff.columns:
        dff = dff[dff["cadena"] == cadena_sel]
    if texto:
        mask = pd.Series(True, index=dff.index)
        for c in ["local_nombre","local_direccion","localidad_nombre"]:
            if c in dff.columns:
                mask &= dff[c].astype(str).str.contains(texto, case=False, na=False) | mask
        dff = dff[mask]

    st.markdown("**Registros filtrados**")
    st.dataframe(dff.head(100), use_container_width=True)
    st.write(f"Total filtrado: {len(dff)}")

    st.subheader("Indicadores")
    met = resumen_basico(dff)
    cols = st.columns(4)
    cols[0].metric("Locales", met.get("total_locales", len(dff)))
    cols[1].metric("Comunas", met.get("comunas_cubiertas", 0))
    cols[2].metric("Regiones", met.get("regiones_cubiertas", 0))
    cols[3].metric("Cadenas", met.get("cadenas", 0))

    st.subheader("Gráficos")
    c1, c2 = st.columns(2)
    with c1:
        if "comuna_nombre" in dff.columns:
            topk = st.slider("Top-k comunas", 5, 30, 10, key="top_comunas")
            g = top_por_categoria(dff, "comuna_nombre", topk)
            st.dataframe(g, use_container_width=True)
            fig = bar_top(g, "comuna_nombre", "conteo", f"Top {topk} comunas por cantidad de locales")
            st.pyplot(fig)
        elif "fk_region" in dff.columns:
            topk = st.slider("Top-k regiones", 5, 16, 10, key="top_regiones")
            g = top_por_categoria(dff, "fk_region", topk)
            st.dataframe(g, use_container_width=True)
            fig = bar_top(g, "fk_region", "conteo", f"Top {topk} regiones por cantidad de locales")
            st.pyplot(fig)
        else:
            st.info("No se encuentran columnas de comuna/región para graficar.")

    with c2:
        if "cadena" in dff.columns:
            topk2 = st.slider("Top-k cadenas", 5, 30, 10, key="top_cadenas")
            g2 = top_por_categoria(dff, "cadena", topk2)
            st.dataframe(g2, use_container_width=True)
            fig2 = bar_top(g2, "cadena", "conteo", f"Top {topk2} cadenas por cantidad de locales")
            st.pyplot(fig2)
        else:
            st.info("No hay columna 'cadena' para ranking.")

    # Si hubiera fechas (por ejemplo en turnos), graficar evolución
    if "fecha" in dff.columns:
        st.subheader("Series de tiempo (si aplica)")
        fig3 = line_by_date(dff, "fecha", "Evolución de registros por fecha")
        st.pyplot(fig3)

    st.divider()
    st.caption("Hecho con requests, json, pandas, matplotlib y streamlit.")
