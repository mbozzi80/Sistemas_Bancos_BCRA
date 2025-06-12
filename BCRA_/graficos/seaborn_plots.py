import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
from .utils import configurar_estilo_seaborn, mostrar_grafico_streamlit, formatear_numero

def grafico_evolucion_volumen_negocio(df_procesado, top_10_bancos, meses=120):
    """
    Crea gráfico de líneas con evolución del Volumen de Negocio
    """
    # ... (mantener todo el código del gráfico de líneas - está perfecto)

def grafico_barras_top_bancos(ranking_bancos):
    """
    Crea gráfico de barras horizontal con Top 10 bancos (REEMPLAZO TEMPORAL DEL TREEMAP)
    """
    st.markdown("### 📊 Top 10 Bancos por Volumen de Negocio")
    
    configurar_estilo_seaborn()
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Crear gráfico de barras horizontal con los valores originales
    df_plot = ranking_bancos.head(10).copy()
    
    # ORDENAR POR VOLUMEN DE NEGOCIO (menor a mayor para que aparezca bien con invert_yaxis)
    df_plot = df_plot.sort_values('Volumen de Negocio', ascending=True)
    
    sns.barplot(
        data=df_plot,
        x='Volumen de Negocio',
        y='Nombre_Banco',
        hue='Nombre_Banco',  # ← Agregar esta línea
        palette='viridis',
        legend=False,        # ← Agregar esta línea
        ax=ax
    )
    
    ax.set_title('Top 10 Bancos por Volumen de Negocio', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Volumen de Negocio (en millones)', fontsize=12)
    ax.set_ylabel('Bancos', fontsize=12)
    
    # Formatear eje X en millones
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1_000_000:.0f}M'))
    
    # Invertir orden para que el mayor esté arriba
    ax.invert_yaxis()
    
    plt.tight_layout()
    mostrar_grafico_streamlit(fig, "")


def grafico_treemap_volumen_negocio(ranking_bancos):
    """
    Crea treemap con participación de mercado por Volumen de Negocio usando Plotly
    """
    st.markdown("#### Participación de Mercado por Volumen de Negocio")
    
    try:
        import plotly.express as px
        import numpy as np
        
        # Preparar datos para treemap
        df_treemap = ranking_bancos[['Nombre_Banco', 'Volumen de Negocio']].copy()
        df_treemap = df_treemap.dropna()
        df_treemap = df_treemap[df_treemap['Volumen de Negocio'] > 0]
        
        # MAPEO DE BANCOS PRINCIPALES CON COLORES CORPORATIVOS
        bancos_principales = {
            'BANCO DE LA NACION ARGENTINA': {'nombre': 'BNA', 'color': '#87CEEB'},
            'BANCO DE GALICIA Y BUENOS AIRES S.A.U.': {'nombre': 'GALICIA', 'color': '#FF8C00'},
            'BANCO SANTANDER ARGENTINA S.A.': {'nombre': 'SANTANDER', 'color': '#DC143C'},
            'BANCO BBVA ARGENTINA S.A.': {'nombre': 'BBVA', 'color': '#0066CC'},
            'BANCO DE LA PROVINCIA DE BUENOS AIRES': {'nombre': 'BPBA', 'color': '#228B22'},
            'BANCO MACRO S.A.': {'nombre': 'MACRO', 'color': '#1E90FF'},
            'INDUSTRIAL AND COMMERCIAL BANK OF CHINA (ARGENTINA) S.A.U.': {'nombre': 'ICBC', 'color': '#4169E1'},
            'BANCO PATAGONIA S.A.': {'nombre': 'PATAGONIA', 'color': '#8B4513'},
            'BANCO CREDICOOP COOPERATIVO LIMITADO': {'nombre': 'CREDICOOP', 'color': '#9932CC'},
            'BANCO DE LA CIUDAD DE BUENOS AIRES': {'nombre': 'CIUDAD', 'color': '#FF6347'}
        }
        
        # Procesar bancos principales
        bancos_procesados = []
        volumen_otros = 0
        
        for idx, row in df_treemap.iterrows():
            banco_original = row['Nombre_Banco']
            volumen = row['Volumen de Negocio']
            
            if banco_original in bancos_principales:
                bancos_procesados.append({
                    'Nombre_Corto': bancos_principales[banco_original]['nombre'],
                    'Volumen de Negocio': volumen,
                    'Color': bancos_principales[banco_original]['color']
                })
            else:
                volumen_otros += volumen
        
        # Agregar "OTROS"
        if volumen_otros > 0:
            bancos_procesados.append({
                'Nombre_Corto': 'OTROS',
                'Volumen de Negocio': volumen_otros,
                'Color': '#B0B0B0'
            })
        
        # Crear DataFrame
        df_final = pd.DataFrame(bancos_procesados)
        df_final = df_final.sort_values('Volumen de Negocio', ascending=False)
        
        # Calcular porcentajes
        total_volumen = df_final['Volumen de Negocio'].sum()
        df_final['Porcentaje'] = (df_final['Volumen de Negocio'] / total_volumen * 100).round(1)
        
        # Crear treemap con Plotly
        fig = px.treemap(
            df_final,
            values='Volumen de Negocio',
            names='Nombre_Corto',
            title='🏦 Participación de Mercado - Sistema Bancario Argentino<br>(Por Volumen de Negocio)',
            color='Nombre_Corto',
            color_discrete_map=dict(zip(df_final['Nombre_Corto'], df_final['Color']))
        )
        
        # Personalizar
        fig.update_traces(
            textinfo="label+percent+value",
            texttemplate='<b>%{label}</b><br>%{percent}<br>$%{value:.1s}B',
            textfont_size=12,
            textfont_color="white"
        )
        
        fig.update_layout(
            height=600,
            font_family="Arial",
            title_font_size=18,
            title_x=0.5
        )
        
        # Mostrar con Streamlit
        st.plotly_chart(fig, use_container_width=True)
        
        # Información adicional
        st.info(f"📊 **{len(df_final)} categorías** | Volumen total: ${total_volumen/1e12:.2f} billones")
        
    except Exception as e:
        st.error(f"❌ Error al crear treemap: {e}")
        grafico_barras_top_bancos(ranking_bancos)

        
