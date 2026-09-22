# utils.py
# Módulo de validación de entradas por teclado y formateo de pantalla

import sys


def _input_inmediato(mensaje):
    """
    Muestra el mensaje y lee una línea de entrada sin necesidad de Enter
    para detectar Tab inmediatamente.
    Retorna None si se pulsa Tab o Enter vacío, o el string ingresado.
    """
    try:
        import tty
        import termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            sys.stdout.write(mensaje)
            sys.stdout.flush()
            ch = sys.stdin.read(1)
            # Si Tab o Enter → volver al menú
            if ch == '\t' or ch in ('\r', '\n'):
                sys.stdout.write('\n')
                sys.stdout.flush()
                return None
            # Eco del primer carácter
            sys.stdout.write(ch)
            sys.stdout.flush()
        finally:
            # Restaurar terminal ANTES de llamar a input()
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        # Terminal restaurado, leer el resto de la línea normalmente
        resto = input()
        return ch + resto
    except (ImportError, AttributeError, termios.error):
        # Fallback en sistemas que no soportan termios (Windows, etc.)
        entrada = input(mensaje)
        if entrada.strip() == "" or "\t" in entrada:
            return None
        return entrada


def validar_entero_menu(mensaje, min_val, max_val):
    """
    Solicita un entero por consola dentro de un rango determinado.
    Retorna None si el usuario presiona Enter vacío o pulsa Tab (cancelar / volver).
    """
    while True:
        try:
            entrada = _input_inmediato(mensaje)
            if entrada is None or entrada.strip() == "":
                return None
            opcion = int(entrada)
            if min_val <= opcion <= max_val:
                return opcion
            print(f" Error: Ingrese un número entre {min_val} y {max_val}.")
        except ValueError:
            print(" Error: Debe ingresar un valor numérico entero.")


def validar_texto_no_vacio(mensaje):
    """
    Solicita un texto y valida que no se ingrese una cadena vacía.
    Retorna None si el usuario pulsa Tab o Enter vacío (cancelar / volver).
    """
    while True:
        texto = _input_inmediato(mensaje)
        if texto is None or texto.strip() == "":
            return None
        if len(texto.strip()) > 0:
            return texto.strip()
        print(" Error: El campo no puede estar vacío.")


def validar_opcion_lista(mensaje, opciones_validas):
    """
    Valida que la opción ingresada pertenezca a una lista dada.
    Retorna None si el usuario presiona Enter vacío o pulsa Tab (cancelar / volver).
    """
    while True:
        valor = _input_inmediato(mensaje)
        if valor is None or valor.strip() == "":
            return None
        valor = valor.strip().lower()
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
