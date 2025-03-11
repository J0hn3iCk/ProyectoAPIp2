import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from API import obtener_datos
from UI import solicitar_datos_usuario, mostrar_resultados

def cleanup_column_names(datos_df, rename_dict={}, do_inplace=True):
    """
    Renombra columnas de un DataFrame de Pandas.
    Convierte nombres de columnas a snake_case si rename_dict no se proporciona.
    """
    if not rename_dict:
        return datos_df.rename(
            columns={col: col.lower().replace(' ', '_') for col in datos_df.columns.values.tolist()},
            inplace=do_inplace
        )
    else:
        return datos_df.rename(columns=rename_dict, inplace=do_inplace)

def imputar_datos(datos_df):
    """Imputa valores faltantes en la columna 'edad' usando la mediana."""
    if "edad" in datos_df.columns:
        datos_df["edad"] = pd.to_numeric(datos_df["edad"], errors="coerce")
        
        # Contamos valores vacios antes de la imputación
        vacios_antes = datos_df["edad"].isnull().sum()
        print(f"\n🔍 Valores vacios en 'edad' antes de la imputación: {vacios_antes}")

        if vacios_antes > 0:
            mediana_edad = datos_df["edad"].median()
            datos_df["edad"].fillna(mediana_edad, inplace=True)
            print(f"✅ Se imputaron {vacios_antes} valores con la mediana ({mediana_edad}).")

    return datos_df

def graficar_edades(datos_df):
    """Genera un gráfico de tendencia de edad con valores reales, no normalizados."""
    if "edad" in datos_df.columns:
        plt.figure(figsize=(12, 6))
        plt.plot(datos_df.index, datos_df["edad"], marker='o', linestyle='-', color='b')
        plt.title('Tendencia de Edad')
        plt.xlabel('Índice')
        plt.ylabel('Edad')
        plt.grid()
        plt.show()
    else:
        print("\n⚠ No hay datos suficientes para generar la gráfica.")

def main():
    nombre_departamento, limite_registros = solicitar_datos_usuario()
    
    datos_df = obtener_datos(nombre_departamento, limite_registros)
    
    if datos_df.empty:
        print("No se encontraron datos. Saliendo del programa.")
        return
    else:
        mostrar_resultados(datos_df)

    # Información del DataFrame
    print("\n----- Información de los datos -----")
    print("Número de filas:", datos_df.shape[0])
    print("Número de columnas:", datos_df.shape[1])
    print("Nombre de las columnas:", datos_df.columns.values.tolist())
    print("Tipos de datos de las columnas:\n", datos_df.dtypes)

    # Verificar valores vacios
    columnas_nulas = datos_df.columns[datos_df.isnull().any()].tolist()
    print("Columnas con valores vacios:", columnas_nulas)
    print("Número de filas con valores vacios:", datos_df.isnull().any(axis=1).sum())
    print("Índices de muestra con datos vacios:", datos_df[datos_df.isnull().any(axis=1)].index.tolist()[:5])

    # Aplicar imputación en "edad"
    datos_df = imputar_datos(datos_df)

    # Normalización de columnas categóricas usando LabelEncoder
    columnas_utiles = [
        "ciudad_municipio_nom",
        "departamento_nom",
        "fuente_tipo_contagio",
        "estado",
        "pais_viajo_1_nom"
    ]
    
    for col in columnas_utiles:
        if col in datos_df.columns:
            datos_df[col] = datos_df[col].astype(str)
            encoder = LabelEncoder()
            datos_df[col] = encoder.fit_transform(datos_df[col])
    
    # Filtrar columnas útiles que existen en el DataFrame
    columnas_a_mostrar = ["edad"] + [col for col in columnas_utiles if col in datos_df.columns]
    print("\n📊 Datos normalizados y codificados:")
    print(datos_df[columnas_a_mostrar].head())

    # Mostrar información adicional del DataFrame
    print("\n📊 Valores generales:")
    print(datos_df.info())

    print("\n📊 Resumen de información:")
    print(datos_df.describe())

    # 🚀 Nueva funcionalidad: Graficar tendencia de "edad" con valores reales
    graficar_edades(datos_df)

if __name__ == "__main__":
    main()
