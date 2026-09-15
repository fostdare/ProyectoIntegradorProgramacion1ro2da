import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Optional, List
from fastapi import APIRouter, HTTPException, Query
from jinja2 import Environment, FileSystemLoader
import estructuras
import persistencia
from app.models import TareaCreate, TareaUpdate, TareaResponse, EstadisticasResponse, MensajeResponse

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_jinja_env = Environment(loader=FileSystemLoader(os.path.join(BASE_DIR, "templates")))

ESTADOS_VALIDOS = {"pendiente", "en_curso", "finalizada"}


@router.get("/tareas", response_model=List[TareaResponse])
def obtener_tareas(
    estado: Optional[str] = Query(None),
    categoria: Optional[str] = Query(None),
    responsable: Optional[str] = Query(None),
):
    tareas = persistencia.cargar_datos_json(persistencia.RUTA_JSON)
    filtradas = estructuras.filtrar_tareas(tareas, estado=estado, categoria=categoria, responsable=responsable)
    return filtradas


@router.get("/tareas/estadisticas", response_model=EstadisticasResponse)
def obtener_estadisticas():
    tareas = persistencia.cargar_datos_json(persistencia.RUTA_JSON)
    stats = estructuras.calcular_estadisticas_productividad(tareas)
    return stats


@router.get("/tareas/filtrar", response_model=List[TareaResponse])
def filtrar_tareas(
    estado: Optional[str] = Query(None),
    categoria: Optional[str] = Query(None),
    responsable: Optional[str] = Query(None),
):
    tareas = persistencia.cargar_datos_json(persistencia.RUTA_JSON)
    resultado = estructuras.filtrar_tareas(tareas, estado=estado, categoria=categoria, responsable=responsable)
    return resultado


@router.get("/tareas/{id_tarea}", response_model=TareaResponse)
def obtener_tarea(id_tarea: int):
    tareas = persistencia.cargar_datos_json(persistencia.RUTA_JSON)
    for tarea in tareas:
        if tarea["id"] == id_tarea:
            return tarea
    raise HTTPException(status_code=404, detail="Tarea no encontrada")


@router.post("/tareas", response_model=TareaResponse)
def crear_tarea(tarea_data: TareaCreate):
    tareas = persistencia.cargar_datos_json(persistencia.RUTA_JSON)
    nuevo_id = estructuras.obtener_siguiente_id(tareas)
    nueva_tarea = estructuras.crear_tarea(
        id_tarea=nuevo_id,
        titulo=tarea_data.titulo,
        descripcion=tarea_data.descripcion,
        prioridad=tarea_data.prioridad,
        estado="pendiente",
        categoria=tarea_data.categoria,
        responsable=tarea_data.responsable,
        fecha_limite=tarea_data.fecha_limite,
    )
    tareas.append(nueva_tarea)
    persistencia.guardar_datos_json(persistencia.RUTA_JSON, tareas)
    persistencia.registrar_log(
        persistencia.RUTA_LOG, "API_CREAR_TAREA", f"Creada tarea ID {nuevo_id} vía REST"
    )
    return nueva_tarea


@router.put("/tareas/{id_tarea}", response_model=TareaResponse)
def actualizar_tarea(id_tarea: int, tarea_data: TareaUpdate):
    tareas = persistencia.cargar_datos_json(persistencia.RUTA_JSON)
    tarea_encontrada = None
    for t in tareas:
        if t["id"] == id_tarea:
            tarea_encontrada = t
            break
    if not tarea_encontrada:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    update_dict = tarea_data.model_dump(exclude_unset=True)
    for campo, valor in update_dict.items():
        if campo == "estado" and valor is not None:
            if valor not in ESTADOS_VALIDOS:
                raise HTTPException(status_code=400, detail=f"Estado inválido. Debe ser uno de: {', '.join(sorted(ESTADOS_VALIDOS))}")
        tarea_encontrada[campo] = valor

    persistencia.guardar_datos_json(persistencia.RUTA_JSON, tareas)
    persistencia.registrar_log(
        persistencia.RUTA_LOG, "API_ACTUALIZAR_TAREA", f"Tarea ID {id_tarea} actualizada vía REST"
    )
    return tarea_encontrada


@router.delete("/tareas/{id_tarea}", response_model=MensajeResponse)
def eliminar_tarea(id_tarea: int):
    tareas = persistencia.cargar_datos_json(persistencia.RUTA_JSON)
    tareas_actualizadas = [t for t in tareas if t["id"] != id_tarea]
    if len(tareas) == len(tareas_actualizadas):
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    persistencia.guardar_datos_json(persistencia.RUTA_JSON, tareas_actualizadas)
    persistencia.registrar_log(
        persistencia.RUTA_LOG, "API_ELIMINAR_TAREA", f"Tarea ID {id_tarea} eliminada vía REST"
    )
    return MensajeResponse(mensaje=f"Tarea ID {id_tarea} eliminada con éxito")


@router.put("/tareas/{id_tarea}/estado", response_model=MensajeResponse)
def cambiar_estado(id_tarea: int, nuevo_estado: str):
    if nuevo_estado not in ESTADOS_VALIDOS:
        raise HTTPException(
            status_code=400,
            detail=f"Estado inválido. Debe ser uno de: {', '.join(sorted(ESTADOS_VALIDOS))}",
        )
    tareas = persistencia.cargar_datos_json(persistencia.RUTA_JSON)
    exito = estructuras.cambiar_estado_tarea(tareas, id_tarea, nuevo_estado)
    if not exito:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    persistencia.guardar_datos_json(persistencia.RUTA_JSON, tareas)
    persistencia.registrar_log(
        persistencia.RUTA_LOG, "API_CAMBIAR_ESTADO", f"Tarea {id_tarea} cambió a {nuevo_estado} vía REST"
    )
    return MensajeResponse(mensaje=f"Estado de tarea ID {id_tarea} actualizado a {nuevo_estado}")
