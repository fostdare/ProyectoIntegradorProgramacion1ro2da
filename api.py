# api.py
# Módulo que expone el backend del Clon de Trello como API REST en FastAPI
# Cumple el Eje de Investigación C (API Propia)

from fastapi import FastAPI, HTTPException
import persistencia
import estructuras

app = FastAPI(title="Trello Clon API - Programación I")

@app.get("/tareas")
def obtener_todas_las_tareas():
    """Retorna la lista completa de tareas desde el archivo JSON."""
    tareas = persistencia.cargar_datos_json()
    return {"tareas": tareas}

@app.get("/tareas/estadisticas")
def obtener_estadisticas():
    """Calcula y retorna las estadísticas actuales del tablero."""
    tareas = persistencia.cargar_datos_json()
    stats = estructuras.calcular_estadisticas_productividad(tareas)
    return {"estadisticas": stats}

@app.post("/tareas")
def crear_nueva_tarea(titulo: str, descripcion: str, prioridad: int, categoria: str, responsable: str, fecha_limite: str):
    """Crea una tarea desde la API REST y actualiza la persistencia."""
    tareas = persistencia.cargar_datos_json()
    nuevo_id = estructuras.obtener_siguiente_id(tareas)
    nueva_tarea = estructuras.crear_tarea(
        nuevo_id, titulo, descripcion, prioridad, "pendiente", categoria, responsable, fecha_limite
    )
    tareas.append(nueva_tarea)
    persistencia.guardar_datos_json(persistencia.RUTA_JSON, tareas)
    persistencia.registrar_log(persistencia.RUTA_LOG, "API_CREAR_TAREA", f"Creada tarea ID {nuevo_id} vía REST")
    return {"mensaje": "Tarea creada con éxito", "tarea": nueva_tarea}

@app.put("/tareas/{id_tarea}/estado")
def actualizar_estado(id_tarea: int, nuevo_estado: str):
    """Actualiza el estado de una tarea por ID."""
    if nuevo_estado not in ["pendiente", "en_curso", "finalizada"]:
        raise HTTPException(status_code=400, detail="Estado inválido")
    
    tareas = persistencia.cargar_datos_json()
    exito = estructuras.cambiar_estado_tarea(tareas, id_tarea, nuevo_estado)
    if not exito:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
    persistencia.guardar_datos_json(persistencia.RUTA_JSON, tareas)
    persistencia.registrar_log(persistencia.RUTA_LOG, "API_CAMBIAR_ESTADO", f"Tarea {id_tarea} a {nuevo_estado}")
    return {"mensaje": f"Estado actualizado a {nuevo_estado}"}