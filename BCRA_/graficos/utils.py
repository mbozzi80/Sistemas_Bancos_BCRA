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

# En BCRA_/graficos/utils.py - debería estar así:
def formatear_numero(numero):
    """Formatea números con separadores de miles"""
    if pd.isna(numero) or numero == 0:
        return "0"
    
    # Convertir a entero si es un número entero
    if isinstance(numero, float) and numero.is_integer():
        numero = int(numero)
    
    # Formatear con puntos como separadores (SIN símbolo $)
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


# Añadir a las utilidades existentes

# Diccionario global de colores para los bancos
COLORES_BANCOS = {
    'BANCO DE LA NACION ARGENTINA': '#87CEEB',           # Celeste
    'BANCO DE GALICIA Y BUENOS AIRES S.A.U.': "#FF7300", # Naranja
    'BANCO SANTANDER ARGENTINA S.A.': "#DC143F",         # Rojo
    'BANCO DE LA PROVINCIA DE BUENOS AIRES': "#1D3805",  # Verde
    'BANCO BBVA ARGENTINA S.A.': '#0066CC',              # Azul
    'INDUSTRIAL AND COMMERCIAL BANK OF CHINA (ARGENTINA) S.A.U.': "#E14641", # Azul real
    'BANCO MACRO S.A.': '#1E90FF',                       # Azul claro
    'BANCO PATAGONIA S.A.': '#8B4513',                   # Marrón
    'BANCO CREDICOOP COOPERATIVO LIMITADO': '#9932CC',   # Púrpura
    'BANCO DE LA CIUDAD DE BUENOS AIRES': "#474AFF",     # Tomate
    # Colores adicionales para otros bancos
    'HSBC BANK ARGENTINA S.A.': '#DB0011',               # Rojo HSBC
    'BANCO SUPERVIELLE S.A.': "#DB726F",                 # Verde Supervielle
    'BANCO ITAU ARGENTINA S.A.': "#6B9980",              # Azul Itaú
    'OTROS': '#B0B0B0'                                   # Gris para "otros" bancos
}

def obtener_color_banco(nombre_banco):
    """
    Obtiene el color corporativo para un banco dado.
    Si el banco no está en la lista, devuelve un color predeterminado.
    
    Parámetros:
    - nombre_banco: Nombre del banco
    
    Retorno:
    - Color en formato hexadecimal
    """
    return COLORES_BANCOS.get(nombre_banco, '#B0B0B0')  # Gris por defecto

def obtener_colores_para_bancos(lista_bancos):
    """
    Genera un diccionario de colores para una lista de bancos.
    
    Parámetros:
    - lista_bancos: Lista con los nombres de los bancos
    
    Retorno:
    - Diccionario con formato {banco: color}
    """
    return {banco: obtener_color_banco(banco) for banco in lista_bancos}



# Añadir después de COLORES_BANCOS

# Diccionario global de siglas para los bancos
SIGLAS_BANCOS = {
    "BANCO DE LA NACION ARGENTINA": "BNA",
    "BANCO DE GALICIA Y BUENOS AIRES S.A.U.": "GALICIA",
    "BANCO SANTANDER ARGENTINA S.A.": "SANTANDER",
    "BANCO DE LA PROVINCIA DE BUENOS AIRES": "BPBA",
    "BANCO BBVA ARGENTINA S.A.": "BBVA",
    "INDUSTRIAL AND COMMERCIAL BANK OF CHINA (ARGENTINA) S.A.U.": "ICBC",
    "BANCO MACRO S.A.": "MACRO",
    "BANCO PATAGONIA S.A.": "PATAGONIA",
    "BANCO CREDICOOP COOPERATIVO LIMITADO": "CREDICOOP",
    "BANCO DE LA CIUDAD DE BUENOS AIRES": "CIUDAD",
    "BANK OF CHINA"	"BANK OF CHINA L":'BANK OF CHINA',
    "BANCO HIPOTECARIO":'HIPOTECARIO',
    "BANCO SUPERVIELLE S.A.": "SUPERVIELLE",
    "BANCO ITAU ARGENTINA S.A.": "ITAU",
    "BANCO MARIVA S.A.": "MARIVA",
    "BANCO DE LA PROVINCIA DE CORDOBA": "BANCOR",
    "BANCO COMAFI SOCIEDAD ANONIMA": "COMAFI",
    "BANCO DE INVERSION Y COMERCIO EXTERIOR S.A.": "BICE",
    "BANCO DE LA PROVINCIA DE SAN JUAN": "BPSJ",
    "BANCO PROVINCIA DE TIERRA DEL FUEGO": "BPTDF",
    "WILOBANK S.A.U.": 'UALA',
    "BACS BANCO DE CREDITO Y SECURITIZACION S.A.": "BACS"
}

def obtener_sigla_banco(nombre_banco):
    """
    Obtiene la sigla para un banco dado.
    Si el banco no está en la lista, devuelve el nombre original.
    
    Parámetros:
    - nombre_banco: Nombre del banco
    
    Retorno:
    - Sigla del banco o el nombre original si no existe sigla
    """
    return SIGLAS_BANCOS.get(nombre_banco, nombre_banco)

def obtener_siglas_para_bancos(lista_bancos):
    """
    Genera un diccionario de siglas para una lista de bancos.
    
    Parámetros:
    - lista_bancos: Lista con los nombres de los bancos
    
    Retorno:
    - Diccionario con formato {banco: sigla}
    """
    return {banco: obtener_sigla_banco(banco) for banco in lista_bancos}

    