import streamlit as st
import pandas as pd

def render(df_procesado):
    """
    Renderiza el tab de Descarga de Información
    """
    st.header("⬇️ Descarga de Información")
    st.markdown("### 📥 Exportar datos procesados")
    
    # Obtener período más reciente para nombres de archivos
    ultimo_periodo = df_procesado['Periodo'].max()
    
    # Opciones de descarga
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Datos Completos")
        csv_completo = df_procesado.to_csv(index=False)
        st.download_button(
            label="💾 Descargar CSV Completo",
            data=csv_completo,
            file_name=f"datos_bcra_completos_{ultimo_periodo}.csv",
            mime="text/csv"
        )
        
        st.markdown("#### 🏆 Ranking Bancos")
        ranking_bancos = df_procesado[df_procesado['Periodo'] == ultimo_periodo].nlargest(10, 'Volumen de Negocio')
        csv_ranking = ranking_bancos.to_csv(index=False)
        st.download_button(
            label="💾 Descargar Ranking CSV",
            data=csv_ranking,
            file_name=f"ranking_bancos_{ultimo_periodo}.csv",
            mime="text/csv"
        )
    
    with col2:
        st.markdown("#### 💰 Solo Préstamos")
        prestamos_cols = ['Entidad', 'Nombre_Banco', 'Periodo'] + [col for col in df_procesado.columns if 'Prestamos' in col or 'prestamos' in col.lower()]
        df_prestamos_export = df_procesado[prestamos_cols]
        csv_prestamos = df_prestamos_export.to_csv(index=False)
        st.download_button(
            label="💾 Descargar Préstamos CSV",
            data=csv_prestamos,
            file_name=f"prestamos_bcra_{ultimo_periodo}.csv",
            mime="text/csv"
        )
        
        st.markdown("#### 💳 Solo Depósitos")
        depositos_cols = ['Entidad', 'Nombre_Banco', 'Periodo'] + [col for col in df_procesado.columns if 'Deposito' in col or 'deposito' in col.lower()]
        df_depositos_export = df_procesado[depositos_cols]
        csv_depositos = df_depositos_export.to_csv(index=False)
        st.download_button(
            label="💾 Descargar Depósitos CSV",
            data=csv_depositos,
            file_name=f"depositos_bcra_{ultimo_periodo}.csv",
            mime="text/csv"
        )
    
    # Información adicional
    st.markdown("### 📋 Información del Dataset")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Registros totales", len(df_procesado))
    with col2:
        st.metric("Columnas disponibles", len(df_procesado.columns))
    with col3:
        st.metric("Bancos únicos", df_procesado['Entidad'].nunique())
    with col4:
        st.metric("Períodos", f"{df_procesado['Periodo'].min()} - {df_procesado['Periodo'].max()}")