// ============================================
// Trello Clon - Frontend JavaScript
// ============================================

const API_BASE = '/api';

// ---- Utility Functions ----

function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast ${type} show`;
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

async function fetchJSON(url, options = {}) {
    try {
        const response = await fetch(url, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers,
            },
            ...options,
        });
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.detail || data.mensaje || 'Error en la petición');
        }
        return data;
    } catch (error) {
        showToast(error.message || 'Error de conexión', 'error');
        throw error;
    }
}

// ---- Load Functions ----

async function loadTasks() {
    const estado = document.getElementById('filterEstado')?.value || '';
    const categoria = document.getElementById('filterCategoria')?.value || '';
    const responsable = document.getElementById('filterResponsable')?.value || '';

    try {
        const params = new URLSearchParams();
        if (estado) params.set('estado', estado);
        if (categoria) params.set('categoria', categoria);
        if (responsable) params.set('responsable', responsable);

        const data = await fetchJSON(`${API_BASE}/tareas?${params}`);
        renderTasks(data);
        loadStats();
    } catch (error) {
        console.error('Error cargando tareas:', error);
    }
}

async function loadStats() {
    try {
        const data = await fetchJSON(`${API_BASE}/tareas/estadisticas`);
        document.getElementById('totalTasks').textContent = data.total_tareas;
        document.getElementById('pendingTasks').textContent = data.pendientes;
        document.getElementById('inProgressTasks').textContent = data.en_curso;
        document.getElementById('completedTasks').textContent = data.finalizadas;
        document.getElementById('progressBar').style.width = `${data.porcentaje_completadas}%`;
        document.getElementById('progressText').textContent = `${data.porcentaje_completadas}% completadas`;
    } catch (error) {
        console.error('Error cargando estadísticas:', error);
    }
}

async function loadCategories() {
    try {
        const data = await fetchJSON(`${API_BASE}/tareas`);
        const categories = [...new Set(data.map(t => t.categoria))];
        const select = document.getElementById('filterCategoria');
        const currentValue = select.value;
        select.innerHTML = '<option value="">Todas las categorías</option>';
        categories.forEach(cat => {
            const option = document.createElement('option');
            option.value = cat;
            option.textContent = cat;
            select.appendChild(option);
        });
        if (categories.includes(currentValue)) {
            select.value = currentValue;
        }
    } catch (error) {
        console.error('Error cargando categorías:', error);
    }
}

// ---- Render Functions ----

function renderTasks(tareas) {
    const grid = document.getElementById('tasksGrid');
    grid.innerHTML = '';

    if (!tareas || tareas.length === 0) {
        grid.innerHTML = '<div class="empty-state"><p>📭 No hay tareas para mostrar.</p></div>';
        return;
    }

    // Sort by priority (1 first)
    const sorted = [...tareas].sort((a, b) => a.prioridad - b.prioridad);

    sorted.forEach(tarea => {
        const card = document.createElement('div');
        card.className = 'task-card';
        card.innerHTML = `
            <div class="task-header">
                <span class="task-title">${escapeHTML(tarea.titulo)}</span>
                <span class="task-id">#${tarea.id}</span>
            </div>
            <div class="task-description">${escapeHTML(tarea.descripcion)}</div>
            <div class="task-meta">
                <div class="task-meta-item">
                    <span class="label">Prioridad</span>
                    <span class="value"><span class="priority-badge prioridad-${tarea.prioridad}">${getPriorityLabel(tarea.prioridad)}</span></span>
                </div>
                <div class="task-meta-item">
                    <span class="label">Estado</span>
                    <span class="value"><span class="status-badge ${tarea.estado}">${getStatusLabel(tarea.estado)}</span></span>
                </div>
                <div class="task-meta-item">
                    <span class="label">Categoría</span>
                    <span class="value">${escapeHTML(tarea.categoria)}</span>
                </div>
                <div class="task-meta-item">
                    <span class="label">Responsable</span>
                    <span class="value">${escapeHTML(tarea.responsable)}</span>
                </div>
            </div>
            <div class="task-footer">
                <div class="task-actions">
                    ${renderStateButtons(tarea)}
                    <button class="btn-delete" onclick="deleteTask(${tarea.id})">Eliminar</button>
                </div>
            </div>
        `;
        grid.appendChild(card);
    });
}

function renderStateButtons(tarea) {
    const states = ['pendiente', 'en_curso', 'finalizada'];
    const buttons = states.map(state => {
        const active = tarea.estado === state;
        const opacity = active ? '1' : '0.5';
        return `<button class="btn-state ${state}" onclick="changeState(${tarea.id}, '${state}')" style="opacity: ${opacity}; ${active ? 'font-style: italic;' : ''}">${getStatusLabel(state)}</button>`;
    });
    return buttons.join('');
}

// ---- Action Functions ----

async function createTask(e) {
    e.preventDefault();

    const taskData = {
        titulo: document.getElementById('formTitulo').value.trim(),
        descripcion: document.getElementById('formDescripcion').value.trim(),
        prioridad: parseInt(document.getElementById('formPrioridad').value),
        categoria: document.getElementById('formCategoria').value.trim(),
        responsable: document.getElementById('formResponsable').value.trim(),
        fecha_limite: document.getElementById('formFechaLimite').value.trim(),
    };

    try {
        await fetchJSON(`${API_BASE}/tareas`, {
            method: 'POST',
            body: JSON.stringify(taskData),
        });
        showToast('Tarea creada con éxito', 'success');
        document.getElementById('taskForm').reset();
        document.getElementById('formSection').style.display = 'none';
        loadTasks();
        loadCategories();
    } catch (error) {
        // Error already shown by showToast
    }
}

async function changeState(id, nuevoEstado) {
    try {
        await fetchJSON(`${API_BASE}/tareas/${id}/estado`, {
            method: 'PUT',
            body: JSON.stringify({ nuevo_estado: nuevoEstado }),
        });
        showToast(`Estado cambiado a ${getStatusLabel(nuevoEstado)}`, 'success');
        loadTasks();
    } catch (error) {
        // Error already shown
    }
}

async function deleteTask(id) {
    if (!confirm('¿Seguro que deseas eliminar esta tarea?')) return;
    try {
        await fetchJSON(`${API_BASE}/tareas/${id}`, { method: 'DELETE' });
        showToast('Tarea eliminada con éxito', 'success');
        loadTasks();
        loadCategories();
    } catch (error) {
        // Error already shown
    }
}

// ---- Form Toggle ----

function toggleForm() {
    const formSection = document.getElementById('formSection');
    const isVisible = formSection.style.display !== 'none';
    formSection.style.display = isVisible ? 'none' : 'block';
    if (!isVisible) {
        document.getElementById('formTitulo').focus();
    }
}

// ---- Helpers ----

function escapeHTML(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

function getPriorityLabel(prioridad) {
    const labels = { 1: 'Alta', 2: 'Media', 3: 'Baja' };
    return labels[prioridad] || `(${prioridad})`;
}

function getStatusLabel(estado) {
    const labels = { pendiente: 'Pendiente', en_curso: 'En Curso', finalizada: 'Finalizada' };
    return labels[estado] || estado;
}

// ---- Event Listeners ----

document.addEventListener('DOMContentLoaded', () => {
    // Load initial data
    loadTasks();
    loadCategories();

    // Form toggle
    document.getElementById('toggleFormBtn').addEventListener('click', toggleForm);
    document.getElementById('cancelFormBtn').addEventListener('click', toggleForm);

    // Form submission
    document.getElementById('taskForm').addEventListener('submit', createTask);

    // Filter buttons
    document.getElementById('applyFilters').addEventListener('click', loadTasks);
    document.getElementById('resetFilters').addEventListener('click', () => {
        document.getElementById('filterEstado').value = '';
        document.getElementById('filterCategoria').value = '';
        document.getElementById('filterResponsable').value = '';
        loadTasks();
    });

    // Real-time filter on Enter key
    document.getElementById('filterResponsable').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') loadTasks();
    });
});
