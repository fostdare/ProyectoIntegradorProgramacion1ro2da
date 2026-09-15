# estructuras.py
# Módulo de estructuras de datos y lógica del dominio (Gestor de Tareas / Trello)

def crear_tarea(id_tarea, titulo, descripcion, prioridad, estado, categoria, responsable, fecha_limite):
    """
    Construye y retorna un diccionario que representa una tarea del tablero.
    """
    return {
        "id": id_tarea,
        "titulo": titulo,
        "descripcion": descripcion,
        "prioridad": prioridad,  # 1: Alta, 2: Media, 3: Baja
        "estado": estado,        # pendiente, en_curso, finalizada
        "categoria": categoria,
        "responsable": responsable,
        "fecha_limite": fecha_limite
    }

def obtener_siguiente_id(lista_tareas):
    """
    Calcula el siguiente ID disponible para una nueva tarea.
    """
    if not lista_tareas:
        return 1
    max_id = max(tarea["id"] for tarea in lista_tareas)
    return max_id + 1

def filtrar_tareas(lista_tareas, estado=None, categoria=None, responsable=None):
    """
    Filtra la lista de tareas según los criterios especificados.
    """
    resultados = []
    for tarea in lista_tareas:
        cumple_estado = (estado is None or tarea["estado"].lower() == estado.lower())
        cumple_categoria = (categoria is None or tarea["categoria"].lower() == categoria.lower())
        cumple_responsable = (responsable is None or responsable.lower() in tarea["responsable"].lower())
        
        if cumple_estado and cumple_categoria and cumple_responsable:
            resultados.append(tarea)
    return resultados

def ordenar_tareas_por_prioridad(lista_tareas):
    """
    Ordena una copia de la lista de tareas por prioridad (1: Alta a 3: Baja).
    """
    lista_copia = list(lista_tareas)
    n = len(lista_copia)
    # Algoritmo de ordenamiento por burbuja
    for i in range(n):
        for j in range(0, n - i - 1):
            if lista_copia[j]["prioridad"] > lista_copia[j + 1]["prioridad"]:
                lista_copia[j], lista_copia[j + 1] = lista_copia[j + 1], lista_copia[j]
    return lista_copia

def cambiar_estado_tarea(lista_tareas, id_tarea, nuevo_estado):
    """
    Modifica el estado de una tarea por su ID. Retorna True si tuvo éxito.
    """
    for tarea in lista_tareas:
        if tarea["id"] == id_tarea:
            tarea["estado"] = nuevo_estado
            return True
    return False

def calcular_estadisticas_productividad(lista_tareas):
    """
    Calcula y retorna estadísticas descriptivas del tablero de tareas.
    """
    total = len(lista_tareas)
    if total == 0:
        return {
            "total_tareas": 0,
            "pendientes": 0,
            "en_curso": 0,
            "finalizadas": 0,
            "porcentaje_completadas": 0.0
        }
    
    pendientes = sum(1 for t in lista_tareas if t["estado"] == "pendiente")
    en_curso = sum(1 for t in lista_tareas if t["estado"] == "en_curso")
    finalizadas = sum(1 for t in lista_tareas if t["estado"] == "finalizada")
    porcentaje = (finalizadas / total) * 100

    return {
        "total_tareas": total,
        "pendientes": pendientes,
        "en_curso": en_curso,
        "finalizadas": finalizadas,
        "porcentaje_completadas": round(porcentaje, 2)
    }