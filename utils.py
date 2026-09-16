# utils.py
# Módulo de validación de entradas por teclado y formateo de pantalla

def validar_entero_menu(mensaje, min_val, max_val):
    """
    Solicita un entero por consola dentro de un rango determinado.
    """
    while True:
        try:
            opcion = int(input(mensaje))
            if min_val <= opcion <= max_val:
                return opcion
            print(f" Error: Ingrese un número entre {min_val} y {max_val}.")
        except ValueError:
            print(" Error: Debe ingresar un valor numérico entero.")

def validar_texto_no_vacio(mensaje):
    """
    Solicita un texto y valida que no se ingrese una cadena vacía.
    """
    while True:
        texto = input(mensaje).strip()
        if len(texto) > 0:
            return texto
        print(" Error: El campo no puede estar vacío.")

def validar_opcion_lista(mensaje, opciones_validas):
    """
    Valida que la opción ingresada pertenezca a una lista dada.
    """
    while True:
        valor = input(mensaje).strip().lower()
        if valor in opciones_validas:
            return valor
        print(f" Error: Opción inválida. Opciones válidas: {', '.join(opciones_validas)}")

def mostrar_tabla_tareas(lista_tareas):
    """
    Imprime un listado formateado de tareas en la terminal.
    """
    if not lista_tareas:
        print("\n[ No hay tareas para mostrar. ]\n")
        return
    
    print("-" * 80)
    print(f"{'ID':<4} | {'Título':<20} | {'Estado':<12} | {'Prio':<5} | {'Responsable':<15}")
    print("-" * 80)
    for t in lista_tareas:
        print(f"{t['id']:<4} | {t['titulo'][:18]:<20} | {t['estado']:<12} | {t['prioridad']:<5} | {t['responsable'][:13]:<15}")
    print("-" * 80)

def mostrar_tarea_detalle(tarea):
    """
    Imprime los detalles completos de una tarea.
    """
    print(f"\n{'─' * 50}")
    print(f"  ID:          {tarea['id']}")
    print(f"  Título:      {tarea['titulo']}")
    print(f"  Descripción: {tarea['descripcion']}")
    print(f"  Prioridad:   {tarea['prioridad']} {'(Alta)' if tarea['prioridad']==1 else '(Media)' if tarea['prioridad']==2 else '(Baja)'}")
    print(f"  Estado:      {tarea['estado']}")
    print(f"  Categoría:   {tarea['categoria']}")
    print(f"  Responsable: {tarea['responsable']}")
    print(f"  Fecha Límite:{tarea['fecha_limite']}")
    print(f"{'─' * 50}\n")