def grafico_pie_volumen_negocio(ranking_bancos):
    """
    Crea un gráfico de pie interactivo con la participación de mercado por Volumen de Negocio usando Plotly
    """
    st.markdown("##### Participación de Mercado por Volumen de Negocio")

    try:
        # Preparar datos para el gráfico de pie
        df_pie = ranking_bancos[['Nombre_Banco', 'Volumen de Negocio']].copy()
        df_pie = df_pie.dropna()
        df_pie = df_pie[df_pie['Volumen de Negocio'] > 0]

        # Crear gráfico de pie con Plotly
        fig = px.pie(
            df_pie,
            values='Volumen de Negocio',
            names='Nombre_Banco',
            title='🏦 Participación de Mercado - Sistema Bancario Argentino<br>(Por Volumen de Negocio)',
            color_discrete_sequence=px.colors.sequential.Viridis
        )

        # Personalizar el gráfico
        fig.update_traces(
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>Volumen: $%{value:,.0f}<br>Porcentaje: %{percent}',
            textfont_size=12
        )

        fig.update_layout(
            height=600,
            font_family="Arial",
            title_font_size=18,
            title_x=0.5
        )

        # Mostrar el gráfico en Streamlit
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Error al crear el gráfico de pie: {e}")


def grafico_treemap_volumen_negocio__(ranking_bancos):
    """
    Crea un treemap interactivo con la participación de mercado por Volumen de Negocio usando Plotly
    """
    st.markdown("##### Participación de Mercado por Volumen de Negocio")

    try:
        # Preparar datos para el treemap
        df_treemap = ranking_bancos[['Nombre_Banco', 'Volumen de Negocio']].copy()
        df_treemap = df_treemap.dropna()
        df_treemap = df_treemap[df_treemap['Volumen de Negocio'] > 0]

        # Ordenar por Volumen de Negocio (descendente)
        df_treemap = df_treemap.sort_values('Volumen de Negocio', ascending=False)

        # Separar los últimos 30 bancos en "OTROS"
        df_principales = df_treemap.iloc[:-30]  # Todos menos los últimos 30
        df_otros = df_treemap.iloc[-30:]       # Últimos 30 bancos

        # Calcular la participación total de "OTROS"
        volumen_otros = df_otros['Volumen de Negocio'].sum()

        # Crear DataFrame para "OTROS"
        df_otros_agrupado = pd.DataFrame({
            'Nombre_Banco': ['OTROS'],
            'Volumen de Negocio': [volumen_otros]
        })

        # Concatenar principales y "OTROS", forzando "OTROS" al final
        df_final = pd.concat([df_principales, df_otros_agrupado], ignore_index=True)

        # Reordenar para que "OTROS" esté al final
        df_final['Orden'] = df_final['Nombre_Banco'].apply(lambda x: 1 if x == 'OTROS' else 0)
        df_final = df_final.sort_values(by=['Orden', 'Volumen de Negocio'], ascending=[True, False]).drop(columns=['Orden'])

        # Calcular porcentajes
        total_volumen = df_final['Volumen de Negocio'].sum()
        df_final['Porcentaje'] = (df_final['Volumen de Negocio'] / total_volumen * 100).round(1)

        # Crear treemap con Plotly
        fig = px.treemap(
            df_final,
            path=['Nombre_Banco'],  # Jerarquía: solo bancos
            values='Volumen de Negocio',
            title='🏦 Participación de Mercado - Sistema Bancario Argentino<br>(Por Volumen de Negocio)',
            color='Volumen de Negocio',
            color_continuous_scale=px.colors.sequential.Viridis
        )

        # Personalizar el gráfico
        fig.update_traces(
            hovertemplate='<b>%{label}</b><br>Volumen: $%{value:,.0f}<br>Porcentaje: %{percentRoot:.1%}',
            textinfo='label+percent entry',
            textfont_size=12
        )

        fig.update_layout(
            height=600,
            font_family="Arial",
            title_font_size=18,
            title_x=0.5
        )

        # Mostrar el gráfico en Streamlit
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Error al crear el treemap: {e}")


