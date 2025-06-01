"""
Configuración y estructura de datos del BCRA
Este archivo contiene todos los diccionarios y configuraciones para el procesamiento de datos bancarios
"""

# Diccionario con las cuentas contables y sus rangos
dic = {
    "Activo": (100000,299999), 
    "Disponibilidades": (110000,119999),
    "Disponibilidades en pesos": (111000,114999), "Caja $": (111001,111011), "BCRA $": (111015,111025), 
    "Disponibilidades en ME": (115000,116999), "Caja ME": (115001,115009), "BCRA ME": (115015,115019),
    "Titulos públicos y privados":(120000,126999),
    "Titulos públicos y privados en pesos":(121000,124999),"Titulos públicos y privados en ME":(125000,126999),
    "Prestamos": (130000,139999), 
    "Prestamos en pesos": (131000,132999), "Prestamos en ME": (135000,136999),
    "Prestamos sector publico no fcro pesos": (131100,131399), "Prestamos sector publico no fcro ME": (135100,135399),
    "Prestamos sector privado no fcro pesos": (131700,131999), "Prestamos privado no fcro ME": (135700,135999),
    "Prestamos Comerciales": ([131709,131711,131712,131714,131715,131718,131719,131721,
                               135709,135711,135712,135714,135715,135718,135719,135721]),
    "Prevision": ([131601,131606,131901,131907,132301,132307,135601,135606,135901,135907,136301,136307]),    
    "OCIF": (140000,149999), "Creditos por arrendamiento financiero": (150000,159999), "Participación en otras sociedades": (160000,169999), "Créditos diversos": (170000,179999),
    "Propiedad Planta y Equipo":(180000,189999), "Bienes Diversos": (190000,199999), "Activos Intangibles":(210000,219999), "filiales del exterior":(220000,229999), "PPI Deudoras": (230000,239999), 
    
    "Pasivo": (300000,399999),
    "Depositos":(310000,319999),
    "Depositos en pesos":(311000,314999),
    "Depositos a la vista $":(311700,311728), "Depositos a plazo $":(311740,311744),
    "Depositos en ME":(315000,316999), 
    "Depositos a la vista en ME":(315700,315725), "Depositos a plazo ME":(315731, 315750),
    
    "OOIF":(320000,329999), "Obligaciones Diversas":(330000,339999), "Provisiones": (340000,349999), "PPI Pasivo":(350000,359999), "Obligaciones subordinadas":(360000,369999), 
    "PN": (400000,499999), 
    "Capital social": (410000,429999), "Ajuste al Capital": (430000,439999), "Reserva de Utilidades": (440000,449999), "Reserva Legal": (440000,440003), "Resultados no asignados": (450000,469999),
    "PN FINAL": (400000,699999), 
    "Ingresos financieros": (510000,519999), "Egresos financieros": (520000,529999), "Cargo por Incobrabilidad": (530000,539999),
    "Ingresos por servicios": (540000,549999), "Egresos por servicios": (550000,559999), "Gastos de Administracion": (560000,569999), "Gastos de Personal": (560000,560027), "Utilidades diversas": (570000,579999),
    "Perdidas diversas": (580000,589999), "Utilidad neta": (500000,649999)
}

# Diccionario para recorrer, y True o False según haya que multiplicar *-1
cl = { 
    "Activo": True, "Pasivo" : False, "PN" : False, 
    "Disponibilidades" : True, "Disponibilidades en pesos" : True, "Caja $" : True, "BCRA $" : True, 
    "Disponibilidades en ME" : True,  "Caja ME" : True, "BCRA ME" : True,      
    "Titulos públicos y privados" : True, "Titulos públicos y privados en pesos": True, "Titulos públicos y privados en ME":True,
    "Prestamos": True, "Prestamos en pesos": True, "Prestamos en ME": True,
    "Prestamos sector publico no fcro pesos": True, "Prestamos sector publico no fcro ME": True,
    "Prestamos sector privado no fcro pesos": True, "Prestamos privado no fcro ME": True, "Prestamos Comerciales": True,"OCIF": True,  "Propiedad Planta y Equipo": True, "Créditos diversos": True,
    "Participación en otras sociedades": True, "Activos Intangibles":True, "PPI Deudoras": True,
    
    "Depositos" : False, "Depositos en pesos": False,"Depositos a la vista $": False, "Depositos a plazo $": False,"OOIF": False,
    "Depositos en ME": False, "Depositos a la vista en ME": False, "Depositos a plazo ME": False,
    "Capital social": False, "Reserva Legal": False, "PN FINAL": False, 
    "Ingresos financieros" : False,  "Cargo por Incobrabilidad": True, "Egresos financieros": True, "Ingresos por servicios": False, "Egresos por servicios":True,
    "Gastos de Administracion" : True, "Utilidades diversas": False, "Perdidas diversas": True, "Gastos de Personal": True, "Utilidad neta" : False 
}

