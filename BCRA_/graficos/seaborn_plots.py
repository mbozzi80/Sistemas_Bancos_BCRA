import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
# COMENTAR PLOTLY TEMPORALMENTE
# import plotly.express as px
from .utils import configurar_estilo_seaborn, mostrar_grafico_streamlit

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