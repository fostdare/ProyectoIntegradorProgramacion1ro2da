#!/usr/bin/env python3
"""
Generador del documento de desglose del proyecto.
Uso: python3 generar_informe.py
"""

from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

DOC = Document()

# --- Configuración de estilos base ---
normal = DOC.styles["Normal"]
normal.font.name = "Calibri"
normal.font.size = Pt(11)

# Título principal
titulo = DOC.add_heading("Gestor de Tareas — Clon Trello", level=0)
titulo.alignment = WD_ALIGN_PARAGRAPH.CENTER

sub = DOC.add_paragraph("Desglose del código y elementos utilizados")
sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
sub.runs[0].italic = True
sub.runs[0].font.size = Pt(13)

DOC.add_paragraph()

# --- 1. Resumen del proyecto ---
DOC.add_heading("1. Resumen del proyecto", level=1)

DOC.add_paragraph(
    "Aplicación de consola para la gestión de tareas al estilo Trello. "
    "Está escrita en Python vanilla (sin frameworks web) y funciona 100% por terminal. "
    "Permite dar de alta tareas, consultarlas, filtrarlas, modificarlas, cambiar su estado, "
    "ver estadísticas de productividad y exportar un reporte a CSV."
)

DOC.add_paragraph(
    "Los datos se persisten en archivos locales: las tareas en formato JSON "
    "y la bitácora de operaciones en un archivo de texto plano."
)

DOC.add_heading("1.1 Estructura de archivos", level=2)

tabla_estructura = DOC.add_table(rows=1, cols=3)
tabla_estructura.style = "Light Grid Accent 1"
tabla_estructura.alignment = WD_TABLE_ALIGNMENT.CENTER

encabezados = ["Archivo", "Responsabilidad", "Líneas"]
for i, texto in enumerate(encabezados):
    celda = tabla_estructura.rows[0].cells[i]
    celda.text = texto
    for run in celda.paragraphs[0].runs:
        run.bold = True

filas = [
    ("main.py", "Punto de entrada. Menú principal en bucle y submenús de cada operación.", "288"),
    ("estructuras.py", "Modelo de datos y lógica de dominio (tareas, filtros, orden, estadísticas).", "90"),
    ("persistencia.py", "Lectura y escritura de archivos: JSON, CSV y log TXT.", "70"),
    ("utils.py", "Validación de entradas por teclado y formateo de tablas en pantalla.", "121"),
    ("tareas.json", "Archivo de datos donde se persisten las tareas.", "—"),
    ("log_actividad.txt", "Bitácora de acciones del usuario con fecha y hora.", "—"),
    ("reporte_tareas.csv", "Salida generada al exportar el reporte (se crea al usar la opción 7).", "—"),
    ("README.md", "Documentación del proyecto: ejecución, características y estructura.", "—"),
]

for archivo, resp, lineas in filas:
    celdas = tabla_estructura.add_row().cells
    celdas[0].text = archivo
    celdas[1].text = resp
    celdas[2].text = lineas

# --- 2. Elementos del lenguaje ---
DOC.add_heading("2. Elementos del lenguaje Python utilizados", level=1)

DOC.add_paragraph(
    "El proyecto hace uso de las siguientes construcciones del lenguaje, "
    "sin recurrir a librerías externas."
)

DOC.add_heading("2.1 Estructuras de control", level=2)

tabla_control = DOC.add_table(rows=1, cols=2)
tabla_control.style = "Light Grid Accent 1"
tabla_control.alignment = WD_TABLE_ALIGNMENT.CENTER

for i, texto in enumerate(["Elemento", "Dónde se usa"]):
    celda = tabla_control.rows[0].cells[i]
    celda.text = texto
    for run in celda.paragraphs[0].runs:
        run.bold = True

control_filas = [
    ("if / elif / else", "Menú principal (siete opciones) y validación de entradas."),
    ("while True", "Bucle infinito del menú principal y reintentos de validación."),
    ("for", "Recorrido de la lista de tareas al buscar, filtrar y ordenar."),
    ("try / except", "Captura de ValueError al convertir texto a entero, y de errores de archivo."),
    ("continue", "Regresa al menú principal cuando el usuario cancela o no hay tareas."),
    ("break", "Cierra el programa al elegir la opción 0."),
    ("return", "Aborta un submenú cuando el usuario pulsa Tab para volver."),
]

