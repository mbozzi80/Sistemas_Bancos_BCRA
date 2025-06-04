import pandas as pd
from BCRA_.tools import procesar_datos_bcra_con_nombres

def crear_archivo_final():
    """
    Procesa LOCALMENTE y crea archivo final con denominaciones incluidas
    """
    print("🔄 Leyendo h_imput_resumido local...")
    
    # Leer archivo local directamente
    nombre_archivo = "h_imput_resumido.txt"
    
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
            
            # Guardar archivo final PRE-PROCESADO
            archivo_final = "bcra_datos_finales.csv"
            df_final.to_csv(archivo_final, index=False, encoding='utf-8')
            
            print(f"💾 Archivo final guardado: {archivo_final}")
            print("📤 AHORA SUBE ESTE ARCHIVO A DROPBOX")
            print("🎯 Después modificaremos app.py para usar este archivo")
            
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
        print("✅ ÉXITO: Archivo listo para subir a Dropbox")
    else:
        print("❌ Error en el proceso")