# main.py
# Punto de entrada de la aplicación de consola. Orquesta la interacción con el usuario.

import estructuras
import persistencia
import utils

def submenu_cambio_estado(lista_tareas):
    """Submenú para modificar el estado de una tarea."""
    print("\n--- SUBMENÚ: CAMBIAR ESTADO DE TAREA ---")
    id_tarea = utils.validar_entero_menu("Ingrese el ID de la tarea a modificar: ", 1, 999999)
    nuevo_estado = utils.validar_opcion_lista(
        "Ingrese el nuevo estado (pendiente, en_curso, finalizada): ",
        ["pendiente", "en_curso", "finalizada"]
    )
    
    exito = estructuras.cambiar_estado_tarea(lista_tareas, id_tarea, nuevo_estado)
    if exito:
        persistencia.guardar_datos_json(persistencia.RUTA_JSON, lista_tareas)
        persistencia.registrar_log(persistencia.RUTA_LOG, "CAMBIO_ESTADO", f"Tarea {id_tarea} paso a {nuevo_estado}")
        print(" Estado actualizado correctamente.")
    else:
        print(" No se encontró ninguna tarea con ese ID.")

def menu_principal():
    """Función principal que despliega el menú en bucle."""
    tareas = persistencia.cargar_datos_json()
    persistencia.registrar_log(persistencia.RUTA_LOG, "INICIO_SESION", "El usuario inició el programa")
    
    while True:
        print("\n" + "=" * 45)
        print("    GESTOR DE TAREAS - CLON TRELLO (Python)")
        print("=" * 45)
        print("1. Alta / Cargar nueva tarea")
        print("2. Consultar y filtrar tareas")
        print("3. Modificar estado de tarea (Submenú)")
        print("4. Ver estadísticas de productividad")
        print("5. Exportar reporte a archivo CSV")
        print("6. Iniciar servidor FastAPI (Eje C REST API)")
        print("0. Salir del programa")
        print("=" * 45)
        
        opcion = utils.validar_entero_menu("Seleccione una opción: ", 0, 6)
        
        if opcion == 1:
            titulo = utils.validar_texto_no_vacio("Ingrese título de la tarea: ")
            desc = utils.validar_texto_no_vacio("Ingrese descripción: ")
            prio = utils.validar_entero_menu("Ingrese prioridad (1: Alta, 2: Media, 3: Baja): ", 1, 3)
            cat = utils.validar_texto_no_vacio("Ingrese categoría (ej. Dev, Frontend, Backend): ")
            resp = utils.validar_texto_no_vacio("Ingrese responsable: ")
            limite = utils.validar_texto_no_vacio("Ingrese fecha límite (AAAA-MM-DD): ")
            
            nuevo_id = estructuras.obtener_siguiente_id(tareas)
            nueva_t = estructuras.crear_tarea(nuevo_id, titulo, desc, prio, "pendiente", cat, resp, limite)
            tareas.append(nueva_t)
            
            persistencia.guardar_datos_json(persistencia.RUTA_JSON, tareas)
            persistencia.registrar_log(persistencia.RUTA_LOG, "ALTA_TAREA", f"Tarea ID {nuevo_id} creada")
            print(" Tarea agregada con éxito.")

        elif opcion == 2:
            print("\n--- ORDENAR Y FILTRAR ---")
            filtradas = estructuras.ordenar_tareas_por_prioridad(tareas)
            utils.mostrar_tabla_tareas(filtradas)

        elif opcion == 3:
            submenu_cambio_estado(tareas)

        elif opcion == 4:
            stats = estructuras.calcular_estadisticas_productividad(tareas)
            print("\n--- ESTADÍSTICAS DE PRODUCTIVIDAD ---")
            print(f"Total de tareas: {stats['total_tareas']}")
            print(f"Pendientes: {stats['pendientes']}")
            print(f"En Curso: {stats['en_curso']}")
            print(f"Finalizadas: {stats['finalizadas']}")
            print(f"Porcentaje de completado: {stats['porcentaje_completadas']}%")

        elif opcion == 5:
            exito = persistencia.exportar_reporte_csv(persistencia.RUTA_CSV, tareas)
            if exito:
                persistencia.registrar_log(persistencia.RUTA_LOG, "EXPORTAR_CSV", "Reporte generado")
                print(f" Reporte exportado a {persistencia.RUTA_CSV}")

        elif opcion == 6:
            print("\nIniciando FastAPI... Para salir del servidor presione Ctrl + C")
            import uvicorn
            uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)

        elif opcion == 0:
            persistencia.registrar_log(persistencia.RUTA_LOG, "CIERRE_SESION", "El usuario cerró el programa")
            print("\n¡Gracias por utilizar el Gestor de Tareas! Hasta luego.\n")
            break

if __name__ == "__main__":
    menu_principal()