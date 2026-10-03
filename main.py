# main.py
# Punto de entrada de la aplicación de consola. Gestor de Tareas / Trello Clon


import estructuras
import persistencia
import utils
import sys

# Forzar UTF-8 en consola para evitar errores con emojis en Windows
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

RUTA_JSON = persistencia.RUTA_JSON
RUTA_LOG = persistencia.RUTA_LOG

def submenu_cambio_estado(lista_tareas):
    """Submenú para modificar el estado de una tarea."""
    print("\n--- SUBMENÚ: CAMBIAR ESTADO DE TAREA ---")
    print()
    print("  💡 Pulsa Tab para volver al menú principal")
    utils.mostrar_tabla_tareas(lista_tareas)
    
    id_tarea = utils.validar_entero_menu("Ingrese el ID de la tarea a modificar: ", 1, 999999)
    if id_tarea is None:
        return
    nuevo_estado = utils.validar_opcion_lista(
        "Ingrese el nuevo estado (pendiente, en_curso, finalizada): ",
        ["pendiente", "en_curso", "finalizada"]
    )
    if nuevo_estado is None:
        return
    
    exito = estructuras.cambiar_estado_tarea(lista_tareas, id_tarea, nuevo_estado)
    if exito:
        persistencia.guardar_datos_json(RUTA_JSON, lista_tareas)
        persistencia.registrar_log(RUTA_LOG, "CAMBIO_ESTADO", f"Tarea {id_tarea} paso a {nuevo_estado}")
        print(" ✅ Estado actualizado correctamente.")
    else:
        print(" ❌ No se encontró ninguna tarea con ese ID.")

def submenu_filtrar(lista_tareas):
    """Submenú para filtrar tareas."""
    print("\n--- FILTRAR TAREAS ---")
    print()
    print("  💡 Pulsa Tab para volver al menú principal")
    print("1. Por estado")
    print("2. Por categoría")
    print("3. Por responsable")
    print("0. Volver")
    
    opcion = utils.validar_entero_menu("Seleccione una opción: ", 0, 3)
    
    if opcion is None:
        return
    
    if opcion == 1:
        estado = utils.validar_opcion_lista(
            "Ingrese estado (pendiente, en_curso, finalizada): ",
            ["pendiente", "en_curso", "finalizada"]
        )
        if estado is None:
            return
        resultado = estructuras.filtrar_tareas(lista_tareas, estado=estado)
    elif opcion == 2:
        cat = utils._input_inmediato("Ingrese categoría (Tab para volver): ")
        if cat is None:
            return
        resultado = estructuras.filtrar_tareas(lista_tareas, categoria=cat)
    elif opcion == 3:
        resp = utils._input_inmediato("Ingrese responsable (Tab para volver): ")
        if resp is None:
            return
        resultado = estructuras.filtrar_tareas(lista_tareas, responsable=resp)
    else:
        return
    
    utils.mostrar_tabla_tareas(resultado)
    if not resultado:
        print("\n[ No se encontraron tareas con ese criterio. ]")

