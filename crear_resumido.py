import pandas as pd

def crear_h_imput_resumido():
    """
    Lee h_imput local, filtra bancos y crea versión resumida
    """
    # Leer archivo local directamente
    nombre_archivo_original = "h_imput.txt"
    
    print("🔄 Leyendo h_imput local...")
    df = pd.read_csv(nombre_archivo_original, sep='\t', decimal=',', encoding='latin-1')
    
    print(f"📊 Datos originales: {len(df)} registros")
    
    # La primera columna es la entidad, la segunda el período
    entidad_col = df.columns[0]
    periodo_col = df.columns[1]
    print(f"🏦 Columna entidad: {entidad_col}")
    print(f"📅 Columna período: {periodo_col}")
    print(f"🏦 Bancos únicos: {df[entidad_col].nunique()}")
    
    # Convertir primera columna a string y QUITAR COMILLAS
    df[entidad_col] = df[entidad_col].astype(str).str.replace('"', '').str.strip()
    
    # Convertir período a string y quitar comillas
    df[periodo_col] = df[periodo_col].astype(str).str.replace('"', '').str.strip()
    
    # FILTRO 1: Mantener SOLO bancos < 10000
    df_bancos = df[pd.to_numeric(df[entidad_col], errors='coerce') < 10000]
    
    # CALCULAR DINÁMICAMENTE 10 AÑOS HACIA ATRÁS
    # Obtener el último período
    ultimo_periodo = pd.to_numeric(df_bancos[periodo_col], errors='coerce').max()
    print(f"📅 Último período encontrado: {ultimo_periodo}")
    
    # Calcular 10 años hacia atrás (ejemplo: 202502 -> 201502)
    ultimo_año = ultimo_periodo // 100  # 202502 -> 2025
    ultimo_mes = ultimo_periodo % 100   # 202502 -> 2
    
    año_inicio = ultimo_año - 10        # 2025 - 10 = 2015
    periodo_inicio = año_inicio * 100 + ultimo_mes  # 2015 * 100 + 2 = 201502
    
    print(f"📅 Período de inicio calculado: {periodo_inicio} (10 años hacia atrás)")
    
    # FILTRO 2: Mantener SOLO desde el período calculado
    df_resumido = df_bancos[pd.to_numeric(df_bancos[periodo_col], errors='coerce') >= periodo_inicio]
    
    print(f"✅ Datos filtrados: {len(df_resumido)} registros")
    print(f"🏦 Bancos después del filtro: {df_resumido[entidad_col].nunique()}")
    print(f"📅 Período desde: {df_resumido[periodo_col].min()} hasta: {df_resumido[periodo_col].max()}")
    
    # Guardar el archivo resumido
    nombre_archivo_resumido = "h_imput_resumido.txt"
    df_resumido.to_csv(nombre_archivo_resumido, sep='\t', decimal=',', index=False, encoding='latin-1')
    
    print(f"💾 Archivo guardado: {nombre_archivo_resumido}")
    print("📤 Ahora sube este archivo a tu Dropbox")
    
    return df_resumido

# Ejecutar la función
if __name__ == "__main__":
    df_filtrado = crear_h_imput_resumido()

    