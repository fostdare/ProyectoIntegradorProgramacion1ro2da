#!/usr/bin/env python3
"""
Generador del documento de desglose del proyecto.
Uso: python3 generar_informe.py
"""

from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

import os

DOC = Document()

# Carpeta donde visualizacion.py guarda los PNG. El informe los inserta como
# imágenes para que el eje de investigación se vea documentado, no soloImplementado.
DIR_GRAFICOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "graficos")

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
    ("main.py", "Punto de entrada. Menú principal en bucle y submenús de cada operación.", "349"),
    ("estructuras.py", "Modelo de datos y lógica de dominio (tareas, filtros, orden, estadísticas).", "100"),
    ("persistencia.py", "Lectura y escritura de archivos: JSON, CSV y log TXT.", "70"),
    ("utils.py", "Validación de entradas por teclado y formateo de tablas en pantalla.", "146"),
    ("visualizacion.py", "Eje de investigación 3.8: gráficos de estadísticas en PNG con matplotlib.", "221"),
    ("test_proyecto.py", "Suite de pruebas automáticas con unittest.", "387"),
    ("generar_informe.py", "Genera este documento a partir del código del proyecto.", "—"),
    ("tareas.json", "Archivo de datos donde se persisten las tareas.", "—"),
    ("log_actividad.txt", "Bitácora de acciones del usuario con fecha y hora.", "—"),
    ("reporte_tareas.csv", "Salida generada al exportar el reporte (se crea al usar la opción 7).", "—"),
    ("graficos/", "Imágenes PNG generadas al usar la opción 9.", "—"),
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
    "submenu_eliminar_tarea(lista_tareas) — Pide confirmación y elimina la tarea por su ID.",
    "submenu_filtrar(lista_tareas) — Filtra por estado, categoría o responsable.",
    "submenu_actualizar_tarea(lista_tareas) — Modifica cualquier campo de una tarea existente.",
    "menu_principal() — Carga los datos, dibuja el menú y atiende las opciones 0 a 9.",
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
    ("8", "Eliminar tarea."),
    ("9", "Generar gráficos de las estadísticas en PNG."),
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

DOC.add_paragraph("Requisitos: Python 3.10 o superior.")

DOC.add_paragraph(
    "Dependencias externas: la aplicación requiere matplotlib para la opción 9 "
    "(gráficos). El resto del proyecto funciona solo con la biblioteca estándar."
)

dependencias = DOC.add_paragraph()
run = dependencias.add_run("pip install matplotlib")
run.font.name = "Consolas"
run.font.size = Pt(10)
run.bold = True

# --- 6. Mapa de dependencias ---
DOC.add_heading("6. Mapa de dependencias entre módulos", level=1)

DOC.add_paragraph("El proyecto separa la lógica de la interfaz siguiendo un patrón simple:")
for texto in [
    "main.py importa estructuras, persistencia, utils y visualizacion.",
    "estructuras.py no importa nada del proyecto: es lógica pura y se prueba de forma aislada.",
    "persistencia.py importa json, csv, os y datetime de la biblioteca estándar.",
    "utils.py importa sys, y termios y tty solo en el caso de la lectura inmediata.",
    "visualizacion.py importa estructuras (para obtener las estadísticas) y matplotlib.",
    "test_proyecto.py importa los cuatro módulos anteriores y los prueba con unittest.",
]:
    DOC.add_paragraph(texto, style="List Bullet")

DOC.add_paragraph(
    "main.py nunca accede directamente a los archivos: toda la entrada y salida pasa por persistencia."
)

# --- 7. Eje de investigación ---
DOC.add_heading("7. Eje de investigación: visualización de datos", level=1)

DOC.add_paragraph(
    "Para este eje se eligió la opción D: visualización de datos con matplotlib."
)

DOC.add_heading("7.1 ¿Qué es?", level=2)

DOC.add_paragraph(
    "La visualización de datos es la representación gráfica de información numérica o "
    "estructurada, con el fin de hacerla comprensible a simple vista. "
    "matplotlib es una biblioteca de Python para generar figuras estáticas: en lugar de "
    "escribir los datos a mano en un archivo de imagen, se entrega cada dato a la biblioteca "
    "y ella se encarga de dibujar, escalar los ejes, rotular, colorear y exportar."
)

