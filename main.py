# main.py
# Punto de entrada de la aplicación de consola. Gestor de Tareas / Trello Clon
# Versión Vanilla Python — Sin FastAPI ni frameworks web

import estructuras
import persistencia
import utils

RUTA_JSON = persistencia.RUTA_JSON
RUTA_LOG = persistencia.RUTA_LOG

def submenu_cambio_estado(lista_tareas):
    """Submenú para modificar el estado de una tarea."""
    print("\n--- SUBMENÚ: CAMBIAR ESTADO DE TAREA ---")
    utils.mostrar_tabla_tareas(lista_tareas)
    
    id_tarea = utils.validar_entero_menu("Ingrese el ID de la tarea a modificar: ", 1, 999999)
    nuevo_estado = utils.validar_opcion_lista(
        "Ingrese el nuevo estado (pendiente, en_curso, finalizada): ",
        ["pendiente", "en_curso", "finalizada"]
    )
    
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
    print("1. Por estado")
    print("2. Por categoría")
    print("3. Por responsable")
    print("0. Volver")
    
    opcion = utils.validar_entero_menu("Seleccione una opción: ", 0, 3)
    
    if opcion == 1:
        estado = utils.validar_opcion_lista(
            "Ingrese estado (pendiente, en_curso, finalizada): ",
            ["pendiente", "en_curso", "finalizada"]
        )
        resultado = estructuras.filtrar_tareas(lista_tareas, estado=estado)
    elif opcion == 2:
        cat = input("Ingrese categoría: ").strip()
        resultado = estructuras.filtrar_tareas(lista_tareas, categoria=cat)
    elif opcion == 3:
        resp = input("Ingrese responsable: ").strip()
        resultado = estructuras.filtrar_tareas(lista_tareas, responsable=resp)
    else:
        return
    
    utils.mostrar_tabla_tareas(resultado)
    if not resultado:
        print("\n[ No se encontraron tareas con ese criterio. ]")

def submenu_actualizar_tarea(lista_tareas):
    """Submenú para actualizar una tarea existente."""
    utils.mostrar_tabla_tareas(lista_tareas)
    
    id_tarea = utils.validar_entero_menu("Ingrese el ID de la tarea a actualizar: ", 1, 999999)
    
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
    
    nuevo_titulo = input(f"  Nuevo título [{tarea_encontrada['titulo']}]: ").strip()
    nueva_desc = input(f"  Nueva descripción [{tarea_encontrada['descripcion']}]: ").strip()
    nueva_prio = input(f"  Nueva prioridad (1-3) [{tarea_encontrada['prioridad']}]: ").strip()
    nuevo_estado = input(f"  Nuevo estado (pendiente/en_curso/finalizada) [{tarea_encontrada['estado']}]: ").strip()
    nueva_cat = input(f"  Nueva categoría [{tarea_encontrada['categoria']}]: ").strip()
    nuevo_resp = input(f"  Nuevo responsable [{tarea_encontrada['responsable']}]: ").strip()
    nueva_fecha = input(f"  Nueva fecha límite (AAAA-MM-DD) [{tarea_encontrada['fecha_limite']}]: ").strip()
    
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
        tarea_encontrada["fecha_limite"] = nueva_fecha
    
    persistencia.guardar_datos_json(RUTA_JSON, lista_tareas)
    persistencia.registrar_log(RUTA_LOG, "ACTUALIZAR_TAREA", f"Tarea ID {id_tarea} actualizada")
    print(" ✅ Tarea actualizada correctamente.")

def menu_principal():
    """Función principal que despliega el menú en bucle."""
    tareas = persistencia.cargar_datos_json(RUTA_JSON)
    persistencia.registrar_log(RUTA_LOG, "INICIO_SESION", "El usuario inició el programa")
    
    print("\n" + "=" * 45)
    print("    📋 GESTOR DE TAREAS - CLON TRELLO")
    print("    ⚡ Versión Python Vanilla")
    print("=" * 45)
    
    while True:
        print("\n" + "=" * 45)
        print("    GESTOR DE TAREAS - CLON TRELLO")
        print("=" * 45)
        print("  1. Alta / Cargar nueva tarea")
        print("  2. Consultar y filtrar tareas")
        print("  3. Ver detalle de una tarea")
        print("  4. Modificar tarea")
        print("  5. Modificar estado de tarea")
        print("  6. Ver estadísticas de productividad")
        print("  7. Exportar reporte a archivo CSV")
        print("  0. Salir del programa")
        print("=" * 45)
        
        opcion = utils.validar_entero_menu("Seleccione una opción: ", 0, 7)
        
        if opcion == 1:
            print("\n--- ALTA DE NUEVA TAREA ---")
            titulo = utils.validar_texto_no_vacio("Ingrese título de la tarea: ")
            desc = utils.validar_texto_no_vacio("Ingrese descripción: ")
            prio = utils.validar_entero_menu("Ingrese prioridad (1: Alta, 2: Media, 3: Baja): ", 1, 3)
            cat = utils.validar_texto_no_vacio("Ingrese categoría (ej. Dev, Frontend, Backend): ")
            resp = utils.validar_texto_no_vacio("Ingrese responsable: ")
            limite = utils.validar_texto_no_vacio("Ingrese fecha límite (AAAA-MM-DD): ")
            
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