def grafico_treemap_top_30_bancos(ranking_bancos):
    """
    Crea un treemap interactivo con los 30 principales bancos por Volumen de Negocio.
    La participación se calcula sobre el total del volumen de negocio.
    """
    st.markdown("##### Participación de Mercado - Top 30 Bancos por Volumen de Negocio")

    try:
        # Preparar datos para el treemap
        df_treemap = ranking_bancos[['Nombre_Banco', 'Volumen de Negocio']].copy()
        df_treemap = df_treemap.dropna()
        df_treemap = df_treemap[df_treemap['Volumen de Negocio'] > 0]

        # Ordenar por Volumen de Negocio (descendente) y tomar los 30 principales
        df_treemap = df_treemap.sort_values('Volumen de Negocio', ascending=False).head(30)

        # Renombrar bancos según el mapeo proporcionado
        bancos_principales = {
            'BANCO DE LA NACION ARGENTINA': 'BNA',
            'BANCO DE GALICIA Y BUENOS AIRES S.A.U.': 'GALICIA',
            'BANCO SANTANDER ARGENTINA S.A.': 'SANTANDER',
            'BANCO BBVA ARGENTINA S.A.': 'BBVA',
            'BANCO DE LA PROVINCIA DE BUENOS AIRES': 'BPBA',
            'BANCO MACRO S.A.': 'MACRO',
            'INDUSTRIAL AND COMMERCIAL BANK OF CHINA (ARGENTINA) S.A.U.': 'ICBC',
            'BANCO PATAGONIA S.A.': 'PATAGONIA',
            'BANCO CREDICOOP COOPERATIVO LIMITADO': 'CREDICOOP',
            'BANCO DE LA CIUDAD DE BUENOS AIRES': 'CIUDAD'
        }

        df_treemap['Nombre_Banco'] = df_treemap['Nombre_Banco'].replace(bancos_principales)

        # Calcular porcentajes sobre el total del volumen de negocio
        total_volumen = ranking_bancos['Volumen de Negocio'].sum()
        df_treemap['Porcentaje'] = (df_treemap['Volumen de Negocio'] / total_volumen * 100).round(1)

        # Crear treemap con Plotly
        fig = px.treemap(
            df_treemap,
            path=['Nombre_Banco'],  # Jerarquía: solo bancos
            values='Volumen de Negocio',
            title='🏦 Participación de Mercado - Top 30 Bancos por Volumen de Negocio<br>(Calculado sobre el total)',
            color='Volumen de Negocio',
            color_continuous_scale=px.colors.sequential.Viridis
        )

        # Personalizar el gráfico
        fig.update_traces(
            hovertemplate='<b>%{label}</b><br>Volumen: $%{value:,.0f}<br>Porcentaje: %{percentRoot:.1%}',
            textinfo='label+percent entry',
            textfont_size=12
        )

        fig.update_layout(
            height=600,
            font_family="Arial",
            title_font_size=18,
            title_x=0.5
        )

        # Mostrar el gráfico en Streamlit
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Error al crear el treemap: {e}")