DOC.add_paragraph(
    "Sus dos elementos centrales son Figure, que representa la figura completa, y Axes, que "
    "representa un único panel de dibujo con sus propios ejes. Toda figura se construye con "
    "estos objetos: se crean los paneles, se agregan los datos con funciones de dibujo como "
    "pie, barh o bar_label, se personalizan los títulos y finalmente se guarda la figura en "
    "un archivo."
)

DOC.add_paragraph(
    "El formato de exportación utilizado en el proyecto es PNG, un formato de imagen de "
    "mapa de bits que comprime sin pérdida: el color de cada píxel se guarda tal cual, sin "
    "aplicar el algoritmo de compresión con pérdida de los formatos JPEG. Por eso un gráfico "
    "de datos, donde los colores distinguen categorías y deben ser exactos, se guarda en PNG "
    "y no en JPEG."
)

DOC.add_heading("7.2 ¿Para qué sirve?", level=2)

DOC.add_paragraph(
    "Sirve para reemplazar tablas de números por imágenes que el cerebro procesa más rápido. "
    "Un porcentaje como 16,67 % es un dato abstracto que exige un cálculo mental; un círculo "
    "con ese porcentaje ocupa una fracción de sector y se interpreta de inmediato."
)

DOC.add_paragraph(
    "En el contexto del proyecto, la visualización cumple tres funciones concretas:")
for texto in [
    "Detectar la carga desbalanceada del equipo: el gráfico de barras por responsable hace "
    "evidente que una persona tiene muchas más tareas que las demás.",
    "Comunicar el avance del proyecto a alguien que no usa el sistema, como la profesora o "
    "quien esté a cargo del equipo.",
    "Elegir el tipo de gráfico adecuado según la pregunta que se responde.",
]:
    DOC.add_paragraph(texto, style="List Bullet")

DOC.add_heading("7.2.1 Tipos de gráfico y cuándo usar cada uno", level=3)

DOC.add_paragraph(
    "La elección del tipo de gráfico no es arbitraria: depende de qué relación entre los datos "
    "se quiera mostrar. En el proyecto se usaron tres tipos, cada uno justificado por los datos "
    "que debía representar."
)

tabla_grafos = DOC.add_table(rows=1, cols=3)
tabla_grafos.style = "Light Grid Accent 1"
tabla_grafos.alignment = WD_TABLE_ALIGNMENT.CENTER

for i, texto in enumerate(["Tipo de gráfico", "Qué relación muestra", "Uso en el proyecto"]):
    celda = tabla_grafos.rows[0].cells[i]
    celda.text = texto
    for run in celda.paragraphs[0].runs:
        run.bold = True

tipos_grafo = [
    (
        "Gráfico circular (anillo)",
        "Proporción de un total: cómo se reparte una cantidad entre categorías que suman el 100 %.",
        "Distribución de tareas por estado. Se elige porque los tres estados (pendiente, "
        "en curso, finalizada) son partes de un mismo total.",
    ),
    (
        "Gráfico de barras horizontales",
        "Comparación de magnitudes entre categorías. Funciona mejor que el vertical cuando "
        "las etiquetas son largas.",
        "Avance del trabajo y carga por responsable. Se eligió horizontal porque los nombres "
        "de los responsables son palabras y se leen mejor de lado.",
    ),
    (
        "Barra de progreso",
        "Un único valor dentro de un rango acotado, donde importa la distancia al máximo.",
        "Porcentaje completado. Se eligió porque el rango va de 0 a 100 % y el dato relevante "
        "es cuánto falta para el final.",
    ),
]

for tipo_grafo, relacion, uso in tipos_grafo:
    celdas = tabla_grafos.add_row().cells
    celdas[0].text = tipo_grafo
    celdas[1].text = relacion
    celdas[2].text = uso

DOC.add_paragraph(
    "Regla práctica aplicada: si la pregunta es «¿qué parte del total es X?», se usa un "
    "circular; si es «¿cuál tiene más?», se usan barras. Confundirlas produce gráficos "
    "engañosos: un circular con muchos valores pequeños deja las etiquetas amontonadas."
)

