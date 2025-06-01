import streamlit as st
import pandas as pd

def render(df_procesado):
    """
    Renderiza el tab de Análisis de Préstamos
    """
    st.header("💰 Análisis de Préstamos")
    
    # Selectores
    col1, col2 = st.columns(2)
    with col1:
        bancos_disponibles = ['Todos'] + sorted(df_procesado['Nombre_Banco'].dropna().unique().tolist())
        banco_seleccionado = st.selectbox("Seleccionar Banco", bancos_disponibles, key="prestamos_banco")
    with col2:
        periodos_disponibles = sorted(df_procesado['Periodo'].unique(), reverse=True)
        periodo_seleccionado = st.selectbox("Seleccionar Período", periodos_disponibles, key="prestamos_periodo")
    
    # Filtrar datos
    if banco_seleccionado != 'Todos':
        df_filtrado = df_procesado[
            (df_procesado['Nombre_Banco'] == banco_seleccionado) & 
            (df_procesado['Periodo'] == periodo_seleccionado)
        ]
    else:
        df_filtrado = df_procesado[df_procesado['Periodo'] == periodo_seleccionado]
    
    # Columnas de préstamos
    prestamos_cols = [
        'Prestamos', 'Prestamos totales', 'Prestamos en pesos', 'Prestamos en ME',
        'Prestamos sector publico no fcro pesos', 'Prestamos sector publico no fcro ME',
        'Prestamos sector privado no fcro pesos', 'Prestamos privado no fcro ME',
        'Prestamos Comerciales'
    ]
    
    # Mostrar análisis
    st.markdown("### 📊 Composición de Préstamos")
    
    if not df_filtrado.empty:
        # Seleccionar columnas que existen
        cols_existentes = [col for col in prestamos_cols if col in df_filtrado.columns]
        df_prestamos = df_filtrado[['Nombre_Banco'] + cols_existentes].copy()
        
        # Formatear números - TRANSFORMAR DIRECTAMENTE LAS COLUMNAS ORIGINALES
        for col in cols_existentes:
            df_prestamos[col] = df_prestamos[col].apply(lambda x: f"${x:,.0f}")
        
        st.dataframe(df_prestamos, use_container_width=True)
        
        # Métricas
        if banco_seleccionado != 'Todos' and len(df_filtrado) == 1:
            row = df_filtrado.iloc[0]
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("💰 Préstamos Totales", f"${row['Prestamos']:,.0f}")
            with col2:
                if 'Prestamos en pesos' in row:
                    st.metric("💵 Préstamos Pesos", f"${row['Prestamos en pesos']:,.0f}")
            with col3:
                if 'Prestamos en ME' in row:
                    st.metric("💴 Préstamos ME", f"${row['Prestamos en ME']:,.0f}")
            with col4:
                participacion = (row['Prestamos'] / row['Activo'] * 100) if row['Activo'] > 0 else 0
                st.metric("📊 % del Activo", f"{participacion:.1f}%")
    else:
        st.warning("No hay datos para mostrar con los filtros seleccionados")

        