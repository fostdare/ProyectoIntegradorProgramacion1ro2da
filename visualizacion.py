# visualizacion.py
# Módulo de visualización de datos: genera gráficos PNG a partir de las
# estadísticas del tablero de tareas.
#
# Eje de investigación 3.8 - Opción D (Visualización de datos con matplotlib).
#
# Los gráficos se construyen a partir de estructuras.calcular_estadisticas_productividad(),
# es decir, los datos que el proyecto ya produce: no hay datos simulados.

import os

import matplotlib

# Backend Agg: renderiza a archivo sin abrir ventana. Necesario porque la
# aplicación es de consola y en un servidor no existe un display disponible.
matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402  (debe importarse tras el backend)

from estructuras import calcular_estadisticas_productividad  # noqa: E402

ESTADOS = ("pendiente", "en_curso", "finalizada")

ETIQUETA_ESTADO = {
    "pendiente": "Pendientes",
    "en_curso": "En curso",
    "finalizada": "Finalizadas",
}

COLORES = {
    "pendiente": "#e8a33d",
    "en_curso": "#4a90d9",
    "finalizada": "#4caf7d",
}

NOMBRE_DISTRIBUCION = "grafico_distribucion_estados.png"
NOMBRE_AVANCE = "grafico_avance.png"
NOMBRE_RESPONSABLE = "grafico_carga_responsables.png"


def _preparar_figura(titulo, subtitulo):
    """Crea una figura con tamaño y titulado consistentes entre gráficos."""
    fig, ax = plt.subplots(figsize=(8, 5), dpi=140)
    fig.patch.set_facecolor("white")
    ax.set_title(titulo, fontsize=14, fontweight="bold", pad=18)
    if subtitulo:
        ax.annotate(
            subtitulo,
            xy=(0.5, 1.0),
            xycoords="axes fraction",
            xytext=(0, 8),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9,
            color="#666666",
        )
    return fig, ax


