import requests
from zipfile import ZipFile
import os.path
import pandas as pd
from time import time


def covid_data_downloader(fecha):
    """
    Descarga la base de datos sobre covid 19 y lo descomprime
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
        print(f"La descarga tomó {total_time} segundos")

def read_covid_data(fecha):
    """
    Lee la base de datos de la carpeta y la carga como un data frame
    """
    zipname = "data/"+fecha+"COVID19MEXICO.zip"
    filename = fecha+"COVID19MEXICO.csv"

    start_time = time()
    zipfile = ZipFile(zipname)
    df = pd.read_csv(zipfile.open(filename))

    end_time = time()
    total_time = end_time - start_time

    print(f"La base de datos tardó en cargarse {total_time} segundos")
    return df
