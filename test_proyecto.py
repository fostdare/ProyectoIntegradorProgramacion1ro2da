# test_proyecto.py
# Pruebas unitarias para validar funciones clave del dominio y la persistencia

import unittest
import os
import estructuras
import persistencia

class TestClonTrello(unittest.TestCase):

    def test_crear_tarea(self):
        tarea = estructuras.crear_tarea(1, "Fix Bug", "Error login", 1, "pendiente", "Dev", "Ana", "2026-10-01")
        self.assertEqual(tarea["id"], 1)
        self.assertEqual(tarea["titulo"], "Fix Bug")
        self.assertEqual(tarea["estado"], "pendiente")

    def test_filtrar_tareas(self):
        t1 = estructuras.crear_tarea(1, "T1", "D1", 1, "pendiente", "Dev", "Ana", "2026-10-01")
        t2 = estructuras.crear_tarea(2, "T2", "D2", 2, "finalizada", "QA", "Juan", "2026-10-01")
        lista = [t1, t2]
        res = estructuras.filtrar_tareas(lista, estado="pendiente")
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]["id"], 1)

    def test_calcular_estadisticas(self):
        t1 = estructuras.crear_tarea(1, "T1", "D1", 1, "pendiente", "Dev", "Ana", "2026-10-01")
        t2 = estructuras.crear_tarea(2, "T2", "D2", 2, "finalizada", "QA", "Juan", "2026-10-01")
        stats = estructuras.calcular_estadisticas_productividad([t1, t2])
        self.assertEqual(stats["total_tareas"], 2)
        self.assertEqual(stats["porcentaje_completadas"], 50.0)

    def test_persistencia_json(self):
        ruta_temp = "test_tareas.json"
        datos_test = [{"id": 1, "titulo": "Prueba"}]
        persistencia.guardar_datos_json(ruta_temp, datos_test)
        cargados = persistencia.cargar_datos_json(ruta_temp)
        self.assertEqual(len(cargados), 1)
        if os.path.exists(ruta_temp):
            os.remove(ruta_temp)

    def test_cambiar_estado_tarea(self):
        t1 = estructuras.crear_tarea(1, "T1", "D1", 1, "pendiente", "Dev", "Ana", "2026-10-01")
        lista = [t1]
        exito = estructuras.cambiar_estado_tarea(lista, 1, "en_curso")
        self.assertTrue(exito)
        self.assertEqual(lista[0]["estado"], "en_curso")

if __name__ == "__main__":
    unittest.main()