def grafico_treemap_top_10_bancos(ranking_bancos):
    """
    Crea un treemap interactivo con los 10 principales bancos por Volumen de Negocio.
    La participación se calcula sobre el total del volumen de negocio de todos los bancos.
    """
    st.markdown("##### Participación de Mercado - Top 10 Bancos por Volumen de Negocio")

    try:
        # Preparar datos para el treemap
        df_treemap = ranking_bancos[['Nombre_Banco', 'Volumen de Negocio']].copy()
        df_treemap = df_treemap.dropna()
        df_treemap = df_treemap[df_treemap['Volumen de Negocio'] > 0]

        # Ordenar por Volumen de Negocio (descendente) y tomar los 10 principales
        df_treemap = df_treemap.sort_values('Volumen de Negocio', ascending=False).head(10)

        # Renombrar bancos según el mapeo proporcionado
        bancos_principales = {
            'BANCO DE LA NACION ARGENTINA': 'BNA',
            'BANCO DE GALICIA Y BUENOS AIRES S.A.U.': 'GALICIA',
            'BANCO SANTANDER ARGENTINA S.A.': 'SANTANDER',
            'BANCO BBVA ARGENTINA S.A.': 'BBVA',
            'BANCO DE LA PROVINCIA DE BUENOS AIRES': 'BPBA',
            'BANCO MACRO S.A.': 'MACRO',
            'INDUSTRIAL AND COMMERCIAL BANK OF CHINA (ARGENTINA) S.A.U.': 'ICBC',
            'BANCO PATAGONIA S.A.': 'PATAGONIA',
            'BANCO CREDICOOP COOPERATIVO LIMITADO': 'CREDICOOP',
            'BANCO DE LA CIUDAD DE BUENOS AIRES': 'CIUDAD'
        }

        df_treemap['Nombre_Banco'] = df_treemap['Nombre_Banco'].replace(bancos_principales)

        # Calcular porcentajes sobre el total del volumen de negocio
        total_volumen = ranking_bancos['Volumen de Negocio'].sum()
        df_treemap['Porcentaje'] = (df_treemap['Volumen de Negocio'] / total_volumen * 100).round(1)

        # Crear treemap con Plotly
        fig = px.treemap(
            df_treemap,
            path=['Nombre_Banco'],  # Jerarquía: solo bancos
            values='Volumen de Negocio',
            title='🏦 Participación de Mercado - Top 10 Bancos por Volumen de Negocio<br>(Calculado sobre el total)',
            color='Volumen de Negocio',
            color_continuous_scale=px.colors.sequential.Viridis
        )

        # Personalizar el gráfico
        fig.update_traces(
            hovertemplate='<b>%{label}</b><br>Volumen: $%{value:,.0f}<br>Porcentaje: %{percentRoot:.1%}',
            textinfo='label+percent entry',
            textfont_size=12
        )

        fig.update_layout(
            height=600,
            font_family="Arial",
            title_font_size=18,
            title_x=0.5
        )

        # Mostrar el gráfico en Streamlit
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Error al crear el treemap: {e}")



