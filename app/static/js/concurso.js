// Mensaje para confirmar en consola que el archivo cargó
console.log("¡Cerebro del concurso (JS) activado!");

// 1. ABRIR MODAL (Para Crear o Editar)
async function abrirModal(id = null) {
    const modal = document.getElementById('modalConcurso');
    const form = document.getElementById('formConcurso');
    const title = document.getElementById('modalTitle');
    
    if (!modal || !form) return; // Seguridad

    form.reset(); 
    document.getElementById('concursoId').value = id || '';

    if (id) {
        title.innerText = "Editar Concurso";
        try {
            // Buscamos los datos en tu nueva ruta de Python
            const response = await fetch(`/admin/api/concursos/${id}`);
            if (!response.ok) throw new Error("No se pudo obtener el concurso");
            
            const data = await response.json();
            
            // Rellenamos los campos con lo que viene de MongoDB
            document.getElementById('titulo').value = data.titulo || '';
            document.getElementById('descripcion').value = data.descripcion || '';
            document.getElementById('estado').value = data.estado || 'activo';
        } catch (error) {
            console.error("Error al cargar datos:", error);
            alert("No se pudieron cargar los datos del concurso");
        }
    } else {
        title.innerText = "Nuevo Concurso";
    }
    modal.style.display = 'flex';
}

// 2. CERRAR MODAL
function cerrarModal() {
    document.getElementById('modalConcurso').style.display = 'none';
}

// 3. GUARDAR DATOS (IMPORTANTE: Espera a que el HTML esté listo)
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('formConcurso');
    
    if (form) {
        form.onsubmit = async (e) => {
            e.preventDefault();
            console.log("Intentando guardar...");

            const formData = new FormData(form);
            
            try {
                const response = await fetch('/admin/api/concursos/guardar', {
                    method: 'POST',
                    body: formData
                });

                if (response.ok) {
                    console.log("¡Guardado con éxito!");
                    window.location.reload(); // Refresca la tabla para ver los cambios
                } else {
                    const errorData = await response.json();
                    alert("Error: " + (errorData.message || "No se pudo guardar"));
                }
            } catch (error) {
                console.error("Error en la petición:", error);
                alert("Error de conexión con el servidor");
            }
        };
    }
});


// 4. ELIMINAR CONCURSO
async function eliminarConcurso(id) {
    // Pedimos confirmación al usuario
    if (!confirm('¿Estás seguro de que deseas eliminar este concurso?')) {
        return; 
    }

    try {
        // Llamamos a la ruta que creamos en Python
        const response = await fetch(`/admin/api/concursos/eliminar/${id}`, {
            method: 'POST' // Usamos POST para que coincida con la ruta de Python
        });

        if (response.ok) {
            console.log("Eliminado con éxito");
            window.location.reload(); // Recargamos para que desaparezca de la tabla
        } else {
            const errorData = await response.json();
            alert("Error: " + (errorData.message || "No se pudo eliminar"));
        }
    } catch (error) {
        console.error("Error al eliminar:", error);
        alert("Error de conexión");
    }
}

// 5. FILTRAR CONCURSOS POR ESTADO
function filtrarConcursos() {
    const filtro = document.getElementById('filtroEstado').value.toLowerCase();
    const filas = document.querySelectorAll('.fila-concurso');

    filas.forEach(fila => {
        const estadoConcurso = fila.getAttribute('data-estado');
        
        // Si el filtro está vacío ("Todos") o coincide con el estado de la fila
        if (filtro === "" || estadoConcurso === filtro) {
            fila.style.display = ""; // Muestra la fila
        } else {
            fila.style.display = "none"; // Oculta la fila
        }
    });
}