for elemento, uso in control_filas:
    celdas = tabla_control.add_row().cells
    celdas[0].text = elemento
    celdas[1].text = uso

DOC.add_heading("2.2 Funciones y métodos", level=2)

DOC.add_paragraph(
    "Se defining funciones con palabra reservada def, documentadas con docstrings de tres comillas "
    "y con parámetros posicionales y valores por defecto."
)

DOC.add_paragraph("Ejemplo de una función del módulo utils.py:", style="Intense Quote")
ejemplo = DOC.add_paragraph()
run = ejemplo.add_run(
    "def validar_entero_menu(mensaje, min_val, max_val):\n"
    "    \"\"\"\n"
    "    Solicita un entero por consola dentro de un rango determinado.\n"
    "    Retorna None si el usuario pulsa Tab (cancelar / volver).\n"
    "    \"\"\""
)
run.font.name = "Consolas"
run.font.size = Pt(9)

DOC.add_heading("2.3 Módulos de la biblioteca estándar", level=2)

tabla_std = DOC.add_table(rows=1, cols=3)
tabla_std.style = "Light Grid Accent 1"
tabla_std.alignment = WD_TABLE_ALIGNMENT.CENTER

for i, texto in enumerate(["Módulo", "Método", "Función en el proyecto"]):
    celda = tabla_std.rows[0].cells[i]
    celda.text = texto
    for run in celda.paragraphs[0].runs:
        run.bold = True

std_filas = [
    ("json", "json.load / json.dump", "Cargar y guardar tareas en tareas.json."),
    ("csv", "csv.DictWriter", "Exportar el reporte con encabezados fijos."),
    ("os", "os.path / os.path.exists", "Construir rutas absolutas y verificar existencia."),
    ("datetime", "datetime.now", "Sellar la bitácora con fecha y hora."),
    ("sys", "sys.stdin / sys.stdout", "Leer y escribir directamente del terminal."),
    ("termios", "tcgetattr / tcsetattr", "Guardar y restaurar el estado del terminal."),
    ("tty", "tty.setraw", "Activar el modo lectura inmediata de teclas."),
]

for modulo, metodo, uso in std_filas:
    celdas = tabla_std.add_row().cells
    celdas[0].text = modulo
    celdas[1].text = metodo
    celdas[2].text = uso

DOC.add_paragraph(
    "Nota: termios y tty son módulos disponibles en sistemas Unix (Linux y macOS). "
    "En Windows el programa cae automáticamente en el método alternativo con input()."
)
DOC.paragraphs[-1].runs[0].italic = True

# --- 3. Desglose por módulo ---
DOC.add_heading("3. Desglose de cada módulo", level=1)

DOC.add_heading("3.1 main.py — Interfaz y flujo de menús", level=2)

DOC.add_paragraph(
    "Es el punto de entrada de la aplicación. Contiene tres submenús y la función "
    "menu_principal, que mantiene el bucle de navegación."
)

DOC.add_paragraph("Funciones definidas:")
for texto in [
    "submenu_cambio_estado(lista_tareas) — Muestra la tabla y permite cambiar el estado de una tarea.",
    "submenu_filtrar(lista_tareas) — Filtra por estado, categoría o responsable.",
    "submenu_actualizar_tarea(lista_tareas) — Modifica cualquier campo de una tarea existente.",
    "menu_principal() — Carga los datos, dibuja el menú y atiende las opciones 0 a 7.",
]:
    DOC.add_paragraph(texto, style="List Bullet")

DOC.add_paragraph("Opciones del menú principal:")
tabla_menu = DOC.add_table(rows=1, cols=2)
tabla_menu.style = "Light Grid Accent 1"
tabla_menu.alignment = WD_TABLE_ALIGNMENT.CENTER

for i, texto in enumerate(["Opción", "Acción"]):
    celda = tabla_menu.rows[0].cells[i]
    celda.text = texto
    for run in celda.paragraphs[0].runs:
        run.bold = True