def grafico_treemap_volumen_negocio_total(ranking_bancos):
    """
    Crea un treemap interactivo con la participación de mercado por Volumen de Negocio usando Plotly.
    Muestra todos los bancos sin agrupar.
    """
    st.markdown("##### Participación de Mercado por Volumen de Negocio")

    try:
        # Preparar datos para el treemap
        df_treemap = ranking_bancos[['Nombre_Banco', 'Volumen de Negocio']].copy()
        df_treemap = df_treemap.dropna()
        df_treemap = df_treemap[df_treemap['Volumen de Negocio'] > 0]

        # Ordenar por Volumen de Negocio (descendente)
        df_treemap = df_treemap.sort_values('Volumen de Negocio', ascending=False)

        # Calcular porcentajes sobre el total del volumen de negocio
        total_volumen = df_treemap['Volumen de Negocio'].sum()
        df_treemap['Porcentaje'] = (df_treemap['Volumen de Negocio'] / total_volumen * 100).round(1)

        # Crear treemap con Plotly
        fig = px.treemap(
            df_treemap,
            path=['Nombre_Banco'],  # Jerarquía: solo bancos
            values='Volumen de Negocio',
            title='🏦 Participación de Mercado - Sistema Bancario Argentino<br>(Por Volumen de Negocio)',
            color='Volumen de Negocio',
            color_continuous_scale=px.colors.sequential.Viridis
        )

        # Personalizar el gráfico
        fig.update_traces(
            hovertemplate='<b>%{label}</b><br>Volumen: $%{value:,.0f}<br>Porcentaje: %{percentRoot:.1%}',
            textinfo='label+percent entry',
            textfont_size=12
        )

        fig.update_layout(
            height=600,
            font_family="Arial",
            title_font_size=18,
            title_x=0.5
        )

        # Mostrar el gráfico en Streamlit
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Error al crear el treemap: {e}")


def grafico_treemap_prestamos(ranking_bancos):
    """
    Crea un treemap interactivo con la participación de mercado por Préstamos usando Plotly.
    """
    st.markdown("##### Participación de Mercado por Préstamos")

    try:
        # Preparar datos para el treemap
        df_treemap = ranking_bancos[['Nombre_Banco', 'Prestamos']].copy()
        df_treemap = df_treemap.dropna()
        df_treemap = df_treemap[df_treemap['Prestamos'] > 0]

        # Ordenar por Préstamos (descendente)
        df_treemap = df_treemap.sort_values('Prestamos', ascending=False)

        # Calcular porcentajes sobre el total de préstamos
        total_prestamos = df_treemap['Prestamos'].sum()
        df_treemap['Porcentaje'] = (df_treemap['Prestamos'] / total_prestamos * 100).round(1)

        # Crear treemap con Plotly
        fig = px.treemap(
            df_treemap,
            path=['Nombre_Banco'],  # Jerarquía: solo bancos
            values='Prestamos',
            title='🏦 Participación de Mercado - Sistema Bancario Argentino<br>(Por Préstamos)',
            color='Prestamos',
            color_continuous_scale=px.colors.sequential.Viridis
        )

        # Personalizar el gráfico
        fig.update_traces(
            hovertemplate='<b>%{label}</b><br>Préstamos: $%{value:,.0f}<br>Porcentaje: %{percentRoot:.1%}',
            textinfo='label+percent entry',
            textfont_size=12
        )

        fig.update_layout(
            height=600,
            font_family="Arial",
            title_font_size=18,
            title_x=0.5
        )

        # Mostrar el gráfico en Streamlit
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Error al crear el treemap: {e}")


