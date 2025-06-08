import pandas as pd
from BCRA_.tools import procesar_datos_bcra_con_nombres
from leer_IPC import leer_archivo_xls

def crear_archivo_final_constante():
    """
    Procesa LOCALMENTE y crea archivo final con denominaciones incluidas AJUSTADO POR INFLACIÓN
    """
    print("🚀 INICIANDO PROCESAMIENTO EN MONEDA CONSTANTE...")
    
    # 1. CARGAR DATOS IPC
    print("\n📊 Cargando datos de IPC...")
    df_ipc = leer_archivo_xls()
    if df_ipc is None:
        print("❌ Error: No se pudo cargar el IPC")
        return None
    
    # 2. PROCESAR DATOS BCRA (IGUAL QUE PROCESAR_COMPLETO.PY)
    print("\n🔄 Leyendo h_imput local...")
    
    # Leer archivo local directamente (IGUAL QUE PROCESAR_COMPLETO)
    nombre_archivo = "h_imput.txt"
    
    try:
        with open(nombre_archivo, 'r', encoding='latin-1') as file:
            texto_crudo = file.read()
        
        print(f"✅ Lectura exitosa. Tamaño: {len(texto_crudo)} caracteres")
        
        print("🔄 Procesando COMPLETAMENTE con denominaciones...")
        
        # Usar tu función existente que ya funciona (IGUAL QUE PROCESAR_COMPLETO)
        df_final = procesar_datos_bcra_con_nombres(texto_crudo)
        
        if df_final is not None:
            print(f"✅ Procesamiento exitoso: {len(df_final)} registros")
            print(f"📊 Columnas: {len(df_final.columns)} columnas")
            print(f"🏦 Bancos únicos: {df_final['Entidad'].nunique()}")
            
            # APLICAR FILTRO PARA OPTIMIZAR (IGUAL QUE PROCESAR_COMPLETO)
            print("🔄 Aplicando filtro de bancos...")
            
            # FILTRO: Solo bancos < 10000
            df_final = df_final[df_final['Entidad'] < 10000]
            print(f"🏦 Después filtro bancos < 10000: {len(df_final)} registros")
            print(f"🏦 Bancos finales: {df_final['Entidad'].nunique()}")

            # 3. OBTENER ÚLTIMO PERÍODO DEL BCRA (NO DEL IPC)
            ultimo_periodo_bcra = df_final['Periodo'].max()
            print(f"📅 Último período BCRA: {ultimo_periodo_bcra}")
            
            # Buscar IPC correspondiente al último período del BCRA
            ipc_ultimo_bcra = df_ipc[df_ipc['Periodo'] == ultimo_periodo_bcra]['IPC']
            
            if ipc_ultimo_bcra.empty:
                print(f"❌ No se encontró IPC para período {ultimo_periodo_bcra}")
                return None
            
            ipc_ultimo = ipc_ultimo_bcra.iloc[0]
            print(f"📈 IPC período {ultimo_periodo_bcra}: {ipc_ultimo:,.2f}")

            # 4. AJUSTAR POR INFLACIÓN
            print("\n💰 Ajustando por inflación a moneda constante...")

            # Crear diccionario de IPC para lookup rápido
            ipc_dict = dict(zip(df_ipc['Periodo'], df_ipc['IPC']))

            # DEFINIR COLUMNAS QUE NO DEBEN MODIFICARSE
            columnas_no_modificar = ['Entidad', 'Periodo', 'Nombre_Banco']
            
            # Columnas que son valores monetarios (todas excepto las protegidas)
            columnas_monetarias = [col for col in df_final.columns if col not in columnas_no_modificar]

            # CONVERTIR SOLO COLUMNAS MONETARIAS A NUMÉRICO ANTES DEL AJUSTE
            print("🔄 Convirtiendo columnas monetarias a formato numérico...")
            for col in columnas_monetarias:
                df_final[col] = pd.to_numeric(df_final[col], errors='coerce').fillna(0)

            print(f"✅ {len(columnas_monetarias)} columnas convertidas a numérico")
            print(f"🛡️ Columnas protegidas: {columnas_no_modificar}")

            # Ajustar cada fila por inflación
            print("🔄 Aplicando factor de ajuste por inflación...")
            total_filas = len(df_final)
            for idx, row in df_final.iterrows():
                if idx % 1000 == 0:
                    print(f"📊 Progreso: {idx}/{total_filas} ({idx/total_filas*100:.1f}%)")
                
                periodo = row['Periodo']
                if periodo in ipc_dict:
                    ipc_periodo = ipc_dict[periodo]
                    factor_ajuste = ipc_ultimo / ipc_periodo
                    
                    # Aplicar factor de ajuste SOLO a columnas monetarias
                    for col in columnas_monetarias:
                        df_final.at[idx, col] = row[col] * factor_ajuste

            print(f"✅ Ajuste por inflación completado")
            print(f"📈 Factor promedio aplicado: {ipc_ultimo/df_ipc['IPC'].mean():.2f}")

            # 5. GUARDAR ARCHIVO FINAL AJUSTADO POR INFLACIÓN
            archivo_final = f"bcra_datos_constantes_{ultimo_periodo_bcra}.csv"
            df_final.to_csv(archivo_final, index=False, encoding='utf-8')

            print(f"💾 Archivo final guardado: {archivo_final}")
            print(f"📊 {len(df_final)} registros en moneda constante de {ultimo_periodo_bcra}")

            return df_final
        else:
            print("❌ Error en procesamiento")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    print("🚀 Iniciando procesamiento en moneda constante...")
    df_result = crear_archivo_final_constante()
    
    if df_result is not None:
        print("✅ ÉXITO: Archivo en moneda constante creado")
    else:
        print("❌ Error en el proceso")