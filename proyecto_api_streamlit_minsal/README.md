
# Análisis y presentación de datos (MINSAL Farmacias - datos.gob.cl)

**Objetivo:** Consumir la API pública del Ministerio de Salud (MIDAS/Farmanet) publicada en datos.gob.cl,
analizarla con pandas y presentar resultados en una app **Streamlit** con gráficos **matplotlib**.

## Endpoints usados
- Listado farmacias del país: `https://midas.minsal.cl/farmacia_v2/WS/getLocales.php`
- Farmacias de turno (hoy): `https://midas.minsal.cl/farmacia_v2/WS/getLocalesTurnos.php`

> Ambos endpoints están referenciados desde el Portal de Datos Abiertos de Chile (datos.gob.cl).

## Librerías (permitidas por pauta)
- requests, json, pandas, matplotlib, streamlit

## Instalación
```bash
pip install requests pandas matplotlib streamlit
```

## Ejecución
```bash
streamlit run app.py
```

## Cómo usar
1. En la barra lateral de la app, elige entre **Listado de farmacias** o **Farmacias de turno (hoy)** y presiona **Cargar datos**.
2. Usa los **filtros** (Región, Comuna, Cadena, texto) para explorar.
3. Revisa indicadores y gráficos (Top comunas/Top cadenas). Si el recurso trae `fecha`, verás además una **serie de tiempo**.
4. Exporta desde la tabla si lo necesitas (opción nativa de Streamlit/DataFrame).

## Entregables sugeridos
- Código completo (este repositorio).
- Capturas de la app funcionando con tus filtros y gráficos.
- Informe breve: objetivos, API utilizada, metodología de análisis (limpieza/casteos), resultados y conclusiones.
