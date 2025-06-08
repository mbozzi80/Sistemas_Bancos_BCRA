"""
Configuración y estructura de datos del BCRA
Este archivo contie todos los diccionarios y configuraciones para el procesamito de datos bancarios
"""

# Diccionario con las cutas contables y sus rangos
dic = {
    "Activo": (100000,299999), 
    "Disponibilidades": (110000,119999),
    "Disponibilidades ARS": (111000,114999), "Caja ARS": (111001,111011), "BCRA ARS": (111015,111025), 
    "Disponibilidades USD": (115000,116999), "Caja USD": (115001,115009), "BCRA USD": (115015,115019),
    "Titulos públicos y privados":(120000,126999),
    "Titulos públicos y privados ARS":(121000,124999),"Titulos públicos y privados USD":(125000,126999),
    'Tit pub a Costo + TIR': ([121016]), 'Tit pub a VR': ([121003]),
    "Instrumtos BCRA": ([121056, 121057,121058, 121024,121026,121041,121091,121092,121093, 141143, 141144, 141176,141153]),  # Letras y Notas del BCRA 
        
    "Prestamos": (130000,139999), # son prestamos netos de previsiones
    "Prestamos ARS": (131000,132999), "Prestamos USD": (135000,136999),
    "Prestamos SP ARS": (131100,131399), "Prestamos SP USD": (135100,135399),
    "Prestamos SPNF ARS": (131700,131999), "Prestamos SPNF USD": (135700,135999),
    "Prestamos Comerciales": ([131709,131711,131712,131714,131715,131718,131719,131721,
                               135709,135711,135712,135714,135715,135718,135719,135721]),
    "Prevision": ([131601,131606,131901,131905,131907,132301,132307,135601,135606,135901,135905,135907,136301,136307]),    
    
    # Préstamos Sector Privado No Financiero (SPNF)
    'Prestamos personales ARS': ([131731, 131749]), 
    'Prestamos hipotecarios ARS + UVA': ([131708, 131711,131745,131746,131809,131810,131816,131817,131866,131867]),
    'Tarjetas de Crédito ARS': ([131742]), 'Documentos descontados ARS': ([131718, 131791]),
    'Prefinancacion de Expor USD': ([135799]), 'Doc a sola firma ARS':([131718,136121]), 'Adelantos ARS':([131709,131712,135709]),
    'Doc a sola firma USD':([135715]), 'Tarjetas de Crédito USD': ([135742]),
    
    "OCIF": (140000,149999), "Creditos por arrendamiento financiero": (150000,159999), "Participación  otras sociedades": (160000,169999), "Créditos diversos": (170000,179999),
    "Propiedad Planta y Equipo":(180000,189999), "Bienes Diversos": (190000,199999), "Activos Intangibles":(210000,219999), "Filiales del exterior":(220000,229999), "PPI Deudoras": (230000,239999), 
    
    "Pasivo": (300000,399999),
    "Depositos":(310000,319999),
    "Depositos ARS":(311000,314999),
    "Depositos a la vista ARS":(311700,311728), "Depositos a plazo ARS":(311740,311744),
    "Depositos USD":(315000,316999), 
    "Depositos a la vista USD":(315700,315725), "Depositos a plazo USD":(315731, 315750),
    
    # Depósitos Sector Público (SP)
    'Cta Cte SP ARS': ([311106, 311113,311142,311145,311151,311191,311211]),
    'Cta Cte SP USD': ([315113,315142]),
    'Cja Ahorro SP ARS':([311123,311124]),
    'Cja Ahorro SP USD':([315123]),
    'Pzo Fijo SP ARS':([311131,311140,311153,311156]),
    'Pzo Fijo SP UVA':([311766,311767,311785,311789]),
    'Pzo Fijo SP USD':([315132,315137]),


    # Depósitos Sector Privado No Financiero (SPNF)
    'Ctas Remuneradas SPNF': ([311712,311724]),
    'Cta Cte ARS SPNF': ([311706, 311712,311725,311730,311742,311745,311751]),
    'Cja Ahorro ARS SPNF':([311718,311722,311723,311724,311726,311790,311791,311792,311793]),
    'Cja Ahorro USD SPNF':([315718,315784,315786,315788,315790,315793,315794]),
    'Pzo Fijo ARS SPNF':([311731,311736,311740,311744]),
    'Pzo Fijo UVA SPNF':([311766,311767,311785,311789]),
    'Pzo Fijo USD SPNF':([315732,315737,315785,315787,315789]),

    "OOIF":(320000,329999), "Obligaciones Diversas":(330000,339999), "Provisiones": (340000,349999), "PPI Pasivo":(350000,359999), "Obligaciones subordinadas":(360000,369999), 
    "PN": (400000,499999), 
    "Capital social": (410000,429999), "Ajuste al Capital": (430000,439999), "Reserva de Utilidades": (440000,449999), "Reserva Legal": (440000,440003), "Resultados no asignados": (450000,469999),
    "PN FINAL": (400000,699999), 
    "Ingresos financieros": (510000,519999), "Egresos financieros": (520000,529999), "Cargo por Incobrabilidad": (530000,539999),
    "Ingresos por servicios": (540000,549999), "Egresos por servicios": (550000,559999), "Gastos de Administracion": (560000,569999), "Gastos de Personal": (560000,560027), "Utilidades diversas": (570000,579999),
    "Perdidas diversas": (580000,589999), "Utilidad neta": (500000,649999)
}

