import pandas as pd

def solicitar_datos_usuario():
    nombre_departamento = input("Por favor, ingresa el nombre del departamento (MAYÚSCULAS) a consultar: ").strip()
    
    while True:
        limite_registros = input("Por favor, ingresa la cantidad de datos que deseas obtener: ").strip()
        if limite_registros.isdigit():
            limite_registros = int(limite_registros)
            break
        else:
            print("Error: Debes ingresar un número válido para la cantidad de registros.")
    
    return nombre_departamento, limite_registros

def mostrar_resultados(datos_df):
    if datos_df.empty:
        print("No hay datos para mostrar.")
        return
    
    datos_df = datos_df.copy()  # Crear una copia para evitar modificar el original

    # Renombrar columnas para mayor claridad
    datos_df.rename(columns={
        'ciudad_municipio_nom': 'Ciudad de ubicación',
        'departamento_nom': 'Departamento',
        'edad': 'Edad',
        'fuente_tipo_contagio': 'Tipo de contagio',
        'estado': 'Estado',
        'pais_viajo_1_nom': 'País de procedencia'
    }, inplace=True)

    # Seleccionar columnas a mostrar
    columnas_a_mostrar = [
        'Ciudad de ubicación',
        'Departamento',
        'Edad',
        'Tipo de contagio',
        'Estado',
        'País de procedencia'
    ]
    columnas_existentes = [col for col in columnas_a_mostrar if col in datos_df.columns]

    # Mostrar datos en formato legible
    print("\nDatos obtenidos:\n")
    for indice, fila in datos_df[columnas_existentes].iterrows():
        print("------ Registro {} ------".format(indice + 1))
        for columna in columnas_existentes:
            valor = fila[columna] if pd.notnull(fila[columna]) else 'No disponible'
            print("{:<22}: {}".format(columna, valor))
        print("-" * 40)
