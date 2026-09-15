# 📋 Trello Clon - Gestor de Tareas (FastAPI)

Proyecto integrador de **Programación I** — Tecnicatura Superior en Desarrollo de Software (2026).

Un clon de Trello completo con interfaz web moderna, API REST y lógica de dominio de gestión de tareas.

---

## 🚀 Despliegue Rápido

### Requisitos previos

- Python 3.10+
- pip o pip3
- Git

### 1. Clonar el repositorio

```bash
git clone https://github.com/fostdare/ProyectoIntegradorProgramacion1ro2da.git
cd ProyectoIntegradorProgramacion1ro2da
```

### 2. Crear entorno virtual e instalar dependencias

```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
# venv\Scripts\activate         # Windows

pip install -r requeriments.txt
```

### 3. Ejecutar el servidor

```bash
python -m app.main
```

El servidor inicia en **`http://localhost:8000`**.

### 4. Abrir en el navegador

Ingresá a **`http://localhost:8000`** en cualquier navegador (Chrome, Firefox, Vivaldi, Edge, Safari).

### 5. Documentación interactiva

FastAPI genera documentación automática:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

---

## 📁 Estructura del Proyecto

```
ProyectoIntegradorProgramacion1ro2da/
├── app/
│   ├── __init__.py
│   ├── main.py           # App FastAPI: servidor web, CORS, rutas estáticas
│   ├── models.py         # Modelos Pydantic para validación de datos
│   └── routes.py         # Endpoints REST (CRUD completo)
├── templates/
│   └── index.html        # Frontend único (SPA con Jinja2)
├── static/
│   ├── css/
│   │   └── style.css     # Estilos: tema oscuro, responsive
│   └── js/
│       └── app.js        # Lógica frontend con fetch()
├── estructuras.py        # Lógica de dominio (crear, filtrar, ordenar, stats)
├── persistencia.py       # Persistencia JSON, CSV y logs
├── utils.py              # Validaciones de consola
├── main.py               # App de consola (modo alternativo)
├── api.py                # API FastAPI original (legacy)
├── test_proyecto.py      # Tests unitarios (unittest)
├── requeriments.txt      # Dependencias del proyecto
├── tareas.json           # Datos de tareas (auto-generado)
├── log_actividad.txt     # Registro de actividad
├── venv/                 # Entorno virtual
└── README.md             # Este archivo
```

---

## 🔌 Endpoints REST

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/` | Página web principal (frontend) |
| `GET` | `/api/tareas` | Listar todas las tareas |
| `GET` | `/api/tareas/{id}` | Obtener una tarea por ID |
| `GET` | `/api/tareas/estadisticas` | Estadísticas del tablero |
| `GET` | `/api/tareas/filtrar` | Filtrar por estado/categoría/responsable |
| `POST` | `/api/tareas` | Crear nueva tarea (body JSON) |
| `PUT` | `/api/tareas/{id}` | Actualizar tarea parcialmente |
| `PUT` | `/api/tareas/{id}/estado` | Cambiar estado de tarea |
| `DELETE` | `/api/tareas/{id}` | Eliminar tarea |

### Modelo de tarea

```json
{
  "id": 1,
  "titulo": "Tarea ejemplo",
  "descripcion": "Descripción detallada",
  "prioridad": 1,
  "estado": "pendiente",
  "categoria": "Backend",
  "responsable": "Ana",
  "fecha_limite": "2026-12-31"
}
```

**Prioridad:** `1: Alta`, `2: Media`, `3: Baja`  
**Estado:** `pendiente`, `en_curso`, `finalizada`

---

## 🖥️ Uso desde consola

El proyecto también incluye un menú interactivo por terminal:

```bash
python main.py
```

Opciones disponibles:
1. Alta / Cargar nueva tarea
2. Consultar y filtrar tareas
3. Modificar estado de tarea
4. Ver estadísticas de productividad
5. Exportar reporte a CSV
6. Iniciar servidor FastAPI
0. Salir

---

## 🧪 Tests

Ejecutar los tests unitarios:

```bash
python -m pytest test_proyecto.py -v
```

Incluye 5 tests que cubren:
- Creación de tareas
- Filtrado por estado
- Cálculo de estadísticas
- Persistencia JSON
- Cambio de estado

---

## 📦 Dependencias

| Paquete | Versión | Descripción |
|---------|---------|-------------|
| `fastapi` | >=0.100.0 | Framework web ASGI |
| `uvicorn[standard]` | >=0.22.0 | Servidor ASGI |
| `pydantic` | >=2.0.0 | Validación de datos |
| `jinja2` | >=3.1.0 | Motor de templates HTML |
| `python-multipart` | >=0.0.6 | Formularios multipart |
| `pytest` | >=7.4.0 | Framework de testing |
| `httpx` | >=0.24.1 | Cliente HTTP para tests |
| `flake8` | >=6.1.0 | Linter de código |
| `black` | >=23.7.0 | Formateador de código |

Instalar todas: `pip install -r requeriments.txt`

---

## 🌐 Despliegue en producción

### Con Uvicorn (recomendado)

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Con Docker

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install -r requeriments.txt
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Con Nginx como reverse proxy

```nginx
server {
    listen 80;
    server_name tu-dominio.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 🎨 Características del Frontend

- **Interfaz Kanban** con tarjetas organizadas por estado
- **Tema oscuro** profesional
- **Diseño responsive** — funciona en móvil, tablet y desktop
- **Filtros** en tiempo real por estado, categoría y responsable
- **Crear, editar, cambiar estado y eliminar** tareas directamente desde el navegador
- **Estadísticas** en tiempo real (total, pendientes, en curso, finalizadas, % completado)
- **Llamadas REST** con `fetch()` y `async/await`
- **Navegación** desde el menú lateral del header

---

## 🔑 Autor

**gconcina** (gconcinalo@gmail.com)  
Tecnicatura Superior en Desarrollo de Software — Programación I (2026)

---

## 📝 Licencia

Proyecto académico integrador — Programación I 2026.