# Orden de columnas para el DataFrame final
columnas = [
    "Entidad", "Periodo", "Activo","Disponibilidades", "Disponibilidades en pesos", "Caja $", "BCRA $", "Disponibilidades en ME",  "Caja ME", "BCRA ME",
    "Titulos públicos y privados",  "Titulos públicos y privados en pesos", "Titulos públicos y privados en ME", "Letras y Notas BCRA",
    "Prestamos", "Prestamos totales", "Volumen de Negocio",  # ← NUEVO
    "Prestamos en pesos", "Prestamos en ME", 
    "Prestamos sector publico no fcro pesos", "Prestamos sector publico no fcro ME","Prestamos sector privado no fcro pesos", "Prestamos privado no fcro ME", "OCIF",
    "Prestamos Comerciales",  "Propiedad Planta y Equipo", "Créditos diversos", "Participación en otras sociedades", "Activos Intangibles", "PPI Deudoras",
    "Pasivo", "Depositos", 
    "Depositos en pesos", "Depositos a la vista $", "Depositos a plazo $","Depositos en ME","Depositos a la vista en ME", "Depositos a plazo ME","OOIF",
    "PN","Capital social", "PN FINAL", "Reserva Legal", "Previsiones", "Ingresos financieros", "Egresos financieros", "Ingresos por servicios", "Egresos por servicios", 
    "Gastos de Administracion", "Cargo por Incobrabilidad","Utilidades diversas", "Perdidas diversas","Gastos de Personal", "Utilidad neta"
]

# RATIOS FINANCIEROS - Definiciones para cálculo
ratios_definiciones = {
    # Estructura de Activos
    "I1": "Disponibilidades / Activo",  # Liquidez inmediata
    "I2": "Prestamos / Activo",  # Participación préstamos
    "I3": "Titulos públicos y privados / Activo",  # Participación títulos
    "I4": "Propiedad Planta y Equipo / Activo",  # Activos fijos
    "I6": "OCIF / Activo",  # Otras entidades financieras
    "I7": "(Prestamos + Titulos públicos y privados) / Activo",  # Activos productivos
    
    # Estructura Patrimonial
    "I8": "Depositos / (Pasivo + PN FINAL)",  # Participación depósitos
    "I9": "OOIF / Pasivo",  # Otras obligaciones
    "I10": "(Capital social + Reserva Legal) / (Pasivo + PN FINAL)",  # Capital básico
    "I11": "PN FINAL / (Pasivo + PN FINAL)",  # Participación patrimonio
    
    # Cartera de Préstamos
    "I12": "Prestamos / Prestamos totales",  # Calidad cartera
    "I13": "Prestamos en pesos / Prestamos totales",  # Préstamos en pesos
    "I14": "Prestamos en ME / Prestamos totales",  # Préstamos en ME
    "I16": "Previsiones / Prestamos totales",  # Provisiones
    
    # Liquidez
    "I17": "Disponibilidades / Depositos",  # Liquidez básica
    "I18": "Disponibilidades / (Depositos + OOIF)",  # Liquidez ampliada
    "I19": "(Disponibilidades + Titulos públicos y privados) / Activo",  # Activos líquidos
    
    # Eficiencia Administrativa
    "I20": "(Prestamos + Titulos públicos y privados) / (Depositos + OOIF)",  # Intermediación
    "I21": "Gastos de Administracion / Depositos",  # Costo administrativo
    "I22": "Gastos de Personal / Gastos de Administracion",  # Participación personal
    "I24": "Gastos de Administracion / (Gastos de Administracion + Egresos financieros)",  # Eficiencia
    "I27": "Egresos financieros / (Depositos a plazo $ + Depositos a plazo ME)",  # Costo fondeo
    "I29": "Utilidad neta / PN FINAL",  # ROE
    
    # Otros Indicadores
    "I30": "Gastos de Administracion / Ingresos financieros",  # Ratio eficiencia
    "I31": "Prestamos sector publico no fcro pesos / Prestamos totales",  # Expo sector público
    "I32": "Prestamos sector privado no fcro pesos / Prestamos totales",  # Expo sector privado
    "I33": "Prestamos Comerciales / Prestamos totales",  # Préstamos comerciales
    "I34": "Capital social / Activo",  # Capital sobre activo
    "I35": "Depositos a plazo $ / Depositos en pesos",  # Estructura depósitos pesos
    "I36": "Depositos a plazo ME / Depositos en ME",  # Estructura depósitos ME
    "I37": "Prestamos totales / Depositos",  # Ratio préstamos/depósitos
    "I38": "Pasivo / PN FINAL",  # Apalancamiento
    "I39": "Activo / Pasivo",  # Cobertura activos
    "I40": "PN FINAL / Activo",  # Capitalización
    "I41": "Utilidad neta / Activo",  # ROA
    "I42": "(Propiedad Planta y Equipo + Créditos diversos) / PN FINAL",  # Activos inmovilizados
    "I43": "Cargo por Incobrabilidad / (Ingresos financieros + Egresos financieros + Ingresos por servicios + Egresos por servicios)"  # Calidad cartera
}

