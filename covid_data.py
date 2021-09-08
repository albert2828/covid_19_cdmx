import requests
from zipfile import ZipFile
import os.path
import pandas as pd
from time import time

#Formato fecha YYMMDD

def descarga_base_covid(fecha):
    """
    Descarga la base de datos, del día de hoy, sobre covid 19 y la descomprime
    """
    zipname = "data/"+fecha+"COVID19MEXICO.zip"
    filename = fecha+"COVID19MEXICO.csv"
    if os.path.exists(zipname):
        print("La base de datos se encuentra en la carpeta")
    else:
        start_time = time()
        url = "http://datosabiertos.salud.gob.mx/gobmx/salud/datos_abiertos/"
        url += "datos_abiertos_covid19.zip"
        r = requests.get(url)
        with open(zipname, "wb") as code:
            code.write(r.content)
        end_time = time()
        total_time = end_time - start_time
        print(r.status_code)
        if r.status_code == 200:
            print("Descarga exitosa")
            print(f"La descarga tomó {total_time} segundos")

def descarga_base_covid_antigua(fecha):
    """Descarga la base de datos de una fecha anterior a la del día actual"""
    zipname = "data/"+fecha+"COVID19MEXICO.zip"
    filename = fecha+"COVID19MEXICO.csv"
    if os.path.exists(zipname):
        print("La base de datos se encuentra en la carpeta")
    else:
        start_time = time()
        url = "http://datosabiertos.salud.gob.mx/gobmx/salud/datos_abiertos/"
        url += "historicos/20"+fecha[:2]+"/"+fecha[2:4]
        url += "/datos_abiertos_covid19_"+fecha[4:6]+"."+fecha[2:4]+"."
        url += "20"+fecha[:2]+".zip"
        r = requests.get(url)
        with open(zipname, "wb") as code:
            code.write(r.content)
        end_time = time()
        total_time = end_time - start_time
        print(r.status_code)
        if r.status_code == 200:
            print("Descarga exitosa")
            print(f"La descarga tomó {total_time} segundos")

def lee_base_covid(fecha):
    """
    Lee la base de datos de la carpeta y la carga como un data frame
    """
    zipname = "data/"+fecha+"COVID19MEXICO.zip"
    filename = fecha+"COVID19MEXICO.csv"

    try:
        start_time = time()
        zipfile = ZipFile(zipname)
        df = pd.read_csv(zipfile.open(filename), parse_dates=True)
        end_time = time()
        total_time = end_time - start_time
    except FileNotFoundError:
        print("La base de datos no se encuentra en la carpeta.")

    print(f"La base de datos tardó en cargarse {total_time} segundos")
    return df

def defuncion(x):
    '''Función que indica si el paciente falleció o no'''
    if x == '9999-99-99':
        d = 0
    else:
        d=1
    return d

def date_na(date):
    if date == "9999-99-99":
        date = "1999-01-31"
    return date

def procesa_datos_covid(fecha):
    df = lee_base_covid(fecha)
    df = df[df['ENTIDAD_RES']==9]
    df = df[df['RESULTADO_LAB']==1]
    #Agremaos una columna al dataframe que indique si el paciente falleció
    df['DEF'] = df['FECHA_DEF'].apply(defuncion)
    features = ['SEXO', 'TIPO_PACIENTE',
       'FECHA_INGRESO', 'FECHA_SINTOMAS', 'FECHA_DEF', 'INTUBADO', 'NEUMONIA',
       'EDAD', 'EMBARAZO','DIABETES', 'EPOC', 'ASMA', 'INMUSUPR', 'HIPERTENSION'
       , 'OTRA_COM','CARDIOVASCULAR', 'OBESIDAD', 'RENAL_CRONICA', 'TABAQUISMO',
        'DEF']
    df = df[features]
    df["FECHA_DEF"] = df["FECHA_DEF"].apply(date_na)
    df["FECHA_SINTOMAS"] = pd.to_datetime(df["FECHA_SINTOMAS"])
    df["FECHA_DEF"] = pd.to_datetime(df["FECHA_DEF"])
    #Indicamos si el paciente fue hospitalizado.
    df_gam["TIPO_PACIENTE"] = df_gam["TIPO_PACIENTE"].apply(lambda x: x-1)
    df_gam["EMBARAZO"]=df_gam["EMBARAZO"].apply(lambda x: x-1)