def _cerrar(fig, ruta_salida):
    """Ajusta los margenes, guarda el PNG y libera la figura."""
    fig.tight_layout()
    fig.savefig(ruta_salida, format="png", bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return ruta_salida


def generar_grafico_distribucion(lista_tareas, ruta_salida=NOMBRE_DISTRIBUCION):
    """
    Genera un gráfico de anillo con la distribución de tareas por estado.
    Retorna la ruta del PNG, o None si no hay tareas.
    """
    stats = calcular_estadisticas_productividad(lista_tareas)
    if stats["total_tareas"] == 0:
        return None

    valores = [stats["pendientes"], stats["en_curso"], stats["finalizadas"]]
    etiquetas = [ETIQUETA_ESTADO[e] for e in ESTADOS]
    colores = [COLORES[e] for e in ESTADOS]

    fig, ax = _preparar_figura(
        "Distribución de tareas por estado",
        f"{stats['total_tareas']} tarea(s) en el tablero",
    )

    def formato_autopct(porcentaje):
        cantidad = int(round(porcentaje * stats["total_tareas"] / 100))
        return f"{porcentaje:.0f}%\n({cantidad})"

    ax.pie(
        valores,
        labels=etiquetas,
        colors=colores,
        autopct=formato_autopct,
        startangle=90,
        counterclock=False,
        wedgeprops={"edgecolor": "white", "linewidth": 2},
        textprops={"fontsize": 10},
    )
    ax.axis("equal")

    return _cerrar(fig, ruta_salida)


def generar_grafico_avance(lista_tareas, ruta_salida=NOMBRE_AVANCE):
    """
    Genera un gráfico de avance en dos paneles con escalas separadas:
    izquierda, el porcentaje completado (0-100 %); derecha, la cantidad
    de tareas por estado. Retorna la ruta del PNG, o None si no hay tareas.
    """
    stats = calcular_estadisticas_productividad(lista_tareas)
    if stats["total_tareas"] == 0:
        return None

    fig, (ax_porcentaje, ax_estados) = plt.subplots(
        1, 2, figsize=(10, 4.5), dpi=140,
        gridspec_kw={"width_ratios": [1, 1.4]},
    )
    fig.patch.set_facecolor("white")
    fig.suptitle("Avance del trabajo", fontsize=14, fontweight="bold", y=0.98)
    fig.text(
        0.5, 0.91,
        f"{stats['total_tareas']} tarea(s) en el tablero",
        ha="center", fontsize=9, color="#666666",
    )

    # Panel izquierdo: porcentaje completado, escala fija 0-100
    porcentaje = stats["porcentaje_completadas"]
    ax_porcentaje.barh(
        ["Completado"],
        [porcentaje],
        color=COLORES["finalizada"],
        height=0.62,
        edgecolor="white",
    )
    ax_porcentaje.barh(
        ["Completado"],
        [100 - porcentaje],
        left=[porcentaje],
        color="#e9ecef",
        height=0.62,
        edgecolor="white",
    )
    ax_porcentaje.set_xlim(0, 100)
    ax_porcentaje.set_ylim(-0.5, 0.5)
    ax_porcentaje.set_yticks([])
    ax_porcentaje.set_xlabel("Porcentaje completado (%)")
    ax_porcentaje.annotate(
        f"{porcentaje}%",
        xy=(50, 0), ha="center", va="center",
        fontsize=18, fontweight="bold", color="#1a1a1a",
    )
    ax_porcentaje.grid(axis="x", linestyle="--", alpha=0.3)
    ax_porcentaje.set_axisbelow(True)

    # Panel derecho: cantidad de tareas por estado, escala propia en conteos
    estados_con_cantidad = [
        (ETIQUETA_ESTADO[e], stats_key)
        for e, stats_key in zip(
            ESTADOS, ("pendientes", "en_curso", "finalizadas")
        )
    ]
    cantidades = [stats[clave] for _, clave in estados_con_cantidad]
    colores = [COLORES[e] for e in ESTADOS]
    maximo = max(cantidades + [1])

    barras = ax_estados.barh(
        [nombre for nombre, _ in estados_con_cantidad],
        cantidades,
        color=colores,
        height=0.55,
        edgecolor="white",
    )
    ax_estados.bar_label(barras, padding=4, fontsize=10, fontweight="bold")
    ax_estados.set_xlim(0, maximo + maximo * 0.18)
    ax_estados.set_xlabel("Cantidad de tareas")
    ax_estados.invert_yaxis()
    ax_estados.grid(axis="x", linestyle="--", alpha=0.3)
    ax_estados.set_axisbelow(True)

    fig.tight_layout(rect=(0, 0, 1, 0.88))
    fig.savefig(ruta_salida, format="png", bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return ruta_salida


def generar_grafico_responsables(lista_tareas, ruta_salida=NOMBRE_RESPONSABLE):
    """
    Genera un gráfico de barras horizontales con la cantidad de tareas
    asignada a cada responsable, ordenado de mayor a menor.
    Retorna la ruta del PNG, o None si no hay tareas.
    """
    if not lista_tareas:
        return None

    conteo = {}
    for tarea in lista_tareas:
        nombre = (tarea["responsable"] or "Sin asignar").strip() or "Sin asignar"
        conteo[nombre] = conteo.get(nombre, 0) + 1

    if not conteo:
        return None

    # Ordenar de mayor a menor: el equipo más cargado queda arriba.
    ordenados = sorted(conteo.items(), key=lambda par: par[1])
    nombres = [par[0] for par in ordenados]
    cantidades = [par[1] for par in ordenados]

    total = sum(cantidades)
    fig, ax = _preparar_figura(
        "Carga de trabajo por responsable",
        f"{len(nombres)} responsable(s), {total} tarea(s) en total",
    )

    barras = ax.barh(
        nombres,
        cantidades,
        color="#4a90d9",
        edgecolor="white",
        height=0.6,
    )
    ax.bar_label(barras, padding=4, fontsize=10, fontweight="bold")

    ax.set_xlabel("Tareas asignadas")
    ax.set_xlim(0, max(cantidades) + 1)
    ax.grid(axis="x", linestyle="--", alpha=0.35)
    ax.set_axisbelow(True)

    return _cerrar(fig, ruta_salida)


def generar_visualizaciones(lista_tareas, directorio="."):
    """
    Genera todos los gráficos del proyecto en el directorio indicado.
    Retorna la lista de rutas de los PNG creados.
    """
    os.makedirs(directorio, exist_ok=True)

    generadores = (
        (generar_grafico_distribucion, NOMBRE_DISTRIBUCION),
        (generar_grafico_avance, NOMBRE_AVANCE),
        (generar_grafico_responsables, NOMBRE_RESPONSABLE),
    )

    rutas = []
    for generar, nombre in generadores:
        ruta = generar(lista_tareas, os.path.join(directorio, nombre))
        if ruta:
            rutas.append(ruta)

    return rutas