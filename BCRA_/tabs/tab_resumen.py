import streamlit as st
import pandas as pd
from ..tools import obtener_resumen_datos_con_nombres
import streamlit as st
import pandas as pd
from ..tools import obtener_resumen_datos_con_nombres
from ..graficos.seaborn_plots import (
    grafico_evolucion_volumen_negocio,
    grafico_barras_top_bancos,
    grafico_treemap_volumen_negocio,
    grafico_treemap_volumen_negocio__,
    grafico_treemap_top_30_bancos,
    grafico_treemap_top_10_bancos,
    grafico_treemap_volumen_negocio_total,
    grafico_pie_volumen_negocio  # ← IMPORTAR AQUÍ
)
from ..graficos.utils import formatear_numero  # ← AGREGAR ESTA LÍNEA


def render(df_procesado):
    """
    Renderiza el tab de Resumen General
    """
    st.header("📊 Resumen General del Sistema Bancario")
    
    # Mostrar resumen general
    st.markdown("### 📋 Información General")
    resumen = obtener_resumen_datos_con_nombres(df_procesado)
    st.text(resumen)
    
    # Ranking Top 10 bancos por Volumen de Negocio
    st.markdown("### 🏆 Ranking Top 10 Bancos por Volumen de Negocio (Febrero 2025)")
    
    # Obtener último período y filtrar
    ultimo_periodo = df_procesado['Periodo'].max()
    ranking_bancos = df_procesado[df_procesado['Periodo'] == ultimo_periodo].copy()
    
    # Ordenar por Volumen de Negocio (descendente) y tomar los primeros 10
    ranking_bancos_todos = ranking_bancos.copy()  # TODOS LOS BANCOS PARA TREEMAP
    ranking_bancos = ranking_bancos.nlargest(10, 'Volumen de Negocio')  # SOLO 10 PARA TABLA
    
    # GUARDAR TOP 10 BANCOS PARA LOS GRÁFICOS
    top_10_bancos = ranking_bancos['Entidad'].tolist()
    
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

    # Antes de línea 44, agregar:
    print(f"DEBUG: ranking_bancos_todos shape: {ranking_bancos_todos.shape}")
    print(f"DEBUG: ranking_bancos_todos columns: {ranking_bancos_todos.columns.tolist()}")
    print(f"DEBUG: Sample data:")
    print(ranking_bancos_todos[['Nombre_Banco', 'Volumen de Negocio']].head())

    # Mostrar la tabla
    st.dataframe(tabla_ranking, use_container_width=True, hide_index=True)
    
    # 1. TREEMAP - PARTICIPACIÓN DE MERCADO (todos los bancos del último período)
    # grafico_treemap_volumen_negocio__(ranking_bancos_todos)
    grafico_treemap_volumen_negocio_total(ranking_bancos_todos)
    # grafico_pie_volumen_negocio(ranking_bancos_todos)
    # grafico_treemap_top_10_bancos(ranking_bancos) 
    

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
    
    # ========== SECCIÓN DE GRÁFICOS ==========
    st.markdown("---")
    st.markdown("## 📈 Análisis Visual del Sistema Bancario")
    
    # 1. GRÁFICO DE LÍNEAS - EVOLUCIÓN TEMPORAL (120 MESES)
    grafico_evolucion_volumen_negocio(df_procesado, top_10_bancos, meses=120)
    
    # 2. TREEMAP - PARTICIPACIÓN DE MERCADO
    grafico_barras_top_bancos(ranking_bancos)
    
    # Vista previa de datos
    st.markdown("### 🔍 Vista previa de datos estructurados")
    st.dataframe(df_procesado.head(10))