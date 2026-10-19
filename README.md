# 📋 Gestor de Tareas - Lazarus

Aplicación de consola para gestión de tareas al estilo Trello.

## Ejecución

```bash
python main.py
```

## Pruebas

```bash
python -m unittest test_proyecto -v
```

## Características

- Alta de nuevas tareas (título, descripción, prioridad, categoría, responsable, fecha límite)
- Consultar y filtrar tareas por estado, categoría o responsable
- Ver detalle completo de una tarea
- Modificar cualquier campo de una tarea
- Cambiar estado (pendiente / en_curso / finalizada)
- Estadísticas de productividad
- Exportar reporte a CSV
- Persistencia en JSON
- Registro de actividad en log TXT
- Generación de gráficos de estadísticas en PNG (opción 9)

## Dependencias

- Python 3.10+ estándar
- matplotlib (para la generación de gráficos)

## Estructura

```
proyecto-tareas-console/
├── main.py
├── estructuras.py
├── persistencia.py
├── utils.py
├── tareas.json
├── log_actividad.txt
└── README.md
```
