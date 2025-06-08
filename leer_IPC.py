import pandas as pd

def leer_archivo_xls():
    """
    Lee archivo .xlsx del IPC FACPCE y crea DataFrame con solo Periodo e IPC
    """
    try:
        # Leer archivo especificando la hoja
        print("🔄 Leyendo archivo IPC FACPCE - Hoja 'ipc empalme ipim'...")
        df_raw = pd.read_excel('Indice-FACPCE-Res.-JG-539-18-_2025-04-1.xlsx', 
                              sheet_name='ipc empalme ipim')
        
        print(f"✅ Archivo leído: {len(df_raw)} filas, {len(df_raw.columns)} columnas")
        
        # LIMPIAR Y PROCESAR DATOS
        print("🔄 Procesando y limpiando datos...")
        
        # Buscar la fila donde empiezan los datos reales
        start_idx = None
        for i, row in df_raw.iterrows():
            if 'MES' in str(row.iloc[0]):
                start_idx = i + 1  # Los datos empiezan en la siguiente fila
                break
        
        if start_idx is None:
            print("❌ No se encontró el inicio de los datos")
            return None
            
        # Crear DataFrame limpio
        df_clean = df_raw.iloc[start_idx:].copy()
        
        # Renombrar columnas
        df_clean.columns = ['Fecha', 'IPC']
        
        # Limpiar datos
        df_clean = df_clean.dropna()  # Eliminar filas vacías
        df_clean = df_clean[df_clean['IPC'] != '*']  # Eliminar asteriscos
        
        # Convertir tipos de datos
        df_clean['Fecha'] = pd.to_datetime(df_clean['Fecha'])
        df_clean['IPC'] = pd.to_numeric(df_clean['IPC'], errors='coerce')
        
        # Eliminar filas con valores no válidos
        df_clean = df_clean.dropna()
        
        # Agregar período en formato YYYYMM para compatibilidad con BCRA
        df_clean['Periodo'] = df_clean['Fecha'].dt.strftime('%Y%m').astype(int)
        
        # SOLO DEVOLVER PERIODO E IPC
        df_final = df_clean[['Periodo', 'IPC']].reset_index(drop=True)
        
        print(f"✅ Datos procesados: {len(df_final)} períodos válidos")
        print(f"📅 Desde período {df_final['Periodo'].min()} hasta {df_final['Periodo'].max()}")
        print(f"📊 Primeras filas:")
        print(df_final.head())
        print(f"📊 Últimas filas:")
        print(df_final.tail())
        
        return df_final
        
    except Exception as e:
        print(f"❌ Error al leer archivo: {e}")
        return None

if __name__ == "__main__":
    print("🚀 Iniciando lectura de IPC FACPCE...")
    df_ipc = leer_archivo_xls()
    
    if df_ipc is not None:
        print("✅ ÉXITO: IPC cargado correctamente")
        print(f"📊 {len(df_ipc)} períodos desde {df_ipc['Periodo'].min()} hasta {df_ipc['Periodo'].max()}")
    else:
        print("❌ Error en la carga")
        