DOC.add_heading("7.3 Ejemplo práctico: implementación en el proyecto", level=2)

DOC.add_paragraph(
    "La implementación se encuentra en el módulo visualizacion.py, incorporado al programa "
    "como la opción 9 del menú principal. El módulo genera tres gráficos y los guarda como "
    "imágenes PNG en la carpeta graficos/."
)

DOC.add_paragraph(
    "El punto más importante del diseño es que los gráficos no usan datos inventados. "
    "Consumen la función estructuras.calcular_estadisticas_productividad(), que ya existía "
    "en el proyecto y alimenta la opción 6 del menú. Los gráficos muestran, por lo tanto, "
    "las mismas tareas reales que el usuario tiene cargadas."
)

DOC.add_paragraph("Funciones definidas en visualizacion.py:")
for texto in [
    "generar_grafico_distribucion(lista_tareas, ruta) — Circular de anillo con la distribución "
    "por estado. Muestra porcentaje y cantidad absoluta en cada sector.",
    "generar_grafico_avance(lista_tareas, ruta) — Dos paneles: el porcentaje completado y la "
    "cantidad de tareas por estado.",
    "generar_grafico_responsables(lista_tareas, ruta) — Barras horizontales con las tareas "
    "asignadas a cada persona, ordenadas de mayor a menor.",
    "generar_visualizaciones(lista_tareas, directorio) — Ejecuta los tres generadores y "
    "devuelve la lista de archivos creados.",
]:
    DOC.add_paragraph(texto, style="List Bullet")

DOC.add_paragraph("Ejemplo de uso desde el menú, opción 9:")
ejemplo_grafico = DOC.add_paragraph()
run = ejemplo_grafico.add_run(
    "rutas = visualizacion.generar_visualizaciones(tareas, \"graficos\")"
)
run.font.name = "Consolas"
run.font.size = Pt(9)

DOC.add_heading("7.3.1 Un detalle técnico: el backend Agg", level=3)

DOC.add_paragraph(
    "Un problema real apareció durante la implementación. Por defecto, matplotlib intenta "
    "abrir una ventana gráfica para mostrar el resultado, y el programa fallaba con un error "
    "de backend cuando no había display disponible, por ejemplo al ejecutarlo en un servidor "
    "o a través de una conexión remota."
)

DOC.add_paragraph(
    "La solución fue indicar el backend Agg antes de importar el módulo de dibujo. Este "
    "backend renderiza la figura directamente sobre una memoria intermedia y la escribe en "
    "un archivo, sin necesitar ninguna ventana del sistema operativo:"
)

ejemplo_agg = DOC.add_paragraph()
run = ejemplo_agg.add_run(
    "import matplotlib\n"
    "matplotlib.use(\"Agg\")          # renderiza a archivo, sin ventana\n"
    "import matplotlib.pyplot as plt   # debe importarse después"
)
run.font.name = "Consolas"
run.font.size = Pt(9)

DOC.add_paragraph(
    "El orden de las líneas importa: si pyplot se importa antes de fijar el backend, la "
    "configuración llega tarde y matplotlib ya decidió qué backend usar."
)

DOC.add_paragraph(
    "Otro error se detectó durante el desarrollo al ejecutar las pruebas automáticas: el "
    "primer intento mezclaba en un mismo eje el porcentaje de avance (escala de 0 a 100) y la "
    "cantidad de tareas (escala de 1 a n), lo que producía una gráfica donde las barras quedaban "
    "aplastadas contra el eje vertical y los rótulos se superponían. Se resolvió separando "
    "las dos magnitudes en paneles independientes, cada uno con su propia escala."
)

DOC.add_heading("7.4 Gráficos generados", level=2)

DOC.add_paragraph(
    "Las siguientes imágenes fueron producidas por el programa a partir de las tareas reales "
    "del tablero, ejecutando la opción 9."
)

