# test_proyecto.py
# Suite de pruebas automaticas del Gestor de Tareas.
# Ejecutar con: python -m unittest test_proyecto -v

import os
import tempfile
import unittest
from datetime import datetime, timedelta

import estructuras
import persistencia
import utils
import visualizacion


def tarea_prueba(id_tarea=1, titulo="Tarea", estado="pendiente",
                 prioridad=2, categoria="Trabajo", responsable="Ana"):
    """Atajo para construir una tarea valida en las pruebas."""
    fecha = (datetime.now() + timedelta(days=7)).strftime(utils.FORMATO_FECHA)
    return estructuras.crear_tarea(
        id_tarea, titulo, "Descripcion de prueba", prioridad,
        estado, categoria, responsable, fecha
    )


class TestCrearTarea(unittest.TestCase):
    def test_retorna_las_ocho_claves(self):
        tarea = tarea_prueba()
        self.assertEqual(
            set(tarea.keys()),
            {"id", "titulo", "descripcion", "prioridad", "estado",
             "categoria", "responsable", "fecha_limite"}
        )

    def test_conserva_los_valores_ingresados(self):
        tarea = tarea_prueba(id_tarea=7, titulo="Deploy", estado="en_curso")
        self.assertEqual(tarea["id"], 7)
        self.assertEqual(tarea["titulo"], "Deploy")
        self.assertEqual(tarea["estado"], "en_curso")


class TestObtenerSiguienteId(unittest.TestCase):
    def test_lista_vacia_retorna_uno(self):
        self.assertEqual(estructuras.obtener_siguiente_id([]), 1)

    def test_retorna_maximo_mas_uno(self):
        lista = [tarea_prueba(3), tarea_prueba(9), tarea_prueba(5)]
        self.assertEqual(estructuras.obtener_siguiente_id(lista), 10)

    def test_no_reutiliza_ids_eliminados(self):
        lista = [tarea_prueba(1), tarea_prueba(4)]
        estructuras.eliminar_tarea(lista, 4)
        self.assertEqual(estructuras.obtener_siguiente_id(lista), 2)


class TestFiltrarTareas(unittest.TestCase):
    def setUp(self):
        self.lista = [
            tarea_prueba(1, "A", "pendiente", categoria="Trabajo", responsable="Ana"),
            tarea_prueba(2, "B", "en_curso", categoria="Trabajo", responsable="Beto"),
            tarea_prueba(3, "C", "finalizada", categoria="Estudio", responsable="Caro"),
        ]

    def test_sin_criterios_devuelve_todo(self):
        self.assertEqual(len(estructuras.filtrar_tareas(self.lista)), 3)

    def test_filtro_por_estado_ignora_mayusculas(self):
        resultado = estructuras.filtrar_tareas(self.lista, estado="EN_CURSO")
        self.assertEqual([t["id"] for t in resultado], [2])

    def test_filtro_por_categoria(self):
        resultado = estructuras.filtrar_tareas(self.lista, categoria="estudio")
        self.assertEqual([t["id"] for t in resultado], [3])

    def test_filtro_responsable_es_parcial(self):
        resultado = estructuras.filtrar_tareas(self.lista, responsable="an")
        self.assertEqual([t["id"] for t in resultado], [1])

    def test_criterios_combinados_se_intersecan(self):
        resultado = estructuras.filtrar_tareas(
            self.lista, estado="pendiente", categoria="Trabajo", responsable="Ana"
        )
        self.assertEqual([t["id"] for t in resultado], [1])

    def test_sin_coincidencias_retorna_lista_vacia(self):
        self.assertEqual(estructuras.filtrar_tareas(self.lista, estado="bloqueada"), [])