# Diccionario para recorrer, y True o False según haya que multiplicar *-1
# Diccionario para multiplicadores (True = positivo, False = negativo)
cl = { 
    # ACTIVOS (todos positivos)
    "Activo": True, 
    "Disponibilidades": True, "Disponibilidades ARS": True, "Caja ARS": True, "BCRA ARS": True, 
    "Disponibilidades USD": True, "Caja USD": True, "BCRA USD": True,
    
    # TÍTULOS (todos positivos)
    "Titulos públicos y privados": True, "Titulos públicos y privados ARS": True, "Titulos públicos y privados USD": True,
    "Tit pub a Costo + TIR": True, "Tit pub a VR": True, "Instrumtos BCRA": True,
    
    # PRÉSTAMOS (todos positivos)
    "Prestamos": True, "Prestamos ARS": True, "Prestamos USD": True,
    "Prestamos SP ARS": True, "Prestamos SP USD": True,
    "Prestamos SPNF ARS": True, "Prestamos SPNF USD": True, 
    "Prestamos Comerciales": True, "Prevision": True,
    
    # PRÉSTAMOS DETALLADOS (todos positivos)
    "Prestamos personales ARS": True, "Prestamos hipotecarios ARS + UVA": True, 
    "Tarjetas de Crédito ARS": True, "Documentos descontados ARS": True,
    "Prefinancacion de Expor USD": True, "Doc a sola firma ARS": True,
    "Adelantos ARS": True, "Doc a sola firma USD": True, "Tarjetas de Crédito USD": True,
    
    # OTROS ACTIVOS (todos positivos)
    "OCIF": True, "Creditos por arrendamiento financiero": True, 
    "Participación otras sociedades": True, "Créditos diversos": True,
    "Propiedad Planta y Equipo": True, "Bienes Diversos": True,
    "Activos Intangibles": True, "Filiales del exterior": True, "PPI Deudoras": True,
    
    # PASIVOS (todos negativos)
    "Pasivo": False,
    "Depositos": False, "Depositos ARS": False, "Depositos USD": False,
    "Depositos a la vista ARS": False, "Depositos a plazo ARS": False,
    "Depositos a la vista USD": False, "Depositos a plazo USD": False,
    
    # DEPÓSITOS SECTOR PÚBLICO (todos negativos)
    "Cta Cte SP ARS": False, "Cta Cte SP USD": False, 
    "Cja Ahorro SP ARS": False, "Cja Ahorro SP USD": False,
    "Pzo Fijo SP ARS": False, "Pzo Fijo SP UVA": False, "Pzo Fijo SP USD": False,
    
    # DEPÓSITOS SPNF (todos negativos)
    "Ctas Remuneradas SPNF": False, "Cta Cte ARS SPNF": False, "Cja Ahorro ARS SPNF": False,
    "Cja Ahorro USD SPNF": False, "Pzo Fijo ARS SPNF": False, 
    "Pzo Fijo UVA SPNF": False, "Pzo Fijo USD SPNF": False,
    
    # OTROS PASIVOS (todos negativos)
    "OOIF": False, "Obligaciones Diversas": False, "Provisiones": False, 
    "PPI Pasivo": False, "Obligaciones subordinadas": False,
    
    # PATRIMONIO NETO (todos negativos)
    "PN": False, "Capital social": False, "Ajuste al Capital": False, 
    "Reserva de Utilidades": False, "Reserva Legal": False,
    "Resultados no asignados": False, "PN FINAL": False,
    
    # RESULTADOS (ingresos negativos, gastos positivos)
    "Ingresos financieros": False, "Egresos financieros": True, 
    "Cargo por Incobrabilidad": True, "Ingresos por servicios": False, 
    "Egresos por servicios": True, "Gastos de Administracion": True, 
    "Gastos de Personal": True, "Utilidades diversas": False, 
    "Perdidas diversas": True, "Utilidad neta": False 
}

