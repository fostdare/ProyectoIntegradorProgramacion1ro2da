# PROMPTS.md — Registro de código generado y aportes por autor

**Repositorio:** `fostdare/ProyectoIntegradorProgramacion1ro2da`
**Rama:** `main`
**Fecha de elaboración:** 2026-10-13

---

```bash
git show 18497ec   # código generado
git show bef4d3d   # aporte de Juan Benegas
git show b686446   # aporte de Máximo Aceituno
```

---

## 1. Código generado con asistencia de IA

- **Autor del commit:** `fostdare` <291925670+fostdare@users.noreply.github.com>
- **Commit:** `18497ec` — `feat: agregar eliminación de tareas`
- **Fecha:** 2026-10-05 14:39:56 -0300
- **Alcance:** 2 archivos, +44 / −1

### Objetivo (reconstrucción)

> Agregar al Gestor de Tareas una opción para eliminar una tarea existente por
> su ID, siguiendo el mismo patrón que las demás opciones del menú: validar
> entrada con los helpers de `utils`, pedir confirmación, eliminar, persistir
> en JSON y registrar la acción en el log.

### Qué se generó

#### `estructuras.py` — función de dominio

Se agregó `eliminar_tarea()` junto a las demás operaciones de la lista
(`cambiar_estado_tarea`, `calcular_estadisticas_productividad`). Mismo contrato:
recibe la lista y el ID, devuelve `True` si tuvo éxito, `False` si no
encontró coincidencia.

```python
def eliminar_tarea(lista_tareas, id_tarea):
    """
    Elimina una tarea por su ID. Retorna True si tuvo éxito.
    """
    for tarea in lista_tareas:
        if tarea["id"] == id_tarea:
            lista_tareas.remove(tarea)
            return True
    return False
```

#### `main.py` — submenú de interacción

`submenu_eliminar_tarea()` replica la estructura de los submenús existentes:
tabla de referencia, validación de entero acotada (1–999999), confirmación
`s/n`, yearly return si el usuario cancela con Tab o responde `n`.

```python
def submenu_eliminar_tarea(lista_tareas):
    """Submenú para eliminar una tarea existente."""
    if not lista_tareas:
        print("\n[ No hay tareas para eliminar. ]")
        return

    utils.mostrar_tabla_tareas(lista_tareas)
    id_tarea = utils.validar_entero_menu(
        "Ingrese el ID de la tarea a eliminar: ", 1, 999999
    )
    if id_tarea is None:
        return

    confirmar = utils.validar_opcion_lista(
        "¿Confirma la eliminación? (s/n): ", ["s", "n"]
    )
    if confirmar != "s":
        return

    exito = estructuras.eliminar_tarea(lista_tareas, id_tarea)
    if exito:
        persistencia.guardar_datos_json(RUTA_JSON, lista_tareas)
        persistencia.registrar_log(
            RUTA_LOG, "ELIMINAR_TAREA", f"Tarea ID {id_tarea} eliminada"
        )
        print(" ✅ Tarea eliminada correctamente.")
    else:
        print(" ❌ No se encontró ninguna tarea con ese ID.")
```

#### `main.py` — integración en el menú principal

Tres cambios mínimos para exponer la función:

```diff
         print("  7. Exportar reporte a archivo CSV")
+        print("  8. Eliminar tarea")
         print("  0. Salir del programa")
 
-        opcion = utils.validar_entero_menu("Seleccione una opción: ", 0, 7)
+        opcion = utils.validar_entero_menu("Seleccione una opción: ", 0, 8)

+        elif opcion == 8:
+            submenu_eliminar_tarea(tareas)
```

**Observación de diseño relevante:** el rango de validación pasó de `0, 7` a
`0, 8`. Ese es el tipo de acoplamiento que rompe silenciosamente cuando se
agrega una opción al final del menú — si se hubiera agregado en el medio, el
rango igual habría quedado mal. Vale la pena registrarlo porque es el punto
más frágil del `menu_principal()`.

---

## 2. Modificaciones de los compañeros

Estas modificaciones son **trabajo humano**, sin asistencia de IA. Se
documentan porque forman parte del mismo archivo y porque cambiaron
contratos que el código generado consume.

### 2.1 Juan Benegas — `jnbenegas@gmail.com`

- **Commit:** `bef4d3d` — `corregido formato de fecha a huso horario de Argentina`
- **Fecha:** 2026-10-02 21:12:44 -0300
- **Alcance:** 5 archivos, +92 / −8