def submenu_actualizar_tarea(lista_tareas):
    """Submenú para actualizar una tarea existente."""
    print()
    print("  💡 Pulsa Tab para volver al menú principal")
    utils.mostrar_tabla_tareas(lista_tareas)
    
    id_tarea = utils.validar_entero_menu("Ingrese el ID de la tarea a actualizar: ", 1, 999999)
    
    if id_tarea is None:
        return
    
    tarea_encontrada = None
    for t in lista_tareas:
        if t["id"] == id_tarea:
            tarea_encontrada = t
            break
    
    if not tarea_encontrada:
        print(" ❌ No se encontró ninguna tarea con ese ID.")
        return
    
    print(f"\nTarea actual: {tarea_encontrada['titulo']}")
    print("\nDeje en blanco para no cambiar un campo.\n")
    
    nuevo_titulo = utils._input_inmediato(f"  Nuevo título [{tarea_encontrada['titulo']}] (Tab para volver): ")
    if nuevo_titulo is None:
        return
    nueva_desc = utils._input_inmediato(f"  Nueva descripción [{tarea_encontrada['descripcion']}] (Tab para volver): ")
    if nueva_desc is None:
        return
    nueva_prio = utils._input_inmediato(f"  Nueva prioridad (1-3) [{tarea_encontrada['prioridad']}] (Tab para volver): ")
    if nueva_prio is None:
        return
    nuevo_estado = utils._input_inmediato(f"  Nuevo estado (pendiente/en_curso/finalizada) [{tarea_encontrada['estado']}] (Tab para volver): ")
    if nuevo_estado is None:
        return
    nueva_cat = utils._input_inmediato(f"  Nueva categoría [{tarea_encontrada['categoria']}] (Tab para volver): ")
    if nueva_cat is None:
        return
    nuevo_resp = utils._input_inmediato(f"  Nuevo responsable [{tarea_encontrada['responsable']}] (Tab para volver): ")
    if nuevo_resp is None:
        return
    nueva_fecha = utils._input_inmediato(f"  Nueva fecha límite (DD/MM/YYYY) [{tarea_encontrada['fecha_limite']}] (Tab para volver): ")
    if nueva_fecha is None:
        return
    if nueva_fecha.strip():
        from datetime import datetime
        try:
            fecha = datetime.strptime(nueva_fecha.strip(), "%d/%m/%Y")
            if fecha.date() < datetime.now().date():
                print(" ⚠ La fecha no puede ser anterior a hoy, no se modificó.")
                nueva_fecha = ""
        except ValueError:
            print(" ⚠ Fecha inválida (use DD/MM/YYYY), no se modificó.")
            nueva_fecha = ""
    
    if nuevo_titulo:
        tarea_encontrada["titulo"] = nuevo_titulo
    if nueva_desc:
        tarea_encontrada["descripcion"] = nueva_desc
    if nueva_prio:
        try:
            prio = int(nueva_prio)
            if 1 <= prio <= 3:
                tarea_encontrada["prioridad"] = prio
            else:
                print(" ⚠ Prioridad inválida, no se modificó.")
        except ValueError:
            print(" ⚠ Prioridad inválida, no se modificó.")
    if nuevo_estado:
        if nuevo_estado in ["pendiente", "en_curso", "finalizada"]:
            tarea_encontrada["estado"] = nuevo_estado
        else:
            print(" ⚠ Estado inválido, no se modificó.")
    if nueva_cat:
        tarea_encontrada["categoria"] = nueva_cat
    if nuevo_resp:
        tarea_encontrada["responsable"] = nuevo_resp
    if nueva_fecha:
        tarea_encontrada["fecha_limite"] = nueva_fecha.strip()
    
    persistencia.guardar_datos_json(RUTA_JSON, lista_tareas)
    persistencia.registrar_log(RUTA_LOG, "ACTUALIZAR_TAREA", f"Tarea ID {id_tarea} actualizada")
    print(" ✅ Tarea actualizada correctamente.")

