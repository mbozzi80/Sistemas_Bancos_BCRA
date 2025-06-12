import streamlit as st
import pandas as pd
from ..graficos.utils import formatear_numero, calcular_ranking, filtrar_datos_por_periodo
from ..graficos.seaborn_plots import grafico_treemap_prestamos

def render(df):
    """Renderiza el tab de análisis de préstamos"""
    
    st.markdown("### 💰 Análisis de Préstamos")
    
    # Filtros
    col1, col2 = st.columns(2)
    
    with col1:
        periodo_selected = st.selectbox(
            "📅 Seleccionar Período:",
            options=sorted(df['Periodo'].unique(), reverse=True),
            key="prestamos_periodo"
        )
    
    with col2:
        top_n = st.slider(
            "🔢 Top N Bancos:",
            min_value=5, max_value=30, value=15,
            key="prestamos_top_n"
        )
    
    # Filtrar datos
    df_periodo = filtrar_datos_por_periodo(df, periodo_selected)
    
    if df_periodo.empty:
        st.warning("No hay datos para el período seleccionado")
        return
    
    # Columnas de préstamos (AGREGANDO LAS NUEVAS)
    columnas_prestamos = [
        'Nombre_Banco',
        'Prestamos',
        'Prestamos ARS',
        'Prestamos USD',
        'Prestamos SP ARS',
        'Prestamos SP USD',
        'Prestamos SPNF ARS',
        'Prestamos SPNF USD',
        'Prestamos Comerciales',
        'Prevision',
        # AGREGADAS: Préstamos detallados SPNF
        'Prestamos personales ARS',
        'Prestamos hipotecarios ARS + UVA',
        'Tarjetas de Crédito ARS',
        'Documentos descontados ARS',
        'Prefinancacion de Expor USD',
        'Doc a sola firma ARS',
        'Adelantos ARS',
        'Doc a sola firma USD',
        'Tarjetas de Crédito USD'
    ]
    
    # Verificar que todas las columnas existen
    columnas_existentes = [col for col in columnas_prestamos if col in df_periodo.columns]
    
    if len(columnas_existentes) < len(columnas_prestamos):
        columnas_faltantes = set(columnas_prestamos) - set(columnas_existentes)
        st.warning(f"⚠️ Columnas no encontradas: {', '.join(columnas_faltantes)}")
    
    # Ranking por total de préstamos
    ranking_prestamos = calcular_ranking(df_periodo, 'Prestamos', top_n)
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_prestamos = df_periodo['Prestamos'].sum()
        st.metric("💰 Total Préstamos", formatear_numero(total_prestamos))
    
    with col2:
        total_ars = df_periodo['Prestamos ARS'].sum()
        st.metric("🇦🇷 Préstamos ARS", formatear_numero(total_ars))
    
    with col3:
        total_usd = df_periodo['Prestamos USD'].sum()
        st.metric("💵 Préstamos USD", formatear_numero(total_usd))
    
    with col4:
        participacion_usd = (total_usd / total_prestamos * 100) if total_prestamos > 0 else 0
        st.metric("📊 % USD", f"{participacion_usd:.1f}%")
    
    # Tabs secundarios
    tab1, tab2, tab3 = st.tabs(["📊 Ranking", "🔍 Detalle por Banco", "📈 Cartera por Tipo"])
    
    with tab1:
        st.markdown("#### 🏆 Top Bancos por Préstamos Totales")
        
        # Llamar al gráfico de treemap
        grafico_treemap_prestamos(df_periodo)
            
        # Tabla con formato
        df_display = ranking_prestamos[columnas_existentes].copy()
        
        # Formatear columnas numéricas
        for col in columnas_existentes[1:]:  # Excluir 'Nombre_Banco'
            if col in df_display.columns:
                df_display[col] = df_display[col].apply(lambda x: formatear_numero(x) if pd.notna(x) else "0")
        
        st.dataframe(
            df_display,
            use_container_width=True,
            hide_index=True
        )
    
    with tab2:
        # Selector de banco
        banco_selected = st.selectbox(
            "🏦 Seleccionar Banco:",
            options=sorted(df_periodo['Nombre_Banco'].unique()),
            key="prestamos_banco_detail"
        )
        
        # Datos del banco seleccionado
        banco_data = df_periodo[df_periodo['Nombre_Banco'] == banco_selected]
        
        if not banco_data.empty:
            banco_info = banco_data.iloc[0]
            
            # Métricas del banco
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("💰 Total Préstamos", formatear_numero(banco_info['Prestamos']))
                st.metric("🇦🇷 Préstamos ARS", formatear_numero(banco_info['Prestamos ARS']))
                st.metric("💵 Préstamos USD", formatear_numero(banco_info['Prestamos USD']))
            
            with col2:
                if 'Prestamos personales ARS' in banco_info:
                    st.metric("👤 Personales ARS", formatear_numero(banco_info['Prestamos personales ARS']))
                if 'Prestamos hipotecarios ARS + UVA' in banco_info:
                    st.metric("🏠 Hipotecarios", formatear_numero(banco_info['Prestamos hipotecarios ARS + UVA']))
                if 'Tarjetas de Crédito ARS' in banco_info:
                    st.metric("💳 Tarjetas ARS", formatear_numero(banco_info['Tarjetas de Crédito ARS']))
            
            with col3:
                if 'Prestamos Comerciales' in banco_info:
                    st.metric("🏢 Comerciales", formatear_numero(banco_info['Prestamos Comerciales']))
                if 'Adelantos ARS' in banco_info:
                    st.metric("⚡ Adelantos", formatear_numero(banco_info['Adelantos ARS']))
                if 'Prevision' in banco_info:
                    st.metric("🛡️ Previsiones", formatear_numero(banco_info['Prevision']))
    
    with tab3:
        st.markdown("#### 📈 Composición de Cartera por Tipo")
        
        # Calcular participaciones por tipo de préstamo
        cartera_data = []
        
        tipos_prestamos = [
            ('Prestamos personales ARS', '👤 Personales ARS'),
            ('Prestamos hipotecarios ARS + UVA', '🏠 Hipotecarios'),
            ('Tarjetas de Crédito ARS', '💳 Tarjetas ARS'),
            ('Prestamos Comerciales', '🏢 Comerciales'),
            ('Adelantos ARS', '⚡ Adelantos ARS'),
            ('Doc a sola firma ARS', '📄 Doc. Sola Firma ARS'),
            ('Prefinancacion de Expor USD', '🌍 Prefinanc. Export'),
            ('Tarjetas de Crédito USD', '💳 Tarjetas USD')
        ]
        
        for col, nombre_display in tipos_prestamos:
            if col in df_periodo.columns:
                total_col = df_periodo[col].sum()
                participacion = (total_col / total_prestamos * 100) if total_prestamos > 0 else 0
                cartera_data.append({
                    'Tipo de Préstamo': nombre_display,
                    'Monto': total_col,
                    'Participación (%)': participacion
                })
        
        df_cartera = pd.DataFrame(cartera_data)
        df_cartera = df_cartera.sort_values('Monto', ascending=False)
        df_cartera['Monto'] = df_cartera['Monto'].apply(formatear_numero)
        df_cartera['Participación (%)'] = df_cartera['Participación (%)'].round(2)
        
        st.dataframe(df_cartera, use_container_width=True, hide_index=True)

        