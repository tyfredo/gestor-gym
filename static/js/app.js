document.addEventListener('DOMContentLoaded', () => {
    
    // --- LÓGICA PANEL ADMIN ---
    const formAdmin = document.getElementById('formAdmin');
    
    formAdmin.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Armamos el paquete de datos a enviar al servidor
        const datos = {
            id: document.getElementById('adminId').value,
            nombre: document.getElementById('adminNombre').value,
            fecha: document.getElementById('adminFecha').value
        };

        try {
            // Enviamos los datos a Python mediante método POST
            const respuesta = await fetch('/api/guardar', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(datos)
            });
            
            const resultado = await respuesta.json();
            
            if (resultado.success) {
                alert(`Socio ${datos.id} guardado correctamente en la base de datos.`);
                formAdmin.reset();
                document.getElementById('resultadoConsulta').classList.add('d-none');
            }
        } catch (error) {
            console.error("Error al guardar:", error);
            alert("Error al conectar con el servidor.");
        }
    });

    // --- LÓGICA CONSULTA RÁPIDA ---
    const formConsulta = document.getElementById('formConsulta');
    const contenedorRes = document.getElementById('resultadoConsulta');
    const alerta = document.getElementById('alertaEstatus');
    const btnRenovar = document.getElementById('btnRenovar');

    let socioActual = null; 

    formConsulta.addEventListener('submit', async (e) => {
        e.preventDefault();
        const id = document.getElementById('consultaId').value;
        
        try {
            // Consultamos a Python mediante el método GET
            const respuesta = await fetch(`/api/consultar/${id}`);
            
            if (!respuesta.ok) {
                alert("El ID ingresado no está registrado en el sistema SQLite.");
                contenedorRes.classList.add('d-none');
                return;
            }

            // Recibimos el cálculo ya procesado por Python
            const reporte = await respuesta.json();
            
            socioActual = { id: id, nombre: reporte.nombre };

            document.getElementById('resNombre').textContent = reporte.nombre;
            document.getElementById('resMensaje').textContent = reporte.mensaje;
            alerta.className = `alert shadow-sm alert-${reporte.estadoBootstrap}`;
            contenedorRes.classList.remove('d-none');

            // Mostrar botón de renovación SOLO si está vencido
            if (reporte.estadoBootstrap === "danger") {
                btnRenovar.classList.remove('d-none');
            } else {
                btnRenovar.classList.add('d-none');
            }
            
        } catch (error) {
            console.error("Error en consulta:", error);
        }
    });

    // --- LÓGICA BOTÓN "AGREGAR NUEVO PAGO" ---
    btnRenovar.addEventListener('click', () => {
        if (socioActual) {
            document.getElementById('adminId').value = socioActual.id;
            document.getElementById('adminNombre').value = socioActual.nombre;
            
            const hoy = new Date();
            const anio = hoy.getFullYear();
            const mes = String(hoy.getMonth() + 1).padStart(2, '0'); 
            const dia = String(hoy.getDate()).padStart(2, '0');
            
            document.getElementById('adminFecha').value = `${anio}-${mes}-${dia}`;
            document.getElementById('formAdmin').scrollIntoView({ behavior: 'smooth' });
        }
    });
});