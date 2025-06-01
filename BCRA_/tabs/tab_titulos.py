import streamlit as st
import pandas as pd

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
    
    # Columnas de títulos
    titulos_cols = [
        'Titulos públicos y privados', 'Titulos públicos y privados en pesos', 
        'Titulos públicos y privados en ME', 'Letras y Notas BCRA'
    ]
    
    st.markdown("### 📊 Composición de Títulos")
    
    if not df_filtrado.empty:
        cols_existentes = [col for col in titulos_cols if col in df_filtrado.columns]
        df_titulos = df_filtrado[['Nombre_Banco'] + cols_existentes].copy()
        
        # Formatear números - TRANSFORMAR DIRECTAMENTE LAS COLUMNAS ORIGINALES
        for col in cols_existentes:
            df_titulos[col] = df_titulos[col].apply(lambda x: f"${x:,.0f}")
        
        st.dataframe(df_titulos, use_container_width=True)
        
        # Métricas para un banco específico
        if banco_seleccionado != 'Todos' and len(df_filtrado) == 1:
            row = df_filtrado.iloc[0]
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("📈 Títulos Totales", f"${row['Titulos públicos y privados']:,.0f}")
            with col2:
                st.metric("💵 Títulos Pesos", f"${row['Titulos públicos y privados en pesos']:,.0f}")
            with col3:
                st.metric("💴 Títulos ME", f"${row['Titulos públicos y privados en ME']:,.0f}")
            with col4:
                participacion = (row['Titulos públicos y privados'] / row['Activo'] * 100) if row['Activo'] > 0 else 0
                st.metric("📊 % del Activo", f"{participacion:.1f}%")
    else:
        st.warning("No hay datos para mostrar con los filtros seleccionados")