menu_filas = [
    ("1", "Alta / Cargar nueva tarea."),
    ("2", "Consultar y filtrar tareas."),
    ("3", "Ver detalle de una tarea."),
    ("4", "Modificar tarea."),
    ("5", "Modificar estado de tarea."),
    ("6", "Ver estadísticas de productividad."),
    ("7", "Exportar reporte a archivo CSV."),
    ("0", "Salir del programa."),
]

for opcion, accion in menu_filas:
    celdas = tabla_menu.add_row().cells
    celdas[0].text = opcion
    celdas[1].text = accion

DOC.add_heading("3.2 estructuras.py — Lógica de dominio", level=2)

DOC.add_paragraph(
    "Trabaja sobre la tarea como un diccionario de ocho claves: id, titulo, descripcion, "
    "prioridad, estado, categoria, responsable y fecha_limite. No depende de ningun otro modulo."
)

DOC.add_paragraph("Funciones definidas:")
for texto in [
    "crear_tarea(...) — Construye y retorna el diccionario de una tarea.",
    "obtener_siguiente_id(lista_tareas) — Calcula el siguiente ID disponible.",
    "filtrar_tareas(lista_tareas, estado, categoria, responsable) — Filtra por criterios (None = sin filtro).",
    "ordenar_tareas_por_prioridad(lista_tareas) — Ordena por prioridad con algoritmo de burbuja.",
    "cambiar_estado_tarea(lista_tareas, id_tarea, nuevo_estado) — Modifica el estado; retorna True o False.",
    "calcular_estadisticas_productividad(lista_tareas) — Calcula totales y porcentaje completado.",
]:
    DOC.add_paragraph(texto, style="List Bullet")

DOC.add_paragraph("Valores de estado permitidos: pendiente, en_curso, finalizada.")
DOC.add_paragraph("Escala de prioridad: 1 Alta, 2 Media, 3 Baja.")

DOC.add_heading("3.3 persistencia.py — Manejo de archivos", level=2)

DOC.add_paragraph(
    "Define las rutas absolutas de los archivos usando os.path.dirname sobre __file__, "
    "de modo que el programa funciona sin importar el directorio actual."
)

DOC.add_paragraph("Constantes de ruta:")
tabla_rutas = DOC.add_table(rows=1, cols=2)
tabla_rutas.style = "Light Grid Accent 1"
tabla_rutas.alignment = WD_TABLE_ALIGNMENT.CENTER

for i, texto in enumerate(["Constante", "Archivo"]):
    celda = tabla_rutas.rows[0].cells[i]
    celda.text = texto
    for run in celda.paragraphs[0].runs:
        run.bold = True

rutas_filas = [
    ("RUTA_JSON", "tareas.json"),
    ("RUTA_CSV", "reporte_tareas.csv"),
    ("RUTA_LOG", "log_actividad.txt"),
]

for constante, archivo in rutas_filas:
    celdas = tabla_rutas.add_row().cells
    celdas[0].text = constante
    celdas[1].text = archivo

DOC.add_paragraph("Funciones definidas:")
for texto in [
    "cargar_datos_json(ruta) — Lee tareas.json; si no existe, genera el archivo vacío.",
    "guardar_datos_json(ruta, datos) — Escribe la lista con indentación de 4 espacios.",
    "exportar_reporte_csv(ruta, lista) — Exporta las tareas usando csv.DictWriter.",
    "registrar_log(ruta, accion, detalle) — Añade una línea con timestamp al log.",
]:
    DOC.add_paragraph(texto, style="List Bullet")

for texto in [
    "cargar_datos_json(ruta) — Lee tareas.json; si no existe, genera el archivo vacío.",
    "guardar_datos_json(ruta, datos) — Escribe la lista con indentación de 4 espacios.",
    "exportar_reporte_csv(ruta, lista) — Exporta las tareas usando csv.DictWriter.",
    "registrar_log(ruta, accion, detalle) — Añade una línea con timestamp al log.",
]:
    DOC.add_paragraph(texto, style="List Bullet")

DOC.add_paragraph("Todas usan la sentencia with para garantizar el cierre del archivo.")

DOC.add_heading("3.4 utils.py — Validación y presentación", level=2)

