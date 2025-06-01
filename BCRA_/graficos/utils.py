import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

def configurar_estilo_seaborn():
    """
    Configura el estilo global para todos los gráficos de Seaborn
    """
    sns.set_style("whitegrid")
    sns.set_palette("husl")
    plt.rcParams['figure.figsize'] = (10, 6)
    plt.rcParams['font.size'] = 12

def mostrar_grafico_streamlit(fig, titulo=""):
    """
    Función auxiliar para mostrar gráficos de matplotlib en Streamlit
    """
    if titulo:
        st.markdown(f"### {titulo}")
    st.pyplot(fig)
    plt.close(fig)  # Cerrar figura para liberar memoria

def formatear_numeros_millones(valor, pos):
    """
    Formateador para mostrar números en millones en los ejes
    """
    return f'${valor/1_000_000:.0f}M'

def obtener_colores_bancos():
    """
    Retorna una paleta de colores consistente para los bancos
    """
    return sns.color_palette("husl", 15)