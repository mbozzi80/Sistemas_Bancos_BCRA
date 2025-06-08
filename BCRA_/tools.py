import pandas as pd
from io import StringIO
import requests
from .estructura_bcra import dic, cl, columnas

def cargar_denominaciones():
    """
    Carga los archivos de denominaciones de bancos y cuentas desde GitHub
    """
    try:
        print("🔄 Descargando denominaciones de bancos...")
        
        # URL del archivo de denominaciones de bancos desde GitHub
        url_bancos = "https://raw.githubusercontent.com/mbozzi80/Sistemas_Bancos_BCRA/master/denominacion_.TXT"
        
        # Descargar denominaciones de bancos
        response_bancos = requests.get(url_bancos)
        response_bancos.raise_for_status()
        print(f"✅ Descarga de bancos exitosa. Tamaño: {len(response_bancos.text)} caracteres")
        
        # Mostrar primeras líneas para debug
        primeras_lineas = response_bancos.text[:10]
        print(f"📄 Primeras líneas del archivo de bancos: {primeras_lineas}")
        
        # El archivo está en formato CSV con comillas, usar delimitador tab
        df_bancos = pd.read_csv(StringIO(response_bancos.text), sep='\t', header=None, quotechar='"')
        print(f"🏦 Columnas encontradas: {df_bancos.shape[1]}")
        print(f"📊 Primeras filas del archivo:")
        print(df_bancos.head())
        
        # Crear diccionario usando primera columna (código) y segunda columna (nombre)
        dict_bancos = {}
        for index, row in df_bancos.iterrows():
            try:
                codigo = int(str(row[0]).replace('"', '').strip())
                denominacion = str(row[1]).replace('"', '').strip()
                dict_bancos[codigo] = denominacion
            except (ValueError, IndexError) as e:
                print(f"⚠️ Error procesando fila {index}: {e}")
                continue
        
        print(f"🏦 Bancos cargados: {len(dict_bancos)}")
        print(f"📚 Diccionario de bancos creado con {len(dict_bancos)} entradas")
        if len(dict_bancos) > 0:
            print(f"🔍 Primeros bancos: {list(dict_bancos.items())[:3]}")
        
        # URL del archivo de denominaciones de cuentas desde GitHub
        url_cuentas = "https://raw.githubusercontent.com/mbozzi80/Sistemas_Bancos_BCRA/master/cuentas.txt"
        
        # Descargar denominaciones de cuentas
        response_cuentas = requests.get(url_cuentas)
        response_cuentas.raise_for_status()
        
        # Procesar cuentas de manera similar
        dict_cuentas = {}
        for linea in response_cuentas.text.strip().split('\n'):
            if linea.strip():
                partes = linea.strip().split(None, 1)
                if len(partes) >= 2:
                    try:
                        codigo = int(partes[0])
                        denominacion = partes[1]
                        dict_cuentas[codigo] = denominacion
                    except ValueError:
                        continue
        
        return dict_bancos, dict_cuentas
        
    except Exception as e:
        print(f"❌ Error al cargar denominaciones: {e}")
        return {}, {}
    

def procesar_datos_bcra(texto_crudo):
    """
    Procesa el texto crudo del archivo h_imput.txt y lo convierte en DataFrame estructurado
    
    Parámetros:
    texto_crudo: String con el contenido del archivo h_imput.txt
    
    Retorna:
    DataFrame con los datos procesados según la estructura de columnas definida
    """
    try:
        # Convertir texto a DataFrame (asumiendo que está separado por espacios o tabs)
        df_raw = pd.read_csv(StringIO(texto_crudo), sep=r'\s+', header=None, 
                           names=['Entidad', 'Periodo', 'Cuenta', 'Saldo'])
        
        # Convertir columnas a tipos apropiados
        df_raw['Entidad'] = df_raw['Entidad'].astype(int)
        df_raw['Periodo'] = df_raw['Periodo'].astype(int)
        df_raw['Cuenta'] = df_raw['Cuenta'].astype(int)
        df_raw['Saldo'] = pd.to_numeric(df_raw['Saldo'], errors='coerce')
        
        # Función para verificar si una cuenta está en un rango
        def cuenta_en_rango(cuenta, rango):
            if isinstance(rango, tuple):
                return rango[0] <= cuenta <= rango[1]
            elif isinstance(rango, list):
                return cuenta in rango
            return False
        
        # Función para calcular el valor de cada concepto
        def calcular_concepto(df, concepto, rango, multiplicador):
            mask = df['Cuenta'].apply(lambda x: cuenta_en_rango(x, rango))
            valor = df[mask]['Saldo'].sum()
            return valor if multiplicador else -valor
        
        # Agrupar por Entidad y Periodo
        resultado = []
        
        for (entidad, periodo), grupo in df_raw.groupby(['Entidad', 'Periodo']):
            fila = {'Entidad': entidad, 'Periodo': periodo}
            
            # Procesar cada concepto del diccionario
            for concepto, rango in dic.items():
                if concepto in cl:  # Solo procesar conceptos que están en cl
                    multiplicador = cl[concepto]
                    fila[concepto] = calcular_concepto(grupo, concepto, rango, multiplicador)
                else:
                    fila[concepto] = 0
            
             # Agregar conceptos especiales que no están en dic pero sí en columnas
            fila['Prestamos totales'] = fila.get('Prestamos', 0)
            fila['Letras y Notas BCRA'] = 0  # Por ahora en 0, se puede calcular después
            fila['Previsiones'] = calcular_concepto(grupo, 'Prevision', dic['Prevision'], True)
            
            # NUEVO: Calcular Volumen de Negocio con cuentas específicas
            # Depósitos específicos para Volumen de Negocio
            depositos_vn_rangos = [
                (311100, 311199), (311400, 311499), (311700, 311799),
                (312100, 312199), (315100, 315199), (315700, 315799)
            ]
            
            depositos_vn = 0
            for rango in depositos_vn_rangos:
                mask_dep = grupo['Cuenta'].apply(lambda x: rango[0] <= x <= rango[1])
                depositos_vn += -grupo[mask_dep]['Saldo'].sum()  # Negativo porque son pasivos
            
            # Préstamos específicos para Volumen de Negocio
            prestamos_vn_rangos = [
                (131100, 131199), (131400, 131499), (131700, 131799), (135700, 135799)
            ]
            
            prestamos_vn_puntuales = [131263, 131851, 131855, 131859, 131889, 131890]
            
            prestamos_vn = 0
            # Sumar rangos
            for rango in prestamos_vn_rangos:
                mask_prest = grupo['Cuenta'].apply(lambda x: rango[0] <= x <= rango[1])
                prestamos_vn += grupo[mask_prest]['Saldo'].sum()
            
            # Sumar cuentas puntuales
            for cuenta in prestamos_vn_puntuales:
                mask_puntual = grupo['Cuenta'] == cuenta
                prestamos_vn += grupo[mask_puntual]['Saldo'].sum()
            
            # Calcular Volumen de Negocio total
            fila['Volumen de Negocio'] = depositos_vn + prestamos_vn
            
            resultado.append(fila)
        
        # Crear DataFrame final
        df_final = pd.DataFrame(resultado)
        
        # Reordenar columnas según el orden definido
        columnas_existentes = [col for col in columnas if col in df_final.columns]
        df_final = df_final[columnas_existentes]
        
        return df_final
        
    except Exception as e:
        print(f"Error al procesar datos: {e}")
        return None

