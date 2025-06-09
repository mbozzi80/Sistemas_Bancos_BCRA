import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import pandas as pd

def configurar_estilo_seaborn():
    """Configura el estilo visual de seaborn"""
    sns.set_style("whitegrid")
    plt.rcParams['figure.facecolor'] = 'white'
    plt.rcParams['axes.facecolor'] = 'white'

def mostrar_grafico_streamlit(fig, titulo=""):
    """Muestra gráfico en Streamlit con formato consistente"""
    if titulo:
        st.markdown(f"#### {titulo}")
    st.pyplot(fig)
    plt.close(fig)  # Liberar memoria

# AGREGAR ESTAS FUNCIONES NUEVAS:
def formatear_numero(numero):
    """Formatea números con separadores de miles"""
    if pd.isna(numero) or numero == 0:
        return "0"
    
    # Convertir a entero si es un número entero
    if isinstance(numero, float) and numero.is_integer():
        numero = int(numero)
    
    # Formatear con separadores de miles
    return f"{numero:,}".replace(",", ".")

def calcular_ranking(df, columna, top_n=15):
    """Calcula ranking de bancos por una columna específica"""
    if columna not in df.columns:
        return pd.DataFrame()
    
    return df.nlargest(top_n, columna).reset_index(drop=True)

def filtrar_datos_por_periodo(df, periodo):
    """Filtra DataFrame por período específico"""
    if 'Periodo' not in df.columns:
        return pd.DataFrame()
    
    return df[df['Periodo'] == periodo].copy()