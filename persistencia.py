# persistencia.py
# Módulo encargado de la lectura y escritura de archivos (JSON, CSV, TXT)
# Rutas actualizadas para usar rutas absolutas basadas en la ubicación del módulo.

import json
import csv
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RUTA_JSON = os.path.join(BASE_DIR, "tareas.json")
RUTA_CSV = os.path.join(BASE_DIR, "reporte_tareas.csv")
RUTA_LOG = os.path.join(BASE_DIR, "log_actividad.txt")

def cargar_datos_json(ruta_archivo=RUTA_JSON):
    """
    Carga las tareas desde un archivo JSON. Si no existe, genera el archivo vacío.
    """
    if not os.path.exists(ruta_archivo):
        guardar_datos_json(ruta_archivo, [])
        return []
    
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            datos = json.load(f)
            return datos
    except (FileNotFoundError, IOError, json.JSONDecodeError) as err:
        print(f"Error al cargar archivo JSON: {err}")
        return []

def guardar_datos_json(ruta_archivo, datos):
    """
    Guarda la lista de tareas en un archivo JSON usando bloque with.
    """
    try:
        with open(ruta_archivo, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)
        return True
    except IOError as err:
        print(f"Error al guardar datos JSON: {err}")
        return False

def exportar_reporte_csv(ruta_archivo, lista_tareas):
    """
    Exporta la lista de tareas a un archivo CSV.
    """
    columnas = ["id", "titulo", "descripcion", "prioridad", "estado", "categoria", "responsable", "fecha_limite"]
    try:
        with open(ruta_archivo, "w", newline="", encoding="utf-8") as f:
            escritor = csv.DictWriter(f, fieldnames=columnas)
            escritor.writeheader()
            for tarea in lista_tareas:
                escritor.writerow(tarea)
        return True
    except IOError as err:
        print(f"Error al exportar archivo CSV: {err}")
        return False

def registrar_log(ruta_archivo, accion, detalle):
    """
    Registra eventos y acciones del usuario con fecha y hora en un log TXT.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linea_log = f"[{timestamp}] ACCION: {accion} | DETALLE: {detalle}\n"
    try:
        with open(ruta_archivo, "a", encoding="utf-8") as f:
            f.write(linea_log)
        return True
    except IOError as err:
        print(f"Error al escribir en el log TXT: {err}")
        return False
