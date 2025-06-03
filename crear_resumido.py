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
    
    # La primera columna es la entidad
    entidad_col = df.columns[0]
    print(f"🏦 Columna entidad: {entidad_col}")
    print(f"🏦 Bancos únicos: {df[entidad_col].nunique()}")
    
    # Convertir primera columna a string y QUITAR COMILLAS
    df[entidad_col] = df[entidad_col].astype(str).str.replace('"', '').str.strip()

    # FILTRAR: Mantener SOLO bancos < 10000
    df_resumido = df[pd.to_numeric(df[entidad_col], errors='coerce') < 10000]
    
    print(f"✅ Datos filtrados: {len(df_resumido)} registros")
    print(f"🏦 Bancos después del filtro: {df_resumido[entidad_col].nunique()}")
    
    # Guardar el archivo resumido
    nombre_archivo_resumido = "h_imput_resumido.txt"
    df_resumido.to_csv(nombre_archivo_resumido, sep='\t', decimal=',', index=False, encoding='latin-1')
    
    print(f"💾 Archivo guardado: {nombre_archivo_resumido}")
    print("📤 Ahora sube este archivo a tu Dropbox")
    
    return df_resumido

# Ejecutar la función
if __name__ == "__main__":
    df_filtrado = crear_h_imput_resumido()