class TestOrdenarPorPrioridad(unittest.TestCase):
    def test_ordena_de_alta_a_baja(self):
        lista = [tarea_prueba(1, prioridad=3), tarea_prueba(2, prioridad=1),
                 tarea_prueba(3, prioridad=2)]
        resultado = estructuras.ordenar_tareas_por_prioridad(lista)
        self.assertEqual([t["prioridad"] for t in resultado], [1, 2, 3])

    def test_no_modifica_la_lista_original(self):
        lista = [tarea_prueba(1, prioridad=3), tarea_prueba(2, prioridad=1)]
        estructuras.ordenar_tareas_por_prioridad(lista)
        self.assertEqual([t["prioridad"] for t in lista], [3, 1])


class TestCambiarEstado(unittest.TestCase):
    def test_cambia_el_estado_existente(self):
        lista = [tarea_prueba(1)]
        self.assertTrue(estructuras.cambiar_estado_tarea(lista, 1, "finalizada"))
        self.assertEqual(lista[0]["estado"], "finalizada")

    def test_id_inexistente_retorna_false(self):
        lista = [tarea_prueba(1)]
        self.assertFalse(estructuras.cambiar_estado_tarea(lista, 99, "finalizada"))


class TestEliminarTarea(unittest.TestCase):
    def test_elimina_por_id(self):
        lista = [tarea_prueba(1), tarea_prueba(2)]
        self.assertTrue(estructuras.eliminar_tarea(lista, 1))
        self.assertEqual([t["id"] for t in lista], [2])

    def test_id_inexistente_retorna_false(self):
        lista = [tarea_prueba(1)]
        self.assertFalse(estructuras.eliminar_tarea(lista, 42))
        self.assertEqual(len(lista), 1)


class TestEstadisticas(unittest.TestCase):
    def test_lista_vacia_retorna_ceros(self):
        stats = estructuras.calcular_estadisticas_productividad([])
        self.assertEqual(stats["total_tareas"], 0)
        self.assertEqual(stats["porcentaje_completadas"], 0.0)

    def test_cuenta_por_estado(self):
        lista = [
            tarea_prueba(1, estado="pendiente"),
            tarea_prueba(2, estado="en_curso"),
            tarea_prueba(3, estado="finalizada"),
            tarea_prueba(4, estado="finalizada"),
        ]
        stats = estructuras.calcular_estadisticas_productividad(lista)
        self.assertEqual(stats["total_tareas"], 4)
        self.assertEqual(stats["pendientes"], 1)
        self.assertEqual(stats["en_curso"], 1)
        self.assertEqual(stats["finalizadas"], 2)
        self.assertEqual(stats["porcentaje_completadas"], 50.0)