def menu_principal():
    """Función principal que despliega el menú en bucle."""
    tareas = persistencia.cargar_datos_json(RUTA_JSON)
    persistencia.registrar_log(RUTA_LOG, "INICIO_SESION", "El usuario inició el programa")
    
    
    while True:
        print("\n" + "=" * 45)
        print("    Gestor de Tareas - Lazarus")
        print("=" * 45)
        print("  1. Alta / Cargar nueva tarea")
        print("  2. Consultar y filtrar tareas")
        print("  3. Ver detalle de una tarea")
        print("  4. Modificar tarea")
        print("  5. Modificar estado de tarea")
        print("  6. Ver estadísticas de productividad")
        print("  7. Exportar reporte a archivo CSV")
        print("  0. Salir del programa")
        print()
        print("  💡 Pulsa Tab en cualquier momento para volver al menú principal")
        print("=" * 45)
        
        opcion = utils.validar_entero_menu("Seleccione una opción: ", 0, 7)
        
        if opcion is None:
            continue
        
        if opcion == 1:
            print("\n--- ALTA DE NUEVA TAREA ---")
            titulo = utils.validar_texto_no_vacio("Ingrese título de la tarea: ")
            if titulo is None:
                continue
            desc = utils.validar_texto_no_vacio("Ingrese descripción: ")
            if desc is None:
                continue
            prio = utils.validar_entero_menu("Ingrese prioridad (1: Alta, 2: Media, 3: Baja): ", 1, 3)
            
            if prio is None:
                continue
            
            cat = utils.validar_texto_no_vacio("Ingrese categoría (ej. Dev, Frontend, Backend): ")
            if cat is None:
                continue
            resp = utils.validar_texto_no_vacio("Ingrese responsable: ")
            if resp is None:
                continue
            limite = utils.validar_fecha("Ingrese fecha límite (DD/MM/YYYY): ")
            if limite is None or limite == "":
                continue
            
            nuevo_id = estructuras.obtener_siguiente_id(tareas)
            nueva_t = estructuras.crear_tarea(
                nuevo_id, titulo, desc, prio, "pendiente", cat, resp, limite
            )
            tareas.append(nueva_t)
            
            persistencia.guardar_datos_json(RUTA_JSON, tareas)
            persistencia.registrar_log(RUTA_LOG, "ALTA_TAREA", f"Tarea ID {nuevo_id} creada")
            print(f"\n ✅ Tarea ID {nuevo_id} agregada con éxito.")
            utils.mostrar_tarea_detalle(nueva_t)

        elif opcion == 2:
            print("\n--- CONSULTAR Y FILTRAR ---")
            print("1. Ver todas las tareas")
            print("2. Filtrar tareas")
            opcion_filtrar = utils.validar_entero_menu("Seleccione: ", 1, 2)
            
            if opcion_filtrar is None:
                continue
            
            if opcion_filtrar == 1:
                filtradas = estructuras.ordenar_tareas_por_prioridad(tareas)
                utils.mostrar_tabla_tareas(filtradas)
            elif opcion_filtrar == 2:
                submenu_filtrar(tareas)

        elif opcion == 3:
            if not tareas:
                print("\n[ No hay tareas para mostrar. ]")
                continue
            utils.mostrar_tabla_tareas(tareas)
            id_tarea = utils.validar_entero_menu("Ingrese el ID de la tarea a ver: ", 1, 999999)
            if id_tarea is None:
                continue
            tarea_encontrada = None
            for t in tareas:
                if t["id"] == id_tarea:
                    tarea_encontrada = t
                    break
            if tarea_encontrada:
                utils.mostrar_tarea_detalle(tarea_encontrada)
            else:
                print(" ❌ No se encontró ninguna tarea con ese ID.")

        elif opcion == 4:
            if not tareas:
                print("\n[ No hay tareas para modificar. ]")
                continue
            submenu_actualizar_tarea(tareas)

        elif opcion == 5:
            if not tareas:
                print("\n[ No hay tareas para modificar. ]")
                continue
            submenu_cambio_estado(tareas)

        elif opcion == 6:
            stats = estructuras.calcular_estadisticas_productividad(tareas)
            print("\n" + "=" * 40)
            print("  📊 ESTADÍSTICAS DE PRODUCTIVIDAD")
            print("=" * 40)
            print(f"  Total de tareas:      {stats['total_tareas']}")
            print(f"  Pendientes:           {stats['pendientes']}")
            print(f"  En Curso:             {stats['en_curso']}")
            print(f"  Finalizadas:          {stats['finalizadas']}")
            print(f"  Porcentaje completado: {stats['porcentaje_completadas']}%")
            print("=" * 40)

        elif opcion == 7:
            exito = persistencia.exportar_reporte_csv(persistencia.RUTA_CSV, tareas)
            if exito:
                persistencia.registrar_log(RUTA_LOG, "EXPORTAR_CSV", "Reporte generado")
                print(f"\n ✅ Reporte exportado a {persistencia.RUTA_CSV}")
            else:
                print(" ❌ Error al generar el reporte.")

        elif opcion == 0:
            persistencia.registrar_log(RUTA_LOG, "CIERRE_SESION", "El usuario cerró el programa")
            print("\n¡Gracias por utilizar el Gestor de Tareas! Hasta luego. 👋\n")
            break


if __name__ == "__main__":
    menu_principal()