# Ord de columnas para el DataFraUSD final
columnas = [
    "Entidad", "Periodo", 
    
    # ACTIVOS
    "Activo",
    "Disponibilidades", "Disponibilidades ARS", "Caja ARS", "BCRA ARS", 
    "Disponibilidades USD", "Caja USD", "BCRA USD",
    
    ## TÍTULOS
    "Titulos públicos y privados", "Titulos públicos y privados ARS", "Titulos públicos y privados USD",
    "Tit pub a Costo + TIR", "Tit pub a VR", "Instrumtos BCRA",
    
    ## PRÉSTAMOS GENERALES
    "Prestamos", "Prestamos ARS", "Prestamos USD",
    "Prestamos SP ARS", "Prestamos SP USD", "Prestamos SPNF ARS", "Prestamos SPNF USD",
    "Prestamos Comerciales", "Prevision",
    
    ## PRÉSTAMOS Sector Privado No Financiero (SPNF)
    "Prestamos personales ARS", "Prestamos hipotecarios ARS + UVA", "Tarjetas de Crédito ARS",
    "Documentos descontados ARS", "Prefinancacion de Expor USD", "Doc a sola firma ARS",
    "Adelantos ARS", "Doc a sola firma USD", "Tarjetas de Crédito USD",
    
    # OTROS ACTIVOS
    "OCIF", "Creditos por arrendamiento financiero", "Participación otras sociedades",
    "Créditos diversos", "Propiedad Planta y Equipo", "Bienes Diversos",
    "Activos Intangibles", "Filiales del exterior", "PPI Deudoras",
    
    # PASIVOS
    "Pasivo",
    "Depositos", "Depositos ARS", "Depositos USD",
    "Depositos a la vista ARS", "Depositos a plazo ARS",
    "Depositos a la vista USD", "Depositos a plazo USD",
    
    # DEPÓSITOS SECTOR PÚBLICO (SP)
    "Cta Cte SP ARS", "Cta Cte SP USD", "Cja Ahorro SP ARS", "Cja Ahorro SP USD",
    "Pzo Fijo SP ARS", "Pzo Fijo SP UVA", "Pzo Fijo SP USD",
    
    # DEPÓSITOS SECTOR PRIVADO NO FINANCIERO (SPNF)
    "Ctas Remuneradas SPNF", "Cta Cte ARS SPNF", "Cja Ahorro ARS SPNF",
    "Cja Ahorro USD SPNF", "Pzo Fijo ARS SPNF", "Pzo Fijo UVA SPNF", "Pzo Fijo USD SPNF",
    
    # OTROS PASIVOS
    "OOIF", "Obligaciones Diversas", "Provisiones", "PPI Pasivo", "Obligaciones subordinadas",
    
    # PATRIMONIO NETO
    "PN", "Capital social", "Ajuste al Capital", "Reserva de Utilidades", "Reserva Legal",
    "Resultados no asignados", "PN FINAL",
    
    # RESULTADOS
    "Ingresos financieros", "Egresos financieros", "Cargo por Incobrabilidad",
    "Ingresos por servicios", "Egresos por servicios", "Gastos de Administracion",
    "Gastos de Personal", "Utilidades diversas", "Perdidas diversas", "Utilidad neta"
]