class TestPersistenciaJson(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.ruta = os.path.join(self.dir, "tareas_test.json")

    def test_archivo_inexistente_se_crea_vacio(self):
        self.assertEqual(persistencia.cargar_datos_json(self.ruta), [])
        self.assertTrue(os.path.exists(self.ruta))

    def test_guardar_y_cargar_preserva_los_datos(self):
        lista = [tarea_prueba(1), tarea_prueba(2, titulo="Segunda")]
        self.assertTrue(persistencia.guardar_datos_json(self.ruta, lista))
        self.assertEqual(persistencia.cargar_datos_json(self.ruta), lista)

    def test_acentos_se_persisten_sin_escape(self):
        lista = [tarea_prueba(1)]
        lista[0]["titulo"] = "Revision de codigo"
        lista[0]["responsable"] = "José"
        persistencia.guardar_datos_json(self.ruta, lista)
        self.assertEqual(persistencia.cargar_datos_json(self.ruta)[0]["responsable"], "José")

    def test_json_corrupto_retorna_lista_vacia(self):
        with open(self.ruta, "w", encoding="utf-8") as f:
            f.write("{esto no es json")
        self.assertEqual(persistencia.cargar_datos_json(self.ruta), [])


class TestPersistenciaCsv(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.ruta = os.path.join(self.dir, "reporte_test.csv")

    def test_exporta_encabezado_y_filas(self):
        import csv
        lista = [tarea_prueba(1, titulo="Con comas, aqui"), tarea_prueba(2)]
        self.assertTrue(persistencia.exportar_reporte_csv(self.ruta, lista))
        with open(self.ruta, newline="", encoding="utf-8") as f:
            filas = list(csv.DictReader(f))
        self.assertEqual(len(filas), 2)
        self.assertEqual(filas[0]["titulo"], "Con comas, aqui")
        self.assertEqual(filas[0]["estado"], "pendiente")

    def test_lista_vacia_solo_escribe_encabezado(self):
        import csv
        persistencia.exportar_reporte_csv(self.ruta, [])
        with open(self.ruta, newline="", encoding="utf-8") as f:
            filas = list(csv.reader(f))
        self.assertEqual(len(filas), 1)
        self.assertIn("titulo", filas[0])


class TestRegistroLog(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.ruta = os.path.join(self.dir, "log_test.txt")

    def test_escribe_la_accion_con_timestamp(self):
        self.assertTrue(persistencia.registrar_log(self.ruta, "CREAR", "tarea 1"))
        with open(self.ruta, encoding="utf-8") as f:
            contenido = f.read()
        self.assertIn("ACCION: CREAR", contenido)
        self.assertIn("DETALLE: tarea 1", contenido)

    def test_agrega_lineas_sin_sobreescribir(self):
        persistencia.registrar_log(self.ruta, "CREAR", "tarea 1")
        persistencia.registrar_log(self.ruta, "EDITAR", "tarea 1")
        with open(self.ruta, encoding="utf-8") as f:
            self.assertEqual(len(f.readlines()), 2)


class TestValidacionDeEntradas(unittest.TestCase):
    """Las funciones de validacion usan la terminal; se simula _input_inmediato."""

    def setUp(self):
        self.original = utils._input_inmediato

    def tearDown(self):
        utils._input_inmediato = self.original

    def simular(self, *entradas):
        """Programa una secuencia de entradas; None simula cancelar con Tab."""
        secuencia = list(entradas)

        def fake(mensaje):
            return secuencia.pop(0) if len(secuencia) > 1 else secuencia[0]

        utils._input_inmediato = fake

    def test_validar_fecha_acepta_formato_correcto(self):
        self.simular("25/12/2026")
        self.assertEqual(utils.validar_fecha("Fecha: "), "25/12/2026")

    def test_validar_fecha_rechaza_formato_incorrecto(self):
        self.simular("2026-12-25", "25/12/2026")
        self.assertEqual(utils.validar_fecha("Fecha: "), "25/12/2026")

    def test_validar_fecha_rechaza_fecha_pasada(self):
        self.simular("01/01/2020", "25/12/2026")
        self.assertEqual(utils.validar_fecha("Fecha: "), "25/12/2026")

    def test_validar_fecha_tab_retorna_none(self):
        self.simular(None)
        self.assertIsNone(utils.validar_fecha("Fecha: "))

    def test_validar_fecha_vacia_permitida_retorna_string_vacio(self):
        self.simular("")
        self.assertEqual(utils.validar_fecha("Fecha: ", permitir_vacio=True), "")

    def test_validar_entero_acepta_valor_en_rango(self):
        self.simular("5")
        self.assertEqual(utils.validar_entero_menu("Opcion: ", 1, 10), 5)

    def test_validar_entero_rechaza_fuera_de_rango(self):
        self.simular("99", "3")
        self.assertEqual(utils.validar_entero_menu("Opcion: ", 1, 10), 3)

    def test_validar_entero_rechaza_texto(self):
        self.simular("abc", "7")
        self.assertEqual(utils.validar_entero_menu("Opcion: ", 1, 10), 7)

    def test_validar_entero_limites_incluidos(self):
        self.simular("1", "10")
        self.assertEqual(utils.validar_entero_menu("Opcion: ", 1, 10), 1)
        self.assertEqual(utils.validar_entero_menu("Opcion: ", 1, 10), 10)

    def test_validar_texto_no_vacio_recorta_espacios(self):
        self.simular("  hola  ")
        self.assertEqual(utils.validar_texto_no_vacio("Texto: "), "hola")

    def test_validar_texto_no_vacio_tab_retorna_none(self):
        self.simular(None)
        self.assertIsNone(utils.validar_texto_no_vacio("Texto: "))

    def test_validar_opcion_lista_normaliza_a_minusculas(self):
        self.simular("Trabajo")
        self.assertEqual(
            utils.validar_opcion_lista("Categoria: ", ["trabajo", "estudio"]),
            "trabajo"
        )

    def test_validar_opcion_lista_rechaza_no_valida(self):
        self.simular("otro", "estudio")
        self.assertEqual(
            utils.validar_opcion_lista("Categoria: ", ["trabajo", "estudio"]),
            "estudio"
        )


class TestVisualizacion(unittest.TestCase):
    """Eje de investigación 3.8 opción D: verificación de los PNG generados."""

    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.lista = [
            tarea_prueba(1, "A", "pendiente"),
            tarea_prueba(2, "B", "en_curso"),
            tarea_prueba(3, "C", "finalizada", responsable="Beto"),
            tarea_prueba(4, "D", "finalizada", responsable="Beto"),
        ]

    def es_png_valido(self, ruta):
        with open(ruta, "rb") as f:
            # Los archivos PNG empiezan con estos 8 bytes de firma.
            return f.read(8) == b"\x89PNG\r\n\x1a\n"

    def test_distribucion_genera_png(self):
        ruta = visualizacion.generar_grafico_distribucion(
            self.lista, os.path.join(self.dir, "d.png")
        )
        self.assertTrue(os.path.exists(ruta))
        self.assertGreater(os.path.getsize(ruta), 0)
        self.assertTrue(self.es_png_valido(ruta))

    def test_avance_genera_png(self):
        ruta = visualizacion.generar_grafico_avance(
            self.lista, os.path.join(self.dir, "a.png")
        )
        self.assertTrue(os.path.exists(ruta))
        self.assertTrue(self.es_png_valido(ruta))

    def test_responsables_genera_png(self):
        ruta = visualizacion.generar_grafico_responsables(
            self.lista, os.path.join(self.dir, "r.png")
        )
        self.assertTrue(os.path.exists(ruta))
        self.assertTrue(self.es_png_valido(ruta))

    def test_lista_vacia_retorna_none(self):
        for generar in (
            visualizacion.generar_grafico_distribucion,
            visualizacion.generar_grafico_avance,
            visualizacion.generar_grafico_responsables,
        ):
            self.assertIsNone(generar([], os.path.join(self.dir, "vacio.png")))

    def test_responsable_vacio_se_agrupa_como_sin_asignar(self):
        lista = [tarea_prueba(1, responsable="   "), tarea_prueba(2, responsable="")]
        ruta = visualizacion.generar_grafico_responsables(
            lista, os.path.join(self.dir, "sin.png")
        )
        self.assertTrue(os.path.exists(ruta))

    def test_todas_las_visualizaciones_devuelve_tres_rutas(self):
        rutas = visualizacion.generar_visualizaciones(self.lista, self.dir)
        self.assertEqual(len(rutas), 3)
        for ruta in rutas:
            self.assertTrue(self.es_png_valido(ruta))

    def test_directorio_inexistente_se_crea(self):
        destino = os.path.join(self.dir, "sub", "carpeta")
        rutas = visualizacion.generar_visualizaciones(self.lista, destino)
        self.assertTrue(os.path.isdir(destino))
        self.assertEqual(len(rutas), 3)

    def test_lista_vacia_no_crea_archivos(self):
        rutas = visualizacion.generar_visualizaciones([], self.dir)
        self.assertEqual(rutas, [])
        self.assertEqual(os.listdir(self.dir), [])


class TestMostrarTabla(unittest.TestCase):
    def test_tabla_vacia_no_falla(self):
        utils.mostrar_tabla_tareas([])

    def test_tabla_con_tareas_no_falla(self):
        utils.mostrar_tabla_tareas([tarea_prueba(1, titulo="X" * 40)])


if __name__ == "__main__":
    unittest.main(verbosity=2)