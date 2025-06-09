import streamlit as st
import pandas as pd
from ..graficos.utils import formatear_numero, calcular_ranking, filtrar_datos_por_periodo

def render(df):
    """Renderiza el tab de análisis de depósitos"""
    
    st.markdown("### 💳 Análisis de Depósitos")
    
    # Filtros
    col1, col2 = st.columns(2)
    
    with col1:
        periodo_selected = st.selectbox(
            "📅 Seleccionar Período:",
            options=sorted(df['Periodo'].unique(), reverse=True),
            key="depositos_periodo"
        )
    
    with col2:
        top_n = st.slider(
            "🔢 Top N Bancos:",
            min_value=5, max_value=30, value=15,
            key="depositos_top_n"
        )
    
    # Filtrar datos
    df_periodo = filtrar_datos_por_periodo(df, periodo_selected)
    
    if df_periodo.empty:
        st.warning("No hay datos para el período seleccionado")
        return
    
    # Columnas de depósitos (AGREGANDO LAS NUEVAS)
    columnas_depositos = [
        'Nombre_Banco',
        'Depositos',
        'Depositos ARS',
        'Depositos USD', 
        'Depositos a la vista ARS',
        'Depositos a plazo ARS',
        'Depositos a la vista USD',
        'Depositos a plazo USD',
        # Sector Público
        'Cta Cte SP ARS',
        'Cta Cte SP USD',
        'Cja Ahorro SP ARS',
        'Cja Ahorro SP USD', 
        'Pzo Fijo SP ARS',
        'Pzo Fijo SP UVA',
        'Pzo Fijo SP USD',
        # AGREGADAS: Sector Privado No Financiero (SPNF)
        'Ctas Remuneradas SPNF',
        'Cta Cte ARS SPNF',
        'Cja Ahorro ARS SPNF',
        'Cja Ahorro USD SPNF',
        'Pzo Fijo ARS SPNF',
        'Pzo Fijo UVA SPNF',
        'Pzo Fijo USD SPNF'
    ]
    
    # Verificar que todas las columnas existen
    columnas_existentes = [col for col in columnas_depositos if col in df_periodo.columns]
    
    if len(columnas_existentes) < len(columnas_depositos):
        columnas_faltantes = set(columnas_depositos) - set(columnas_existentes)
        st.warning(f"⚠️ Columnas no encontradas: {', '.join(columnas_faltantes)}")
    
    # Ranking por total de depósitos
    ranking_depositos = calcular_ranking(df_periodo, 'Depositos', top_n)
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_depositos = df_periodo['Depositos'].sum()
        st.metric("💰 Total Depósitos", formatear_numero(total_depositos))
    
    with col2:
        total_ars = df_periodo['Depositos ARS'].sum() 
        st.metric("🇦🇷 Depósitos ARS", formatear_numero(total_ars))
    
    with col3:
        total_usd = df_periodo['Depositos USD'].sum()
        st.metric("💵 Depósitos USD", formatear_numero(total_usd))
    
    with col4:
        participacion_usd = (total_usd / total_depositos * 100) if total_depositos > 0 else 0
        st.metric("📊 % USD", f"{participacion_usd:.1f}%")
    
    # Tabs secundarios
    tab1, tab2, tab3 = st.tabs(["📊 Ranking", "🔍 Detalle por Banco", "📈 Estructura"])
    
    with tab1:
        st.markdown("#### 🏆 Top Bancos por Depósitos Totales")
        
        # Tabla con formato
        df_display = ranking_depositos[columnas_existentes].copy()
        
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
            key="depositos_banco_detail"
        )
        
        # Datos del banco seleccionado
        banco_data = df_periodo[df_periodo['Nombre_Banco'] == banco_selected]
        
        if not banco_data.empty:
            banco_info = banco_data.iloc[0]
            
            # Métricas del banco
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("💰 Total Depósitos", formatear_numero(banco_info['Depositos']))
                st.metric("🇦🇷 Depósitos ARS", formatear_numero(banco_info['Depositos ARS']))
                st.metric("💵 Depósitos USD", formatear_numero(banco_info['Depositos USD']))
            
            with col2:
                st.metric("👁️ Vista ARS", formatear_numero(banco_info['Depositos a la vista ARS']))
                st.metric("⏰ Plazo ARS", formatear_numero(banco_info['Depositos a plazo ARS']))
                if 'Cta Cte ARS SPNF' in banco_info:
                    st.metric("🏢 Cta Cte SPNF", formatear_numero(banco_info['Cta Cte ARS SPNF']))
            
            with col3:
                st.metric("👁️ Vista USD", formatear_numero(banco_info['Depositos a la vista USD']))
                st.metric("⏰ Plazo USD", formatear_numero(banco_info['Depositos a plazo USD']))
                if 'Cja Ahorro ARS SPNF' in banco_info:
                    st.metric("💰 Cja Ahorro SPNF", formatear_numero(banco_info['Cja Ahorro ARS SPNF']))
    
    with tab3:
        st.markdown("#### 📈 Estructura de Depósitos del Sistema")
        
        # Calcular participaciones
        estructura_data = []
        
        for col in ['Depositos ARS', 'Depositos USD', 'Depositos a la vista ARS', 
                   'Depositos a plazo ARS', 'Cta Cte ARS SPNF', 'Cja Ahorro ARS SPNF', 
                   'Pzo Fijo ARS SPNF']:
            if col in df_periodo.columns:
                total_col = df_periodo[col].sum()
                participacion = (total_col / total_depositos * 100) if total_depositos > 0 else 0
                estructura_data.append({
                    'Componente': col,
                    'Monto': total_col,
                    'Participación (%)': participacion
                })
        
        df_estructura = pd.DataFrame(estructura_data)
        df_estructura['Monto'] = df_estructura['Monto'].apply(formatear_numero)
        df_estructura['Participación (%)'] = df_estructura['Participación (%)'].round(2)
        
        st.dataframe(df_estructura, use_container_width=True, hide_index=True)


        