DOC.add_paragraph("Funciones de validación de entrada:")
for texto in [
    "_input_inmediato(mensaje) — Lee del terminal detectando Tab sin exigir Enter.",
    "validar_entero_menu(mensaje, min_val, max_val) — Entero dentro de un rango.",
    "validar_texto_no_vacio(mensaje) — Texto que no puede quedar en blanco.",
    "validar_opcion_lista(mensaje, opciones_validas) — Texto perteneciente a una lista.",
]:
    DOC.add_paragraph(texto, style="List Bullet")

DOC.add_paragraph("Funciones de presentación:")
for texto in [
    "mostrar_tabla_tareas(lista_tareas) — Tabla formateada con columnas ID, Título, Estado, Prio y Responsable.",
    "mostrar_tarea_detalle(tarea) — Ficha completa de una tarea con separadores.",
]:
    DOC.add_paragraph(texto, style="List Bullet")

DOC.add_heading("3.4.1 La tecla Tab para volver al menú", level=3)

DOC.add_paragraph(
    "La función _input_inmediato resuelve un problema concreto: input() siempre espera a que "
    "el usuario pulse Enter, de modo que una tecla de cancellation solo se detectaría después "
    "de confirmar."
)

DOC.add_paragraph("El procedimiento es el siguiente:")
for i, texto in enumerate([
    "Se guardan los atributos actuales del terminal con termios.tcgetattr.",
    "Se activa el modo de lectura inmediata con tty.setraw.",
    "Se lee un único carácter con sys.stdin.read(1).",
    "Si el carácter es Tab o Enter, se restaura el terminal y se retorna None.",
    "Si es cualquier otro, se muestra en pantalla y el resto de la línea se lee con input().",
    "En cualquier caso, el finally restaura el terminal con termios.tcsetattr.",
], start=1):
    DOC.add_paragraph(f"{i}. {texto}", style="List Number")

DOC.add_paragraph(
    "Cuando una función de validación retorna None, el submenú hace return y el bucle de "
    "menu_principal vuelve a dibujar el menú. Si ocurre dentro del menú principal, se usa continue. "
    "El valor None es por tanto la señal interna de «volver al menú principal»."
)

# --- 4. Persistencia de datos ---
DOC.add_heading("4. Persistencia de datos", level=1)

DOC.add_paragraph(
    "Los datos sobreviven al cierre porque se releen desde el disco en cada arranque. "
    "menu_principal carga tareas.json una sola vez y mantiene la lista en memoria; "
    "cada operación que la modifica la guarda de nuevo."
)

DOC.add_paragraph(
    "El log de actividad funciona como una bitácora de auditoría: registra altas, "
    "cambios de estado, modificaciones y exportaciones, además de la apertura y el cierre de sesión."
)

# --- 5. Ejecución ---
DOC.add_heading("5. Ejecución", level=1)

DOC.add_paragraph("Desde la carpeta del proyecto:")
ejecucion = DOC.add_paragraph()
run = ejecucion.add_run("python main.py")
run.font.name = "Consolas"
run.font.size = Pt(11)
run.bold = True

DOC.add_paragraph("Requisitos: Python 3.10 o superior. No requiere instalar dependencias.")

# --- 6. Mapa de dependencias ---
DOC.add_heading("6. Mapa de dependencias entre módulos", level=1)

DOC.add_paragraph("El proyecto separa la lógica de la interfaz siguiendo un patrón simple:")
for texto in [
    "main.py importa estructuras, persistencia y utils.",
    "estructuras.py no importa nada: es lógica pura y podría probarse de forma aislada.",
    "persistencia.py importa json, csv, os y datetime de la biblioteca estándar.",
    "utils.py importa sys, y termios y tty solo en el caso de la lectura inmediata.",
]:
    DOC.add_paragraph(texto, style="List Bullet")

DOC.add_paragraph(
    "main.py nunca accede directamente a los archivos: toda la entrada y salida pasa por persistencia."
)

# --- Guardar ---
DOC.save("Desglose_del_Codigo_Gestor_de_Tareas.docx")
print("Documento generado: Desglose_del_Codigo_Gestor_de_Tareas.docx")