def grafico_treemap_depositos(ranking_bancos):
    """
    Crea un treemap interactivo con la participación de mercado por Depósitos usando Plotly.
    """
    st.markdown("##### Participación de Mercado por Depósitos")

    try:
        # Preparar datos para el treemap
        df_treemap = ranking_bancos[['Nombre_Banco', 'Depositos']].copy()
        df_treemap = df_treemap.dropna()
        df_treemap = df_treemap[df_treemap['Depositos'] > 0]

        # Ordenar por Depósitos (descendente)
        df_treemap = df_treemap.sort_values('Depositos', ascending=False)

        # Calcular porcentajes sobre el total de depósitos
        total_depositos = df_treemap['Depositos'].sum()
        df_treemap['Porcentaje'] = (df_treemap['Depositos'] / total_depositos * 100).round(1)

        # Crear treemap con Plotly
        fig = px.treemap(
            df_treemap,
            path=['Nombre_Banco'],  # Jerarquía: solo bancos
            values='Depositos',
            title='🏦 Participación de Mercado - Sistema Bancario Argentino<br>(Por Depósitos)',
            color='Depositos',
            color_continuous_scale=px.colors.sequential.Viridis
        )

        # Personalizar el gráfico
        fig.update_traces(
            hovertemplate='<b>%{label}</b><br>Depósitos: $%{value:,.0f}<br>Porcentaje: %{percentRoot:.1%}',
            textinfo='label+percent entry',
            textfont_size=12
        )

        fig.update_layout(
            height=600,
            font_family="Arial",
            title_font_size=18,
            title_x=0.5
        )

        # Mostrar el gráfico en Streamlit
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Error al crear el treemap: {e}")


        
def grafico_treemap_titulos(ranking_bancos):
    """
    Crea un treemap interactivo con la participación de mercado por Títulos Públicos y Privados usando Plotly.
    """
    st.markdown("##### Participación de Mercado por Títulos Públicos y Privados")

    try:
        # Preparar datos para el treemap
        df_treemap = ranking_bancos[['Nombre_Banco', 'Titulos públicos y privados']].copy()
        df_treemap = df_treemap.dropna()
        df_treemap = df_treemap[df_treemap['Titulos públicos y privados'] > 0]

        # Ordenar por Títulos Públicos y Privados (descendente)
        df_treemap = df_treemap.sort_values('Titulos públicos y privados', ascending=False)

        # Calcular porcentajes sobre el total de títulos
        total_titulos = df_treemap['Titulos públicos y privados'].sum()
        df_treemap['Porcentaje'] = (df_treemap['Titulos públicos y privados'] / total_titulos * 100).round(1)

        # Crear treemap con Plotly
        fig = px.treemap(
            df_treemap,
            path=['Nombre_Banco'],  # Jerarquía: solo bancos
            values='Titulos públicos y privados',
            title='🏦 Participación de Mercado - Sistema Bancario Argentino<br>(Por Títulos Públicos y Privados)',
            color='Titulos públicos y privados',
            color_continuous_scale=px.colors.sequential.Viridis
        )

        # Personalizar el gráfico
        fig.update_traces(
            hovertemplate='<b>%{label}</b><br>Títulos: $%{value:,.0f}<br>Porcentaje: %{percentRoot:.1%}',
            textinfo='label+percent entry',
            textfont_size=12
        )

        fig.update_layout(
            height=600,
            font_family="Arial",
            title_font_size=18,
            title_x=0.5
        )

        # Mostrar el gráfico en Streamlit
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Error al crear el treemap: {e}")

def grafico_treemap_instrumentos_bcra(ranking_bancos):
    """
    Crea un treemap interactivo con la participación de mercado por Instrumentos BCRA usando Plotly.
    """
    # st.markdown("##### Participación de Mercado por Instrumentos BCRA")

    try:
        # Preparar datos para el treemap
        df_treemap = ranking_bancos[['Nombre_Banco', 'Instrumtos BCRA']].copy()
        df_treemap = df_treemap.dropna()
        df_treemap = df_treemap[df_treemap['Instrumtos BCRA'] > 0]

        # Ordenar por Instrumentos BCRA (descendente)
        df_treemap = df_treemap.sort_values('Instrumtos BCRA', ascending=False)

        # Calcular porcentajes sobre el total de Instrumentos BCRA
        total_instrumentos = df_treemap['Instrumtos BCRA'].sum()
        df_treemap['Porcentaje'] = (df_treemap['Instrumtos BCRA'] / total_instrumentos * 100).round(1)

        # Crear treemap con Plotly
        fig = px.treemap(
            df_treemap,
            path=['Nombre_Banco'],  # Jerarquía: solo bancos
            values='Instrumtos BCRA',
            title='🏦 Participación de Mercado - Sistema Bancario Argentino<br>(Por Instrumentos BCRA)',
            color='Instrumtos BCRA',
            color_continuous_scale=px.colors.sequential.Viridis
        )

        # Personalizar el gráfico
        fig.update_traces(
            hovertemplate='<b>%{label}</b><br>Instrumentos: $%{value:,.0f}<br>Porcentaje: %{percentRoot:.1%}',
            textinfo='label+percent entry',
            textfont_size=12
        )

        fig.update_layout(
            height=600,
            font_family="Arial",
            title_font_size=18,
            title_x=0.5
        )

        # Mostrar el gráfico en Streamlit
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Error al crear el treemap: {e}")