def procesar_datos_bcra_con_nombres(texto_crudo):
    """
    Procesa los datos BCRA y agrega los nombres de bancos
    """
    print("🔄 Iniciando procesamiento con nombres...")
    
    # Procesar datos como antes
    df_procesado = procesar_datos_bcra(texto_crudo)
    
    if df_procesado is None:
        print("❌ Error: df_procesado es None")
        return None
    
    print(f"✅ Datos procesados. Shape: {df_procesado.shape}")
    print(f"🔍 Bancos únicos en datos: {df_procesado['Entidad'].unique()[:10]}")
    
    # Cargar denominaciones
    dict_bancos, dict_cuentas = cargar_denominaciones()
    
    print(f"📚 Diccionario bancos tiene {len(dict_bancos)} entradas")
    if len(dict_bancos) > 0:
        print(f"🔍 Primeros bancos en diccionario: {list(dict_bancos.items())[:5]}")
    
    # Agregar columna con nombre del banco
    df_procesado['Nombre_Banco'] = df_procesado['Entidad'].map(dict_bancos)
    
    print(f"✅ Nombres agregados. Nombres únicos: {df_procesado['Nombre_Banco'].nunique()}")
    print(f"🔍 Algunos nombres: {df_procesado['Nombre_Banco'].dropna().unique()[:5]}")
    
    # Reordenar columnas
    columnas_nuevas = ['Entidad', 'Nombre_Banco'] + [col for col in df_procesado.columns if col not in ['Entidad', 'Nombre_Banco']]
    df_procesado = df_procesado[columnas_nuevas]
    
    return df_procesado

def obtener_resumen_datos(df):
    """
    Obtiene un resumen básico de los datos procesados
    """
    if df is None:
        return "No hay datos para mostrar"
    
    resumen = f"""
📊 RESUMEN DE DATOS PROCESADOS:

🏦 Bancos únicos: {df['Entidad'].nunique()}
📅 Períodos: {df['Periodo'].min()} - {df['Periodo'].max()}
📈 Total registros: {len(df)}

🔝 Top 5 bancos por Activo Total (último período):
"""
    
    # Obtener último período
    ultimo_periodo = df['Periodo'].max()
    top_bancos = df[df['Periodo'] == ultimo_periodo].nlargest(5, 'Activo')[['Entidad', 'Activo']]
    
    for _, banco in top_bancos.iterrows():
        resumen += f"\n    Banco {banco['Entidad']}: ${banco['Activo']:,.0f}"
    
    return resumen

def obtener_resumen_datos_con_nombres(df):
    """
    Obtiene un resumen con nombres de bancos en lugar de códigos
    """
    if df is None:
        return "No hay datos para mostrar"
    
    resumen = f"""
📊 RESUMEN DE DATOS PROCESADOS:

🏦 Bancos únicos: {df['Entidad'].nunique()}
📅 Períodos: {df['Periodo'].min()} - {df['Periodo'].max()}
📈 Total registros: {len(df)}

🔝 Top 5 bancos por Volumen de Negocio (último período):
"""
    
    # Obtener último período
    ultimo_periodo = df['Periodo'].max()
    top_bancos = df[df['Periodo'] == ultimo_periodo].nlargest(5, 'Volumen de Negocio')[['Entidad', 'Nombre_Banco', 'Volumen de Negocio']]
    
    for _, banco in top_bancos.iterrows():
        nombre = banco['Nombre_Banco'] if pd.notna(banco['Nombre_Banco']) else f"Banco {banco['Entidad']}"
        resumen += f"\n    {nombre}: ${banco['Volumen de Negocio']:,.0f}"
    
    return resumen

