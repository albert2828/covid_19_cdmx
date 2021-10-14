import pandas as pd
import numpy as np
import covid_data # Código propio para descargar y leer la base de datos de la SSA

def fechas_nulas_def(fecha):
    "Función para corregir el formato de las fechas nulas"
    if fecha=="9999-99-99":
        return np.NaN
    else:
        return fecha

def sexo(s):
    "Función para modificar la variavle de sexo"
    if s==1:
        return "Másculino"
    elif s==2:
        return 'Femenino'
    else:
        return 'No especificado'

def main(fecha):
    covid_data.descarga_base_covid(fecha)
    datos = covid_data.lee_base_covid(fecha)

    # Información de los estados
    estados = pd.read_excel("./others/201128 Catalogos.xlsx", sheet_name="Catálogo de ENTIDADES")
    # Limpieza de datos de los estados para agregarlos a la base
    estados.drop("ABREVIATURA", axis=1, inplace=True)
    estados.set_index("CLAVE_ENTIDAD", inplace=True)
    # Pasar los datos a un diccionatio
    estados_dict = estados.to_dict()
    estados_dict = estados_dict["ENTIDAD_FEDERATIVA"]
    # En el catálogo de descriptores aparece 'Ciudad de México', pero Tableau necesita 'Distrito Federal'
    estados_dict[9] = 'DISTRITO FEDERAL'
    # Cambiar la clave de los estados en el dataset al nombre del estado
    datos['ENTIDAD_RES'] = datos['ENTIDAD_RES'].map(estados_dict)

    # Solo casos positivos (véase el catálogo de descriptores, catálogo de clasificación final)
    datos = datos[datos["CLASIFICACION_FINAL"]==3] 
    # Agregar una variable que indique si la persona falleció
    datos["DEF"] = (datos["FECHA_DEF"] != "9999-99-99")
    # Agregar una variable del país, para que pueda ser agregada en un mapa en Tableau
    datos["PAIS"] = "México"
    # Seleccionar en un solo dataframe las variables que voy a usar en Tableau
    variables = ["FECHA_ACTUALIZACION",'ID_REGISTRO', 'ENTIDAD_RES', 'FECHA_INGRESO', 'FECHA_DEF', 'SEXO',
                'EDAD',  'DEF', 'PAIS']
    casos_positivos = datos[variables]
    # Modificar el formato de las fechas nulas, en el caso de personas que no fallecieron
    casos_positivos["FECHA_DEF"] = casos_positivos["FECHA_DEF"].apply(fechas_nulas_def)
    # Modificando la variable de sexo
    casos_positivos["SEXO"] = casos_positivos["SEXO"].apply(sexo)

    # Guardar el dataset en un archivo csv
    casos_positivos.to_csv("data/casos_positivos.csv", sep=";")

# Descarga e importa los datos en un dataframe
fecha = "211013"
if __name__=='__main__':
    main(fecha)