# RATIOS FINANCIEROS - Definiciones para cálculo
ratios_definiciones = {
    # Estructura de Activos
    "I1": "Disponibilidades / Activo",  # Liquidez inmediata
    "I2": "Prestamos / Activo",  # Participación préstamos
    "I3": "Titulos públicos y privados / Activo",  # Participación títulos
    "I4": "Propiedad Planta y Equipo / Activo",  # Activos fijos
    "I6": "OCIF / Activo",  # Otras tidades financieras
    "I7": "(Prestamos + Titulos públicos y privados) / Activo",  # Activos productivos
    
    # Estructura Patrimonial
    "I8": "Depositos / (Pasivo + PN FINAL)",  # Participación depósitos
    "I9": "OOIF / Pasivo",  # Otras obligaciones
    "I10": "(Capital social + Reserva Legal) / (Pasivo + PN FINAL)",  # Capital básico
    "I11": "PN FINAL / (Pasivo + PN FINAL)",  # Participación patrimonio
    
    # Cartera de Préstamos
    "I12": "Prestamos / Prestamos totales",  # Calidad cartera
    "I13": "Prestamos  ARS / Prestamos totales",  # Préstamos  ARS
    "I14": "Prestamos  USD / Prestamos totales",  # Préstamos  USD
    "I16": "Previsiones / Prestamos totales",  # Provisiones
    
    # Liquidez
    "I17": "Disponibilidades / Depositos",  # Liquidez básica
    "I18": "Disponibilidades / (Depositos + OOIF)",  # Liquidez ampliada
    "I19": "(Disponibilidades + Titulos públicos y privados) / Activo",  # Activos líquidos
    
    # Eficicia Administrativa
    "I20": "(Prestamos + Titulos públicos y privados) / (Depositos + OOIF)",  # Intermediación
    "I21": "Gastos de Administracion / Depositos",  # Costo administrativo
    "I22": "Gastos de Personal / Gastos de Administracion",  # Participación personal
    "I24": "Gastos de Administracion / (Gastos de Administracion + Egresos financieros)",  # Eficicia
    "I27": "Egresos financieros / (Depositos a plazo ARS + Depositos a plazo USD)",  # Costo fondeo
    "I29": "Utilidad neta / PN FINAL",  # ROE
    
    # Otros Indicadores
    "I30": "Gastos de Administracion / Ingresos financieros",  # Ratio eficicia
    "I31": "Prestamos SPARS / Prestamos totales",  # Expo sector público
    "I32": "Prestamos SPNF ARS / Prestamos totales",  # Expo sector privado
    "I33": "Prestamos CoUSDrciales / Prestamos totales",  # Préstamos coUSDrciales
    "I34": "Capital social / Activo",  # Capital sobre activo
    "I35": "Depositos a plazo ARS / Depositos  ARS",  # Estructura depósitos ARS
    "I36": "Depositos a plazo USD / Depositos  USD",  # Estructura depósitos USD
    "I37": "Prestamos totales / Depositos",  # Ratio préstamos/depósitos
    "I38": "Pasivo / PN FINAL",  # Apalancamito
    "I39": "Activo / Pasivo",  # Cobertura activos
    "I40": "PN FINAL / Activo",  # Capitalización
    "I41": "Utilidad neta / Activo",  # ROA
    "I42": "(Propiedad Planta y Equipo + Créditos diversos) / PN FINAL",  # Activos inmovilizados
    "I43": "Cargo por Incobrabilidad / (Ingresos financieros + Egresos financieros + Ingresos por servicios + Egresos por servicios)"  # Calidad cartera
}

# Descripciones de los ratios para la aplicación web
ratios_descripciones = {
    "I1": "Liquidez InUSDdiata - Disponibilidades sobre Activo Total",
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
    "I13": "Préstamos ARS - Préstamos ARS sobre Total Préstamos",
    "I14": "Préstamos USD - Préstamos USD sobre Total Préstamos", 
    "I16": "Provisiones - Previsiones sobre Total Préstamos",
    "I17": "Liquidez Básica - Disponibilidades sobre Depósitos",
    "I18": "Liquidez Ampliada - Disponibilidades sobre (Depósitos + OOIF)",
    "I19": "Activos Líquidos - (Disponibilidades + Títulos) sobre Activo",
    "I20": "InterUSDdiación - Activos Productivos sobre Fondeo Total",
    "I21": "Costo Administrativo - Gastos Admin sobre Depósitos",
    "I22": "Eficicia Personal - Gastos Personal sobre Gastos Admin",
    "I24": "Eficicia Operativa - Gastos Admin sobre Total Gastos",
    "I27": "Costo Fondeo - Egresos Financieros sobre Depósitos Plazo",
    "I29": "ROE - Utilidad Neta sobre Patrimonio Neto",
    "I30": "Ratio Eficicia - Gastos Admin sobre Ingresos Financieros",
    "I31": "Exposición Sector Público - Préstamos Públicos sobre Total",
    "I32": "Exposición Sector Privado - Préstamos Privados sobre Total",
    "I33": "Préstamos CoUSDrciales - CoUSDrciales sobre Total Préstamos",
    "I34": "Capital sobre Activo - Capital Social sobre Activo",
    "I35": "Estructura Dep ARS - Dep Plazo ARS sobre Dep ARS",
    "I36": "Estructura Dep USD - Dep Plazo USD sobre Dep USD",
    "I37": "Préstamos/Depósitos - Total Préstamos sobre Depósitos",
    "I38": "Apalancamito - Pasivo sobre Patrimonio Neto",
    "I39": "Cobertura Activos - Activo sobre Pasivo",
    "I40": "Capitalización - PN sobre Activo Total",
    "I41": "ROA - Utilidad Neta sobre Activo Total",
    "I42": "Activos Inmovilizados - (PPE + Créd Diversos) sobre PN",
    "I43": "Calidad Cartera - Incobrabilidad sobre Ingresos Totales"
}