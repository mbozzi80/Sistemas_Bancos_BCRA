import streamlit as st
import pandas as pd
from ..graficos.utils import formatear_numero, calcular_ranking, filtrar_datos_por_periodo
from ..graficos.seaborn_plots import grafico_treemap_titulos, grafico_treemap_instrumentos_bcra, grafico_interactivo_titulos_rango
from ..graficos.utils import formatear_numero  # ← AGREGAR ESTA LÍNEA
from ..graficos.utils import obtener_siglas_para_bancos, obtener_sigla_banco


def render(df_procesado):
    """
    Renderiza el tab de Análisis de Títulos
    """
    st.header("📈 Análisis de Títulos")
    
    # Similar estructura a préstamos pero para títulos
    col1, col2 = st.columns(2)
    with col1:
        bancos_disponibles = ['Todos'] + sorted(df_procesado['Nombre_Banco'].dropna().unique().tolist())
        banco_seleccionado = st.selectbox("Seleccionar Banco", bancos_disponibles, key="titulos_banco")
    with col2:
        periodos_disponibles = sorted(df_procesado['Periodo'].unique(), reverse=True)
        periodo_seleccionado = st.selectbox("Seleccionar Período", periodos_disponibles, key="titulos_periodo")
    
    # Filtrar datos
    if banco_seleccionado != 'Todos':
        df_filtrado = df_procesado[
            (df_procesado['Nombre_Banco'] == banco_seleccionado) & 
            (df_procesado['Periodo'] == periodo_seleccionado)
        ]
    else:
        df_filtrado = df_procesado[df_procesado['Periodo'] == periodo_seleccionado]
    
    # Tabs secundarios
    tab1, tab2 = st.tabs(["Títulos Públicos y Privados", "Instrumentos BCRA"])
    
    with tab1:
        st.markdown("### Participación de Mercado por Títulos Públicos y Privados")
        grafico_treemap_titulos(df_filtrado)


        # Dentro del with tab1:
        st.markdown("### 📈 Serie Histórica - Títulos Públicos y Privados")

        # Convertir la columna 'Periodo' a tipo fecha y luego al formato 'YYYYMM'
        df_procesado = df_procesado.copy()
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
            key="titulos_historicos_rango"
        )

        # Convertir las fechas seleccionadas al formato 'YYYYMM'
        periodo_inicio = fecha_inicio.strftime('%Y%m')
        periodo_fin = fecha_fin.strftime('%Y%m')

        # Obtener los top 30 bancos del último período basados en Títulos públicos y privados
        ultimo_periodo = max(df_procesado['Periodo'])
        top_bancos_df = df_procesado[df_procesado['Periodo'] == ultimo_periodo].nlargest(30, 'Titulos públicos y privados')
        top_bancos = top_bancos_df['Nombre_Banco'].tolist()

        # Multiselect para seleccionar bancos
        bancos_seleccionados = st.multiselect(
            "Seleccionar bancos para visualizar:",
            options=top_bancos,
            default=top_bancos,
            format_func=obtener_sigla_banco,  # Usar la función centralizada para mostrar siglas
            key="multiselect_bancos_titulos"
        )

        # Si no hay bancos seleccionados, usar todos los top 10
        if not bancos_seleccionados:
            bancos_seleccionados = top_bancos

        # Llamar a la función para generar el gráfico interactivo
        fig = grafico_interactivo_titulos_rango(
            df_procesado, 
            periodo_inicio=periodo_inicio, 
            periodo_fin=periodo_fin,
            bancos_seleccionados=bancos_seleccionados
        )
        st.plotly_chart(fig, use_container_width=True)













    
    with tab2:
        st.markdown("### Participación de Mercado por Instrumentos BCRA")
        grafico_treemap_instrumentos_bcra(df_filtrado)


    # Columnas de títulos
    titulos_cols = [
        "Titulos públicos y privados", "Titulos públicos y privados ARS", "Titulos públicos y privados USD",
        "Tit pub a Costo + TIR", "Tit pub a VR", "Instrumentos BCRA", #"Letras BCRA",
    ]
    
    st.markdown("#### Composición de Títulos")
    
    if not df_filtrado.empty:
        cols_existentes = [col for col in titulos_cols if col in df_filtrado.columns]
        df_titulos = df_filtrado[['Nombre_Banco'] + cols_existentes].copy()
        
        # Ordenar por 'Titulos públicos y privados' de mayor a menor
        if 'Titulos públicos y privados' in df_titulos.columns:
            df_titulos = df_titulos.sort_values(by='Titulos públicos y privados', ascending=False)
    
        # Formatear números - TRANSFORMAR DIRECTAMENTE LAS COLUMNAS ORIGINALES
        for col in cols_existentes:
            df_titulos[col] = df_titulos[col].apply(lambda x: formatear_numero(x) if pd.notna(x) else "0")
        
        st.dataframe(df_titulos, use_container_width=True)
        
        # Métricas para un banco específico
        if banco_seleccionado != 'Todos' and len(df_filtrado) == 1:
            row = df_filtrado.iloc[0]
            col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
            with col1:
                st.metric("📈 Títulos Totales", f"${row['Titulos públicos y privados']:,.0f}")
            with col2:
                st.metric("💵 Títulos Pesos", f"${row["Titulos públicos y privados ARS"]:,.0f}")
            with col3:
                st.metric("💴 Títulos USD", f"${row["Titulos públicos y privados USD"]:,.0f}")
            with col4:
                st.metric("💴 Títulos Costo + TIR", f"${row["Tit pub a Costo + TIR"]:,.0f}")                
            with col5:
                st.metric("💴 Títulos VR", f"${row["Tit pub a VR"]:,.0f}")     
            with col6:
                st.metric("💴 Intrumentos BCRA", f"${row["Instrumentos BCRA"]:,.0f}") # aca reemplazar por "Letras BCRA"        
            with col7:
                participacion = (row['Titulos públicos y privados'] / row['Activo'] * 100) if row['Activo'] > 0 else 0
                st.metric("📊 % del Activo", f"{participacion:.1f}%")
    else:
        st.warning("No hay datos para mostrar con los filtros seleccionados")