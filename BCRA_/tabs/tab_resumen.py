import streamlit as st
import pandas as pd
from ..tools import obtener_resumen_datos_con_nombres
from ..graficos.seaborn_plots import grafico_evolucion_volumen_negocio, grafico_barras_top_bancos
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
    ranking_bancos = ranking_bancos.nlargest(10, 'Volumen de Negocio')
    
    # GUARDAR TOP 10 BANCOS PARA LOS GRÁFICOS
    top_10_bancos = ranking_bancos['Entidad'].tolist()
    
    # Crear tabla de ranking
    ranking_display = ranking_bancos[['Entidad', 'Nombre_Banco', 'Volumen de Negocio', 'Activo', 'Depositos', 'Prestamos', 'PN FINAL']].copy()
    ranking_display['Ranking'] = range(1, len(ranking_display) + 1)
    
    # Formatear números como moneda - TRANSFORMAR DIRECTAMENTE LAS COLUMNAS ORIGINALES
    ranking_display['Volumen de Negocio'] = ranking_display['Volumen de Negocio'].apply(formatear_numero)
    ranking_display['Activo'] = ranking_display['Activo'].apply(formatear_numero)
    ranking_display['Depositos'] = ranking_display['Depositos'].apply(formatear_numero)
    ranking_display['Prestamos'] = ranking_display['Prestamos'].apply(formatear_numero)
    ranking_display['PN FINAL'] = ranking_display['PN FINAL'].apply(formatear_numero)
    
    # Crear DataFrame para mostrar - USAR LAS COLUMNAS ORIGINALES
    tabla_ranking = ranking_display[['Ranking', 'Nombre_Banco', 'Volumen de Negocio', 'Activo', 'Depositos', 'Prestamos', 'PN FINAL']].copy()
    tabla_ranking.columns = ['🏆 Posición', '🏦 Banco', '💼 Volumen de Negocio', '💰 Activo Total', '💳 Depósitos', '💵 Préstamos', '📈 Patrimonio Neto']
    
    # Mostrar la tabla
    st.dataframe(tabla_ranking, use_container_width=True, hide_index=True)
    
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