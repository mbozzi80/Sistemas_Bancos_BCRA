import streamlit as st
import pandas as pd
from ..tools import obtener_resumen_datos_con_nombres
import streamlit as st
import plotly.express as px
import pandas as pd
import datetime as dt
from ..tools import obtener_resumen_datos_con_nombres
from ..graficos.seaborn_plots import (
    grafico_evolucion_volumen_negocio,
    grafico_barras_top_bancos,
    grafico_interactivo_top_bancos_rango,
    grafico_treemap_volumen_negocio_total
)
from ..graficos.utils import formatear_numero  # ← AGREGAR ESTA LÍNEA
from ..graficos.utils import obtener_siglas_para_bancos, obtener_sigla_banco

def render(df_procesado):
    """
    Renderiza el tab de Resumen General
    """
    # st.header("📊 Resumen General del Sistema Bancario")
    
    # Filtros
    col1, col2 = st.columns(2)
    
    with col1:
        periodo_selected = st.selectbox(
            "📅 Seleccionar Período:",
            options=sorted(df_procesado['Periodo'].unique(), reverse=True),
            key="resumen_periodo"
        )
    
    with col2:
        top_n = st.slider(
            "🔢 Top N Bancos:",
            min_value=5, max_value=30, value=10,
            key="resumen_top_n"
        )
    
    # Filtrar datos según el período seleccionado
    df_periodo = df_procesado[df_procesado['Periodo'] == periodo_selected]
    
    if df_periodo.empty:
        st.warning("No hay datos para el período seleccionado")
        return
    
    # Mostrar resumen general
    # st.markdown("### 📋 Información General")
    # resumen = obtener_resumen_datos_con_nombres(df_periodo)
    # st.text(resumen)
    
    # Ranking Top N bancos por Volumen de Negocio
    st.markdown(f"### 🏆 Ranking Top {top_n} Bancos por Volumen de Negocio ({periodo_selected})")
    
    # Ordenar por Volumen de Negocio (descendente) y tomar los primeros N
    ranking_bancos_todos = df_periodo.copy()  # TODOS LOS BANCOS PARA TREEMAP
    ranking_bancos = df_periodo.nlargest(top_n, 'Volumen de Negocio')  # SOLO TOP N PARA TABLA
    
    # Crear tabla de ranking
    ranking_display = ranking_bancos[['Entidad', 'Nombre_Banco', 'Volumen de Negocio', 'Activo', 'Depositos', 'Prestamos', 'PN FINAL']].copy()
    ranking_display['Ranking'] = range(1, len(ranking_display) + 1)
    
    # Crear DataFrame para mostrar - SIN FORMATEAR AÚN
    tabla_ranking = ranking_display[['Ranking', 'Nombre_Banco', 'Volumen de Negocio', 'Activo', 'Depositos', 'Prestamos', 'PN FINAL']].copy()
    tabla_ranking.columns = ['🏆 Posición', '🏦 Banco', '💼 Volumen de Negocio', '💰 Activo Total', '💳 Depósitos', '💵 Préstamos', '📈 Patrimonio Neto']

    # FORMATEAR DESPUÉS DEL RENAME
    columnas_numericas = ['💼 Volumen de Negocio', '💰 Activo Total', '💳 Depósitos', '💵 Préstamos', '📈 Patrimonio Neto']
    for col in columnas_numericas:
        tabla_ranking[col] = tabla_ranking[col].apply(lambda x: formatear_numero(x) if pd.notna(x) else "0")

    # Mostrar la tabla
    st.dataframe(tabla_ranking, use_container_width=True, hide_index=True)
    
    # TREEMAP - PARTICIPACIÓN DE MERCADO (todos los bancos del período seleccionado)
    st.markdown("### 🌳 Treemap - Participación de Mercado")
    grafico_treemap_volumen_negocio_total(ranking_bancos_todos)
    
    # Métricas del sistema
    st.markdown("### 📊 Métricas del Sistema Bancario")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("📊 Total Bancos", f"{len(ranking_bancos)}")
    with col2:
        volumen_total = ranking_bancos['Volumen de Negocio'].sum()  # USAR VALORES ORIGINALES SIN FORMATO
        st.metric("💼 Volumen Total", formatear_numero(volumen_total))
    with col3:
        activo_total = ranking_bancos['Activo'].sum()  # USAR VALORES ORIGINALES
        st.metric("💰 Activo Total Sistema", formatear_numero(activo_total))
    with col4:
        depositos_total = ranking_bancos['Depositos'].sum()  # USAR VALORES ORIGINALES
        st.metric("💳 Depósitos Totales", formatear_numero(depositos_total))
    with col5:
        prestamos_total = ranking_bancos['Prestamos'].sum()
        st.metric("💵 Préstamos Totales", formatear_numero(prestamos_total))
    
    # Vista previa de datos
    st.markdown("### 🔍 Vista previa de datos estructurados")

    # Formatear la columna 'Periodo' para que se muestre como 'YYYY-MM'
    df_periodo_formateado = df_periodo.copy()
    df_periodo_formateado['Periodo'] = df_periodo_formateado['Periodo'].astype(str)

    # Mantener el orden original (de mayor a menor por Volumen de Negocio)
    df_periodo_formateado = df_periodo_formateado.sort_values(by='Volumen de Negocio', ascending=False)

    # Mostrar la tabla con el formato actualizado
    st.dataframe(df_periodo_formateado.head(10))

    # Separador visual
    st.markdown("---")

    # Título para el gráfico
    st.markdown("### 📈 Serie Histórica - Top 10 Bancos por Volumen de Negocio")

    # Convertir la columna 'Periodo' a tipo fecha y luego al formato 'YYYYMM'
    df_procesado['Periodo'] = pd.to_datetime(df_procesado['Periodo'].astype(str), format='%Y%m', errors='coerce')
    df_procesado['Periodo'] = df_procesado['Periodo'].dt.strftime('%Y%m')  # Convertir al formato 'YYYYMM'

    # Verificar si hay valores nulos después de la conversión
    if df_procesado['Periodo'].isnull().any():
        raise ValueError("Algunos valores en la columna 'Periodo' no pudieron ser convertidos al formato 'YYYYMM'. Verifica los datos.")

    # Convertir Periodo a datetime una sola vez
    periodos_date = pd.to_datetime(df_procesado['Periodo'].astype(str), format='%Y%m')
    
    # Crear lista ordenada de fechas únicas disponibles
    fechas_unicas = sorted(periodos_date.dt.date.unique())

    # Crear slider de rango con dos agarres
    fecha_inicio, fecha_fin = st.select_slider(
        "📅 Seleccionar Rango de Períodos:",
        options=fechas_unicas,
        value=(fechas_unicas[0], fechas_unicas[-1]),  # Por defecto selecciona todo el rango
        format_func=lambda x: x.strftime('%Y-%m'),    # Formato visual YYYY-MM
        key="serie_historica_rango"
    )

    # Convertir las fechas seleccionadas al formato 'YYYYMM'
    periodo_inicio = fecha_inicio.strftime('%Y%m')
    periodo_fin = fecha_fin.strftime('%Y%m')

    # Diccionario de siglas para los principales bancos
    banco_a_sigla = {
        "BANCO DE LA NACION ARGENTINA": "BNA",
        "BANCO DE GALICIA Y BUENOS AIRES S.A.U.": "GGAL",
        "BANCO SANTANDER ARGENTINA S.A.": "STDER",
        "BANCO DE LA PROVINCIA DE BUENOS AIRES": "BPBA",
        "BANCO BBVA ARGENTINA S.A.": "BBVA",
        "INDUSTRIAL AND COMMERCIAL BANK OF CHINA (ARGENTINA) S.A.U.": "ICBC",
        "BANCO MACRO S.A.": "MACRO",
        "BANCO PATAGONIA S.A.": "PTGA",
        "BANCO CREDICOOP COOPERATIVO LIMITADO": "COOP",
        "BANCO DE LA CIUDAD DE BUENOS AIRES": "CDAD"
    }

    # Obtener los top 10 bancos del último período
    ultimo_periodo = max(df_procesado['Periodo'])
    top_bancos_df = df_procesado[df_procesado['Periodo'] == ultimo_periodo].nlargest(10, 'Volumen de Negocio')
    top_bancos = top_bancos_df['Nombre_Banco'].tolist()

    # Multiselect para seleccionar bancos
    bancos_seleccionados = st.multiselect(
        "Seleccionar bancos para visualizar:",
        options=top_bancos,
        default=top_bancos,
        format_func=obtener_sigla_banco,  # Usar la función centralizada
        key="multiselect_bancos"
    )

    # Si no hay bancos seleccionados, usar todos los top 10
    if not bancos_seleccionados:
        bancos_seleccionados = top_bancos

    # Llamar a la función modificada para generar el gráfico interactivo
    fig = grafico_interactivo_top_bancos_rango(
        df_procesado, 
        periodo_inicio=periodo_inicio, 
        periodo_fin=periodo_fin,
        bancos_seleccionados=bancos_seleccionados
    )
    st.plotly_chart(fig, use_container_width=True)