# Descripciones de los ratios para la aplicación web
ratios_descripciones = {
    "I1": "Liquidez Inmediata - Disponibilidades sobre Activo Total",
    "I2": "Participación Préstamos - Préstamos sobre Activo Total", 
    "I3": "Participación Títulos - Títulos sobre Activo Total",
    "I4": "Activos Fijos - PPE sobre Activo Total",
    "I6": "Exposición OCIF - OCIF sobre Activo Total",
    "I7": "Activos Productivos - (Préstamos + Títulos) sobre Activo",
    "I8": "Estructura Pasivo - Depósitos sobre Total Pasivo+PN",
    "I9": "Otras Obligaciones - OOIF sobre Pasivo Total",
    "I10": "Capital Básico - (Capital + Reservas) sobre Total",
    "I11": "Capitalización - PN sobre Total Pasivo+PN",
    "I12": "Calidad Cartera - Préstamos sobre Total Préstamos",
    "I13": "Préstamos Pesos - Préstamos $ sobre Total Préstamos",
    "I14": "Préstamos ME - Préstamos ME sobre Total Préstamos", 
    "I16": "Provisiones - Previsiones sobre Total Préstamos",
    "I17": "Liquidez Básica - Disponibilidades sobre Depósitos",
    "I18": "Liquidez Ampliada - Disponibilidades sobre (Depósitos + OOIF)",
    "I19": "Activos Líquidos - (Disponibilidades + Títulos) sobre Activo",
    "I20": "Intermediación - Activos Productivos sobre Fondeo Total",
    "I21": "Costo Administrativo - Gastos Admin sobre Depósitos",
    "I22": "Eficiencia Personal - Gastos Personal sobre Gastos Admin",
    "I24": "Eficiencia Operativa - Gastos Admin sobre Total Gastos",
    "I27": "Costo Fondeo - Egresos Financieros sobre Depósitos Plazo",
    "I29": "ROE - Utilidad Neta sobre Patrimonio Neto",
    "I30": "Ratio Eficiencia - Gastos Admin sobre Ingresos Financieros",
    "I31": "Exposición Sector Público - Préstamos Públicos sobre Total",
    "I32": "Exposición Sector Privado - Préstamos Privados sobre Total",
    "I33": "Préstamos Comerciales - Comerciales sobre Total Préstamos",
    "I34": "Capital sobre Activo - Capital Social sobre Activo",
    "I35": "Estructura Dep Pesos - Dep Plazo $ sobre Dep Pesos",
    "I36": "Estructura Dep ME - Dep Plazo ME sobre Dep ME",
    "I37": "Préstamos/Depósitos - Total Préstamos sobre Depósitos",
    "I38": "Apalancamiento - Pasivo sobre Patrimonio Neto",
    "I39": "Cobertura Activos - Activo sobre Pasivo",
    "I40": "Capitalización - PN sobre Activo Total",
    "I41": "ROA - Utilidad Neta sobre Activo Total",
    "I42": "Activos Inmovilizados - (PPE + Créd Diversos) sobre PN",
    "I43": "Calidad Cartera - Incobrabilidad sobre Ingresos Totales"
}