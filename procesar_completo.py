import pandas as pd
from BCRA_.tools import procesar_datos_bcra_con_nombres

def crear_archivo_final():
    """
    Procesa LOCALMENTE y crea archivo final con denominaciones incluidas
    """
    print("🔄 Leyendo h_imput local...")
    
    # Leer archivo local directamente
    nombre_archivo = "h_imput.txt"
    
    try:
        with open(nombre_archivo, 'r', encoding='latin-1') as file:
            texto_crudo = file.read()
        
        print(f"✅ Lectura exitosa. Tamaño: {len(texto_crudo)} caracteres")
        
        print("🔄 Procesando COMPLETAMENTE con denominaciones...")
        
        # Usar tu función existente que ya funciona
        df_final = procesar_datos_bcra_con_nombres(texto_crudo)
        
        if df_final is not None:
            print(f"✅ Procesamiento exitoso: {len(df_final)} registros")
            print(f"📊 Columnas: {len(df_final.columns)} columnas")
            print(f"🏦 Bancos únicos: {df_final['Entidad'].nunique()}")
            
            # APLICAR FILTRO PARA OPTIMIZAR
            print("🔄 Aplicando filtro de bancos...")
            
            # FILTRO: Solo bancos < 10000
            df_final = df_final[df_final['Entidad'] < 10000]
            print(f"🏦 Después filtro bancos < 10000: {len(df_final)} registros")
            print(f"🏦 Bancos finales: {df_final['Entidad'].nunique()}")

            # CONVERTIR COLUMNAS MONETARIAS A FLOAT
            print("🔄 Convirtiendo columnas monetarias a float...")
            columnas_monetarias = [col for col in df_final.columns 
                                 if col not in ['Entidad', 'Nombre_Banco', 'Periodo']]
            
            for col in columnas_monetarias:
                df_final[col] = pd.to_numeric(df_final[col], errors='coerce').fillna(0).astype(float)
            
            print(f"✅ {len(columnas_monetarias)} columnas convertidas a float")

            # Verificando columnas antes de guardar:
            print("🔍 Verificando columnas antes de guardar...")

            if 'Volumen de Negocio' in df_final.columns:
                print("✅ 'Volumen de Negocio' presente")
                print(f"📊 Muestra: {df_final['Volumen de Negocio'].head()}")
                print(f"📊 Stats: Min={df_final['Volumen de Negocio'].min():,.0f}, Max={df_final['Volumen de Negocio'].max():,.0f}")
            else:
                print("❌ 'Volumen de Negocio' FALTANTE")

            # Guardar archivo final PRE-PROCESADO (eliminar duplicado)
            archivo_final = "bcra_datos_finales.csv"
            df_final.to_csv(archivo_final, index=False, encoding='utf-8')
            
            print(f"💾 Archivo final guardado: {archivo_final}")
            print("📤 AHORA SUBE ESTE ARCHIVO A GITHUB")
                        
            return df_final
        
        else:
            print("❌ Error en procesamiento")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    print("🚀 Iniciando pre-procesamiento completo...")
    df_result = crear_archivo_final()
    
    if df_result is not None:
        print("✅ ÉXITO: Archivo listo para subir al Repo en GitHub")
    else:
        print("❌ Error en el proceso")



