import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
from .utils import configurar_estilo_seaborn, mostrar_grafico_streamlit, formatear_numero, obtener_colores_para_bancos
from .utils import obtener_colores_para_bancos, obtener_color_banco, COLORES_BANCOS
from .utils import obtener_siglas_para_bancos, obtener_sigla_banco, SIGLAS_BANCOS

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


def grafico_treemap_volumen_negocio_total(ranking_bancos):
    """
    Crea un treemap interactivo con la participación de mercado por Volumen de Negocio usando Plotly.
    Muestra todos los bancos sin agrupar y aplica el esquema de colores consistente.
    """
    st.markdown("##### Participación de Mercado por Volumen de Negocio")

    try:
        # Preparar datos para el treemap
        df_treemap = ranking_bancos[['Nombre_Banco', 'Volumen de Negocio']].copy()
        df_treemap = df_treemap.dropna()
        df_treemap = df_treemap[df_treemap['Volumen de Negocio'] > 0]

        # Crear una columna nueva con las siglas
        df_treemap['Sigla_Banco'] = df_treemap['Nombre_Banco'].apply(obtener_sigla_banco)

        # Ordenar por Volumen de Negocio (descendente)
        df_treemap = df_treemap.sort_values('Volumen de Negocio', ascending=False)

        # Calcular porcentajes sobre el total del volumen de negocio
        total_volumen = df_treemap['Volumen de Negocio'].sum()
        df_treemap['Porcentaje'] = (df_treemap['Volumen de Negocio'] / total_volumen * 100).round(1)

        # Obtener colores para los bancos
        colores_bancos = obtener_colores_para_bancos(df_treemap['Nombre_Banco'].tolist())

        # Crear treemap con Plotly - CAMBIADO: usar Sigla_Banco en path
        fig = px.treemap(
            df_treemap,
            path=['Sigla_Banco'],  # Usar siglas en lugar de nombres completos
            values='Volumen de Negocio',
            title='🏦 Participación de Mercado - Sistema Bancario Argentino<br>(Por Volumen de Negocio)',
            color='Nombre_Banco',  # Mantener nombre completo para colores
            color_discrete_map=colores_bancos  # Usar el mapa de colores personalizado
        )

        # Personalizar el gráfico - MODIFICADO: incluir nombre completo en hover
        fig.update_traces(
            hovertemplate='<b>%{label}</b><br>Banco: %{customdata}<br>Volumen: $%{value:,.0f}<br>Porcentaje: %{percentRoot:.1%}',
            customdata=df_treemap['Nombre_Banco'],  # Mostrar nombre completo en hover
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
        
        # Crear una columna nueva con las siglas
        df_treemap['Sigla_Banco'] = df_treemap['Nombre_Banco'].apply(obtener_sigla_banco)

        # Ordenar por Préstamos (descendente)
        df_treemap = df_treemap.sort_values('Prestamos', ascending=False)

        # Calcular porcentajes sobre el total de préstamos
        total_prestamos = df_treemap['Prestamos'].sum()
        df_treemap['Porcentaje'] = (df_treemap['Prestamos'] / total_prestamos * 100).round(1)

        # Obtener colores para los bancos
        colores_bancos = obtener_colores_para_bancos(df_treemap['Nombre_Banco'].tolist())

        # Crear treemap con Plotly usando las siglas para las etiquetas
        fig = px.treemap(
            df_treemap,
            path=['Sigla_Banco'],  # Usar siglas en lugar de nombres completos
            values='Prestamos',
            title='🏦 Participación de Mercado - Sistema Bancario Argentino<br>(Por Préstamos)',
            color='Nombre_Banco',   # Mantener nombre completo para los colores
            color_discrete_map=colores_bancos  # Usar el mapa de colores personalizado
        )

        # Personalizar el gráfico - Incluir nombre completo en hover
        fig.update_traces(
            hovertemplate='<b>%{label}</b><br>Banco: %{customdata}<br>Préstamos: $%{value:,.0f}<br>Porcentaje: %{percentRoot:.1%}',
            customdata=df_treemap['Nombre_Banco'],  # Mostrar nombre completo en hover
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

        # Crear una columna nueva con las siglas
        df_treemap['Sigla_Banco'] = df_treemap['Nombre_Banco'].apply(obtener_sigla_banco)

        # Ordenar por Depósitos (descendente)
        df_treemap = df_treemap.sort_values('Depositos', ascending=False)

        # Calcular porcentajes sobre el total de depósitos
        total_depositos = df_treemap['Depositos'].sum()
        df_treemap['Porcentaje'] = (df_treemap['Depositos'] / total_depositos * 100).round(1)

        # Obtener colores para los bancos
        colores_bancos = obtener_colores_para_bancos(df_treemap['Nombre_Banco'].tolist())

        # Crear treemap con Plotly usando las siglas para las etiquetas
        fig = px.treemap(
            df_treemap,
            path=['Sigla_Banco'],  # Usar siglas en lugar de nombres completos
            values='Depositos',
            title='🏦 Participación de Mercado - Sistema Bancario Argentino<br>(Por Depósitos)',
            color='Nombre_Banco',   # Mantener nombre completo para los colores
            color_discrete_map=colores_bancos  # Usar el mapa de colores personalizado
        )

        # Personalizar el gráfico - Incluir nombre completo en hover
        fig.update_traces(
            hovertemplate='<b>%{label}</b><br>Banco: %{customdata}<br>Depósitos: $%{value:,.0f}<br>Porcentaje: %{percentRoot:.1%}',
            customdata=df_treemap['Nombre_Banco'],  # Mostrar nombre completo en hover
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
    Crea un treemap interactivo con la participación de mercado por Títulos públicos y privados usando Plotly.
    """
    st.markdown("##### Participación de Mercado por Títulos Públicos y Privados")

    try:
        # Preparar datos para el treemap
        df_treemap = ranking_bancos[['Nombre_Banco', 'Titulos públicos y privados']].copy()
        df_treemap = df_treemap.dropna()
        df_treemap = df_treemap[df_treemap['Titulos públicos y privados'] > 0]

        # Crear una columna nueva con las siglas
        df_treemap['Sigla_Banco'] = df_treemap['Nombre_Banco'].apply(obtener_sigla_banco)

        # Ordenar por Títulos (descendente)
        df_treemap = df_treemap.sort_values('Titulos públicos y privados', ascending=False)

        # Calcular porcentajes sobre el total de títulos
        total_titulos = df_treemap['Titulos públicos y privados'].sum()
        df_treemap['Porcentaje'] = (df_treemap['Titulos públicos y privados'] / total_titulos * 100).round(1)

        # Obtener colores para los bancos
        colores_bancos = obtener_colores_para_bancos(df_treemap['Nombre_Banco'].tolist())

        # Crear treemap con Plotly usando las siglas para las etiquetas
        fig = px.treemap(
            df_treemap,
            path=['Sigla_Banco'],  # Usar siglas en lugar de nombres completos
            values='Titulos públicos y privados',
            title='🏦 Participación de Mercado - Sistema Bancario Argentino<br>(Por Títulos Públicos y Privados)',
            color='Nombre_Banco',   # Mantener nombre completo para los colores
            color_discrete_map=colores_bancos  # Usar el mapa de colores personalizado
        )

        # Personalizar el gráfico - Incluir nombre completo en hover
        fig.update_traces(
            hovertemplate='<b>%{label}</b><br>Banco: %{customdata}<br>Títulos: $%{value:,.0f}<br>Porcentaje: %{percentRoot:.1%}',
            customdata=df_treemap['Nombre_Banco'],  # Mostrar nombre completo en hover
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
    st.markdown("##### Participación de Mercado por Instrumentos BCRA")

    try:
        # Preparar datos para el treemap
        df_treemap = ranking_bancos[['Nombre_Banco', 'Instrumtos BCRA']].copy()
        df_treemap = df_treemap.dropna()
        df_treemap = df_treemap[df_treemap['Instrumtos BCRA'] > 0]

        # Crear una columna nueva con las siglas
        df_treemap['Sigla_Banco'] = df_treemap['Nombre_Banco'].apply(obtener_sigla_banco)

        # Ordenar por Instrumentos BCRA (descendente)
        df_treemap = df_treemap.sort_values('Instrumtos BCRA', ascending=False)

        # Calcular porcentajes sobre el total de Instrumentos BCRA
        total_instrumentos = df_treemap['Instrumtos BCRA'].sum()
        df_treemap['Porcentaje'] = (df_treemap['Instrumtos BCRA'] / total_instrumentos * 100).round(1)

        # Obtener colores para los bancos
        colores_bancos = obtener_colores_para_bancos(df_treemap['Nombre_Banco'].tolist())

        # Crear treemap con Plotly usando las siglas para las etiquetas
        fig = px.treemap(
            df_treemap,
            path=['Sigla_Banco'],  # Usar siglas en lugar de nombres completos
            values='Instrumtos BCRA',
            title='🏦 Participación de Mercado - Sistema Bancario Argentino<br>(Por Instrumentos BCRA)',
            color='Nombre_Banco',   # Mantener nombre completo para los colores
            color_discrete_map=colores_bancos  # Usar el mapa de colores personalizado
        )

        # Personalizar el gráfico - Incluir nombre completo en hover
        fig.update_traces(
            hovertemplate='<b>%{label}</b><br>Banco: %{customdata}<br>Instrumentos BCRA: $%{value:,.0f}<br>Porcentaje: %{percentRoot:.1%}',
            customdata=df_treemap['Nombre_Banco'],  # Mostrar nombre completo en hover
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





def grafico_interactivo_top_bancos_rango(df_procesado, periodo_inicio, periodo_fin, bancos_seleccionados=None):
    """
    Crea un gráfico interactivo con Plotly mostrando la evolución del volumen de negocio
    de los bancos seleccionados entre los períodos seleccionados.

    Parámetros:
    - df_procesado: DataFrame con los datos procesados
    - periodo_inicio: Período inicial del rango (formato YYYYMM)
    - periodo_fin: Período final del rango (formato YYYYMM)
    - bancos_seleccionados: Lista de bancos a incluir (si es None, se usan los top 10)
    """
    # Ordenar los períodos disponibles
    periodos_disponibles = sorted(df_procesado['Periodo'].unique())

    # Verificar que los períodos estén en la lista
    if periodo_inicio not in periodos_disponibles:
        raise ValueError(f"El período inicial '{periodo_inicio}' no se encuentra en la lista de períodos disponibles.")
    if periodo_fin not in periodos_disponibles:
        raise ValueError(f"El período final '{periodo_fin}' no se encuentra en la lista de períodos disponibles.")

    # Determinar los índices de los períodos
    periodo_inicio_idx = periodos_disponibles.index(periodo_inicio)
    periodo_fin_idx = periodos_disponibles.index(periodo_fin) + 1  # +1 para incluir el final

    # Seleccionar los períodos entre inicio y fin
    periodos_seleccionados = periodos_disponibles[periodo_inicio_idx:periodo_fin_idx]

    # Filtrar los datos según los períodos seleccionados
    df_ventana = df_procesado[df_procesado['Periodo'].isin(periodos_seleccionados)]

    # Verificar que hay datos válidos
    if df_ventana.empty:
        raise ValueError("No hay datos disponibles para los períodos seleccionados.")

    # Si no se especificaron bancos, obtener los top 10 según el último período
    if bancos_seleccionados is None or len(bancos_seleccionados) == 0:
        ultimo_periodo = periodos_seleccionados[-1]
        top_bancos_df = df_ventana[df_ventana['Periodo'] == ultimo_periodo].nlargest(10, 'Volumen de Negocio')
        bancos_seleccionados = top_bancos_df['Nombre_Banco'].tolist()

    # Filtrar los datos para incluir solo los bancos seleccionados
    df_ventana = df_ventana[df_ventana['Nombre_Banco'].isin(bancos_seleccionados)]
    
    # Diccionario de siglas para los bancos
    banco_a_sigla = {
        "BANCO DE LA NACION ARGENTINA": "BNA",
        "BANCO DE GALICIA Y BUENOS AIRES S.A.U.": "GALICIA",
        "BANCO SANTANDER ARGENTINA S.A.": "SANTANDER",
        "BANCO DE LA PROVINCIA DE BUENOS AIRES": "BPBA",
        "BANCO BBVA ARGENTINA S.A.": "BBVA",
        "INDUSTRIAL AND COMMERCIAL BANK OF CHINA (ARGENTINA) S.A.U.": "ICBC",
        "BANCO MACRO S.A.": "MACRO",
        "BANCO PATAGONIA S.A.": "PATAGONIA",
        "BANCO CREDICOOP COOPERATIVO LIMITADO": "CREDICOOP",
        "BANCO DE LA CIUDAD DE BUENOS AIRES": "CIUDAD"
    }
    
    # Crear columna de siglas para la leyenda
    df_ventana['Sigla_Banco'] = df_ventana['Nombre_Banco'].map(lambda x: banco_a_sigla.get(x, x[:3]))
    
    # Convertir 'Periodo' a texto en formato legible (YYYY-MM)
    df_ventana['Periodo'] = df_ventana['Periodo'].astype(str).str.slice(0, 4) + "-" + df_ventana['Periodo'].astype(str).str.slice(4, 6)

    # Escalar los valores de Volumen de Negocio (a millones)
    df_ventana['Volumen de Negocio'] = df_ventana['Volumen de Negocio'] / 1e6

    # Formatear períodos para el título
    inicio_display = periodo_inicio[:4] + "-" + periodo_inicio[4:]
    fin_display = periodo_fin[:4] + "-" + periodo_fin[4:]


    # Obtener el mapa de colores para los bancos seleccionados
    colores_bancos = obtener_colores_para_bancos(bancos_seleccionados)
    
    # Crear el mapa de colores para las siglas
    color_map = {sigla: colores_bancos[nombre] 
                for nombre, sigla in zip(df_ventana['Nombre_Banco'].unique(), df_ventana['Sigla_Banco'].unique())}

   
    # Crear el gráfico interactivo con Plotly usando las siglas para la leyenda
    fig = px.line(
        df_ventana,
        x='Periodo',
        y='Volumen de Negocio',
        color='Sigla_Banco',  # Cambiar a usar la columna de siglas
        title=f'Evolución del Volumen de Negocio - Bancos Seleccionados ({inicio_display} a {fin_display})',
        labels={"Volumen de Negocio": "Volumen de Negocio (Millones de $)", "Periodo": "Período", "Sigla_Banco": "Banco"},
        height=600,
        color_discrete_map=color_map  # Usar el mapa de colores personalizado
    )

    # Forzar el eje X a tratar los valores como texto
    fig.update_xaxes(type='category')

    # Personalizar el diseño del gráfico
    fig.update_layout(
        xaxis_title="Período",
        yaxis_title="Volumen de Negocio (Millones de $)",
        font=dict(family="Arial", size=12),
        hovermode="x unified",
        # Cambiar la posición de la leyenda para que aparezca abajo
        legend=dict(
            orientation="h",        # Orientación horizontal
            yanchor="top",          # Anclaje vertical arriba
            y=-0.25,                # Posición en Y (negativo para que esté debajo del gráfico)
            xanchor="center",       # Anclaje horizontal centrado
            x=0.5,                  # Centrado en X
            title=None,             # Eliminar título de la leyenda
            font=dict(size=10)      # Tamaño de fuente
        ),
        # Aumentar el margen inferior para dejar espacio a la leyenda
        margin=dict(l=50, r=50, t=80, b=5)
    )

    return fig


