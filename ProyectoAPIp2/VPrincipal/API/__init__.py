import pandas as pd
from sodapy import Socrata

def obtener_datos(nombre_departamento, limite_registros):
    client = Socrata("www.datos.gov.co", None)
    
    try:
        results = client.get(
            "gt2j-8ykr",
            limit=limite_registros,
            departamento_nom=nombre_departamento
        )
        
        if not results:  # Verificar si la consulta devuelve datos vacíos
            print(f"No se encontraron datos para el departamento: {nombre_departamento}")
            return pd.DataFrame()
        
        return pd.DataFrame.from_records(results)
    
    except Exception as e:
        print(f"Error al obtener los datos: {e}")
        return pd.DataFrame()  # Retorna un DataFrame vacío en caso de error
    
    finally:
        client.close()
