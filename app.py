import streamlit as st
import pandas as pd
import requests
from io import StringIO
from BCRA_.tools import procesar_datos_bcra_con_nombres, obtener_resumen_datos_con_nombres

@st.cache_data
def load_data():
    """Descarga y carga el archivo h_imput.txt desde Dropbox"""
    url = "https://www.dropbox.com/scl/fi/xhbjjclp7sn33ak48nge5/h_imput.txt?rlkey=h3dfmnt9skshzdekrarvetnj1&st=ft0127ge&dl=1"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except Exception as e:
        st.error(f"Error al cargar el archivo: {e}")
        return None

# Configuración de la página
st.set_page_config(
    page_title="Sistema Bancario Argentino - BCRA",
    page_icon="🏦",
    layout="wide"
)

# Título principal
st.title("🏦 Sistema Bancario Argentino - BCRA")
st.markdown("**La primera plataforma web de análisis bancario argentino con 20 años de datos**")

# Cargar datos una sola vez
with st.spinner("Cargando datos del BCRA..."):
    texto_crudo = load_data()

if texto_crudo is not None:
    st.success("✅ Datos descargados correctamente!")
    
    with st.spinner("Procesando datos bancarios y cargando denominaciones..."):
        df_procesado = procesar_datos_bcra_con_nombres(texto_crudo)
    
    if df_procesado is not None:
        st.success("✅ Datos procesados correctamente con nombres de bancos!")
        
        # Crear las tabs/pestañas
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📊 Resumen General", 
            "💰 Préstamos", 
            "📈 Títulos", 
            "💳 Depósitos", 
            "📊 Ratios", 
            "⬇️ Descarga"
        ])
        
        # TAB 1: RESUMEN GENERAL - REEMPLAZAR DESDE LÍNEA 54 HASTA LÍNEA 104

        # TAB 1: RESUMEN GENERAL
        with tab1:
            st.header("📊 Resumen General del Sistema Bancario")
            
            # Mostrar resumen general
            st.markdown("### 📋 Información General")
            resumen = obtener_resumen_datos_con_nombres(df_procesado)
            st.text(resumen)
            
            # Ranking Top 10 bancos por Volumen de Negocio ← CAMBIO 1: Título corregido
            st.markdown("### 🏆 Ranking Top 10 Bancos por Volumen de Negocio (Febrero 2025)")
            
            # Obtener último período y filtrar
            ultimo_periodo = df_procesado['Periodo'].max()
            ranking_bancos = df_procesado[df_procesado['Periodo'] == ultimo_periodo].copy()
            
            # Ordenar por Volumen de Negocio (descendente) y tomar los primeros 10
            ranking_bancos = ranking_bancos.nlargest(10, 'Volumen de Negocio')
            
            # Crear tabla de ranking ← CAMBIO 2: Agregar 'PN FINAL'
            ranking_display = ranking_bancos[['Entidad', 'Nombre_Banco', 'Volumen de Negocio', 'Activo', 'Depositos', 'Prestamos', 'PN FINAL']].copy()
            ranking_display['Ranking'] = range(1, len(ranking_display) + 1)
            
            # Formatear números como moneda ← CAMBIO 3: Transformar directamente las columnas originales
            ranking_display['Volumen de Negocio'] = ranking_display['Volumen de Negocio'].apply(lambda x: f"${x:,.0f}")
            ranking_display['Activo'] = ranking_display['Activo'].apply(lambda x: f"${x:,.0f}")
            ranking_display['Depositos'] = ranking_display['Depositos'].apply(lambda x: f"${x:,.0f}")
            ranking_display['Prestamos'] = ranking_display['Prestamos'].apply(lambda x: f"${x:,.0f}")
            ranking_display['PN FINAL'] = ranking_display['PN FINAL'].apply(lambda x: f"${x:,.0f}")
            
            # Crear DataFrame para mostrar ← CAMBIO 4: Usar columnas originales
            tabla_ranking = ranking_display[['Ranking', 'Nombre_Banco', 'Volumen de Negocio', 'Activo', 'Depositos', 'Prestamos', 'PN FINAL']].copy()
            tabla_ranking.columns = ['🏆 Posición', '🏦 Banco', '💼 Volumen de Negocio', '💰 Activo Total', '💳 Depósitos', '💵 Préstamos', '📈 Patrimonio Neto']
            
            # Mostrar la tabla
            st.dataframe(tabla_ranking, use_container_width=True, hide_index=True)
            
            # Métricas del sistema ← CAMBIO 5: Agregar métrica de Volumen de Negocio
            st.markdown("### 📊 Métricas del Sistema Bancario")
            col1, col2, col3, col4, col5 = st.columns(5)  # ← 5 columnas en lugar de 4
            
            with col1:
                st.metric("📊 Total Bancos", f"{len(ranking_bancos)}")
            with col2:
                volumen_total = ranking_bancos['Volumen de Negocio'].sum()  # ← USAR VALORES ORIGINALES SIN FORMATO
                st.metric("💼 Volumen Total", f"${volumen_total:,.0f}")
            with col3:
                activo_total = ranking_bancos['Activo'].sum()  # ← USAR VALORES ORIGINALES
                st.metric("💰 Activo Total Sistema", f"${activo_total:,.0f}")
            with col4:
                depositos_total = ranking_bancos['Depositos'].sum()  # ← USAR VALORES ORIGINALES
                st.metric("💳 Depósitos Totales", f"${depositos_total:,.0f}")
            with col5:
                prestamos_total = ranking_bancos['Prestamos'].sum()  # ← USAR VALORES ORIGINALES
                st.metric("💵 Préstamos Totales", f"${prestamos_total:,.0f}")
            
            # Vista previa de datos
            st.markdown("### 🔍 Vista previa de datos estructurados")
            st.dataframe(df_procesado.head(10))
            
            # Vista previa de datos
            st.markdown("### 🔍 Vista previa de datos estructurados")
            st.dataframe(df_procesado.head(10))
        
        # TAB 2: PRÉSTAMOS
        with tab2:
            st.header("💰 Análisis de Préstamos")
            
            # Filtros
            col1, col2 = st.columns(2)
            with col1:
                bancos_disponibles = ['Todos'] + sorted(df_procesado['Nombre_Banco'].dropna().unique().tolist())
                banco_seleccionado = st.selectbox("Seleccionar Banco", bancos_disponibles)
            with col2:
                periodos_disponibles = sorted(df_procesado['Periodo'].unique(), reverse=True)
                periodo_seleccionado = st.selectbox("Seleccionar Período", periodos_disponibles)
            
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
                
                # Formatear números
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
                        st.metric("💵 Préstamos Pesos", f"${row['Prestamos en pesos']:,.0f}")
                    with col3:
                        st.metric("💴 Préstamos ME", f"${row['Prestamos en ME']:,.0f}")
                    with col4:
                        participacion = (row['Prestamos'] / row['Activo'] * 100) if row['Activo'] > 0 else 0
                        st.metric("📊 % del Activo", f"{participacion:.1f}%")
            else:
                st.warning("No hay datos para mostrar con los filtros seleccionados")
        
        # TAB 3: TÍTULOS
        with tab3:
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
                'Titulos públicos y privados',
                'Titulos públicos y privados en pesos',
                'Titulos públicos y privados en ME',
                'Letras y Notas BCRA'
            ]
            
            st.markdown("### 📊 Composición de Títulos")
            
            if not df_filtrado.empty:
                cols_existentes = [col for col in titulos_cols if col in df_filtrado.columns]
                df_titulos = df_filtrado[['Nombre_Banco'] + cols_existentes].copy()
                
                # Formatear números
                for col in cols_existentes:
                    df_titulos[col] = df_titulos[col].apply(lambda x: f"${x:,.0f}")
                
                st.dataframe(df_titulos, use_container_width=True)
            else:
                st.warning("No hay datos para mostrar con los filtros seleccionados")
        



        
        # TAB 4: DEPÓSITOS
        with tab4:
            st.header("💳 Análisis de Depósitos")
            
            # Similar estructura para depósitos
            col1, col2 = st.columns(2)
            with col1:
                bancos_disponibles = ['Todos'] + sorted(df_procesado['Nombre_Banco'].dropna().unique().tolist())
                banco_seleccionado = st.selectbox("Seleccionar Banco", bancos_disponibles, key="depositos_banco")
            with col2:
                periodos_disponibles = sorted(df_procesado['Periodo'].unique(), reverse=True)
                periodo_seleccionado = st.selectbox("Seleccionar Período", periodos_disponibles, key="depositos_periodo")
            
            # Filtrar datos
            if banco_seleccionado != 'Todos':
                df_filtrado = df_procesado[
                    (df_procesado['Nombre_Banco'] == banco_seleccionado) & 
                    (df_procesado['Periodo'] == periodo_seleccionado)
                ]
            else:
                df_filtrado = df_procesado[df_procesado['Periodo'] == periodo_seleccionado]
            
            # Columnas de depósitos
            depositos_cols = [
                'Depositos', 'Depositos en pesos', 'Depositos en ME',
                'Depositos a la vista $', 'Depositos a plazo $',
                'Depositos a la vista en ME', 'Depositos a plazo ME'
            ]
            
            st.markdown("### 📊 Composición de Depósitos")
            
            if not df_filtrado.empty:
                cols_existentes = [col for col in depositos_cols if col in df_filtrado.columns]
                df_depositos = df_filtrado[['Nombre_Banco'] + cols_existentes].copy()
                
                # Formatear números
                for col in cols_existentes:
                    df_depositos[col] = df_depositos[col].apply(lambda x: f"${x:,.0f}")
                
                st.dataframe(df_depositos, use_container_width=True)
            else:
                st.warning("No hay datos para mostrar con los filtros seleccionados")
        




        # TAB 5: RATIOS
        with tab5:
            st.header("📊 Ratios Financieros")
            st.markdown("### 🚧 En construcción...")
            st.info("Esta sección contendrá todos los ratios financieros calculados automáticamente.")
            
            # Preview de ratios disponibles
            from BCRA_.estructura_bcra import ratios_descripciones
            
            st.markdown("### 📋 Ratios Disponibles:")
            
            # Mostrar ratios por categorías
            categorias = {
                "🏗️ Estructura de Activos": ["I1", "I2", "I3", "I4", "I6", "I7"],
                "🏛️ Estructura Patrimonial": ["I8", "I9", "I10", "I11"],
                "💰 Cartera de Préstamos": ["I12", "I13", "I14", "I16"],
                "💧 Liquidez": ["I17", "I18", "I19"],
                "⚙️ Eficiencia": ["I20", "I21", "I22", "I24", "I27", "I29", "I30"],
                "📈 Otros Indicadores": ["I31", "I32", "I33", "I34", "I35", "I36", "I37", "I38", "I39", "I40", "I41", "I42", "I43"]
            }
            
            for categoria, ratios in categorias.items():
                st.markdown(f"#### {categoria}")
                for ratio in ratios:
                    if ratio in ratios_descripciones:
                        st.write(f"• **{ratio}**: {ratios_descripciones[ratio]}")
        





        # TAB 6: DESCARGA
        with tab6:
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
        
    else:
        st.error("❌ Error al procesar los datos")
else:
    st.error("❌ No se pudieron cargar los datos")