GRAFICOS_INFORME = [
    (
        "grafico_distribucion_estados.png",
        "Figura 1. Distribución de tareas por estado. Gráfico circular: muestra cómo se reparte "
        "el total de tareas entre pendiente, en curso y finalizada.",
    ),
    (
        "grafico_avance.png",
        "Figura 2. Avance del trabajo. A la izquierda, la barra de progreso del porcentaje "
        "completado; a la derecha, la cantidad de tareas por estado.",
    ),
    (
        "grafico_carga_responsables.png",
        "Figura 3. Carga de trabajo por responsable. Barras horizontales ordenadas de mayor a "
        "menor, que permiten detectar si la distribución del trabajo está desbalanceada.",
    ),
]

graficos_insertados = 0
for nombre_archivo, pie_de_figura in GRAFICOS_INFORME:
    ruta_png = os.path.join(DIR_GRAFICOS, nombre_archivo)
    if not os.path.exists(ruta_png):
        DOC.add_paragraph(
            f"[No se encontró {nombre_archivo}. Ejecutá la opción 9 del programa para "
            f"generarlo antes de crear el documento.]",
            style="Intense Quote",
        )
        continue

    try:
        DOC.add_picture(ruta_png, width=Cm(14))
        DOC.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    except Exception as error:
        DOC.add_paragraph(
            f"[No se pudo insertar {nombre_archivo}: {error}]", style="Intense Quote"
        )
        continue

    graficos_insertados += 1

    pie = DOC.add_paragraph()
    run_pie = pie.add_run(pie_de_figura)
    run_pie.italic = True
    run_pie.font.size = Pt(9)
    pie.alignment = WD_ALIGN_PARAGRAPH.CENTER

if graficos_insertados == 0:
    DOC.add_paragraph(
        "Advertencia: el documento se generó sin imágenes porque la carpeta graficos/ está "
        "vacía. Corré la aplicación, elegí la opción 9 y volvé a ejecutar generar_informe.py.",
        style="Intense Quote",
    )

DOC.add_heading("7.5 ¿Qué aprendimos?", level=2)

DOC.add_paragraph(
    "El equipo aprendió que un gráfico no es solo una forma bonita de mostrar datos: es una "
    "afirmación sobre los datos. Elegir el tipo equivocado comunica algo falso. Por ejemplo, "
    "un circular donde una categoría tiene el 2 % del total produce una etiqueta ilegible, y "
    "una barra cuya escala no empieza en cero exagera o minimiza las diferencias."
)

DOC.add_paragraph("En concreto, el trabajo dejó estos aprendizajes:")
for texto in [
    "Los datos que se visualizan deben salir del sistema, no inventarse. Reutilizar "
    "calcular_estadisticas_productividad() garantizó que los gráficos reflejen la realidad "
    "del tablero.",
    "La escala de cada eje es parte del mensaje. Mezclar magnitudes incompatibles en un mismo "
    "eje fue el error principal que encontramos y corrigimos durante el desarrollo.",
    "matplotlib exige configurar el entorno antes de usarlo. El backend Agg y el orden de los "
    "imports son requisitos reales, no detalles opcionales.",
    "Separar el cálculo de la representación es una ventaja: como las estadísticas se calculan "
    "en estructuras.py, los gráficos de visualizacion.py no repiten ninguna lógica y podrían "
    "usarse en una interfaz web sin cambios.",
    "Las imágenes son un formato más de salida, igual que el CSV y el JSON. El programa ya "
    "persistía datos en archivos; con esta opción también los publica de forma visual.",
    "Los gráficos se validaron con pruebas automáticas que verifican la firma binaria PNG, de "
    "modo que se detecta si el archivo generado deja de ser una imagen válida.",
]:
    DOC.add_paragraph(texto, style="List Bullet")

DOC.add_paragraph(
    "Como conclusión, la visualización transformó las estadísticas de productividad —que hasta "
    "entonces solo se mostraban como números en una terminal— en información que se "
    "comprende de un vistazo y que puede sostener decisiones del equipo, como redistribuir "
    "tareas cuando se detecta que una persona está sobrecargada."
)

# --- Guardar ---
DOC.save("Desglose_del_Codigo_Gestor_de_Tareas.docx")
print("Documento generado: Desglose_del_Codigo_Gestor_de_Tareas.docx")