**Objetivo (reconstrucción a partir del diff):** cambiar el formato de fecha de
`AAAA-MM-DD` a `DD/MM/YYYY` en toda la aplicación, validar que no se acepte una
fecha pasada, y forzar UTF-8 en la salida de consola.

#### `utils.py` — nueva función de validación de fecha

```python
FORMATO_FECHA = "%d/%m/%Y"


def validar_fecha(mensaje, permitir_vacio=False):
    """
    Solicita una fecha con formato DD/MM/YYYY y la valida.
    Retorna el string DD/MM/YYYY, None si cancela (Tab/vacío), o "" si permitir_vacio y está vacía.
    """
    while True:
        entrada = _input_inmediato(mensaje)
        if entrada is None or entrada.strip() == "":
            if permitir_vacio and entrada is not None:
                return ""
            return None
        texto = entrada.strip()
        try:
            fecha = datetime.strptime(texto, FORMATO_FECHA)
            if fecha.date() < datetime.now().date():
                print(" Error: La fecha no puede ser anterior a hoy.")
                continue
            return texto
        except ValueError:
            print(" Error: Formato inválido. Use DD/MM/YYYY (ej. 25/12/2026).")
```

Además broadened la captura de excepciones del fallback de teclado:
`except (ImportError, AttributeError, termios.error)` →
`except (ImportError, AttributeError, OSError)`. `termios.error` es subclase
de `OSError`, así que el cambio es correcto y más portable.

#### `main.py` — UTF-8 forzado y validación al editar

```python
import sys

# Forzar UTF-8 en consola para evitar errores con emojis en Windows
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass
```

Y en `submenu_actualizar_tarea()`, validación de la fecha nueva con rechazo de
fechas pasadas y formato incorrecto, más `.strip()` antes de asignar.

#### `persistencia.py` — formato del timestamp del log

```diff
-    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
+    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
```

Esto explica las 21 líneas agregadas a `log_actividad.txt`: son entradas
escritas con el formato nuevo, no código.

### 2.2 Máximo Aceituno — `maximonyan@gmail.com`

- **Commit:** `b686446` — `modificados algunos carteles del menu principal`
- **Fecha:** 2026-10-02 21:52:56 -0300
- **Alcance:** 2 archivos, +4 / −6

**Objetivo (reconstrucción a partir del diff):** eliminar el banner duplicado
que se imprimía en cada iteración del bucle y renombrar el título de la
aplicación.

```diff
-    print("\n" + "=" * 45)
-    print("    📋 GESTOR DE TAREAS - CLON TRELLO")
-    print("    ⚡ Versión Python Vanilla")
-    print("=" * 45)
-    
     while True:
         print("\n" + "=" * 45)
-        print("    GESTOR DE TAREAS - CLON TRELLO")
+        print("    Gestor de Tareas - Lazarus")
         print("=" * 45)
```

El banner estaba **fuera** del `while True`, así que se imprimía una vez como
encabezado y de nuevo en cada vuelta del menú. Este commit lo dejó solo
adentro. Las 2 líneas de `log_actividad.txt` son entradas de esa sesión.

El nombre **"Gestor de Tareas - Lazarus"** es el que figura hoy en el
`README.md` y en el menú.

---

## 3. Resumen de atribución

| Aporte | Autor | Commit | Archivos | +/− |
|---|---|---|---|---|
| Base del proyecto, reescritura a consola | Geronimo Concina | `a46a61a`, `fe9e9e8`, entre otros | 11 | ~1800 |
| Validación de fechas `DD/MM/YYYY`, UTF-8 en consola | Juan Benegas | `bef4d3d` | 5 | +92 / −8 |
| Banner del menú, nombre "Lazarus" | Máximo Aceituno | `b686446` | 2 | +4 / −6 |
| **Eliminación de tareas (generado con IA)** | **fostdare** | `18497ec` | 2 | +44 / −1 |
La lógica encaja con lo que ya vienen usando: estructuras.py cambia la lista y devuelve True o False; main.py muestra el menú, guarda el JSON y registra la acción.

Propongo agregar esta función a estructuras.py:


Y en main.py, un submenú que muestre las tareas, pida el ID y confirme antes de eliminar:


También agregaría la opción 8. Eliminar tarea al menú, ampliaría el rango de opciones hasta 8 y conectaría esa opción con el submenú. El chequeo más directo sería probar que un ID existente se elimina y devuelve True, y que uno inexistente no cambia la lista y devuelve False.

Todavía no hice cambios ni subí nada. Cuando me confirmes que esta propuesta te sirve, la implemento, la pruebo y luego preparo el push a GitHub.


---
