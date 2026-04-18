document.addEventListener('DOMContentLoaded', () => {
    const formAdmin = document.getElementById('formAdmin');
    const formConsulta = document.getElementById('formConsulta');

    // GUARDAR PAGO
    formAdmin.addEventListener('submit', async (e) => {
        e.preventDefault();
        const datos = {
            id: document.getElementById('adminId').value,
            nombre: document.getElementById('adminNombre').value,
            fecha: document.getElementById('adminFecha').value,
            id_recepcionista: document.getElementById('adminRecepcionista').value
        };

        const res = await fetch('/api/guardar', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(datos)
        });
        
        if (res.ok) {
            alert("Pago registrado correctamente");
            formAdmin.reset();
        }
    });

    // CONSULTAR SOCIO
    formConsulta.addEventListener('submit', async (e) => {
        e.preventDefault();
        const id = document.getElementById('consultaId').value;
        const res = await fetch(`/api/consultar/${id}`);

        if (res.ok) {
            const reporte = await res.json();
            document.getElementById('resNombre').textContent = reporte.nombre;
            document.getElementById('resMensaje').textContent = reporte.mensaje;
            document.getElementById('alertaEstatus').className = `alert shadow-sm alert-${reporte.estadoBootstrap}`;
            document.getElementById('resultadoConsulta').classList.remove('d-none');
            
            const btn = document.getElementById('btnRenovar');
            if(reporte.estadoBootstrap === "danger") {
                btn.classList.remove('d-none');
                btn.onclick = () => {
                    document.getElementById('adminId').value = id;
                    document.getElementById('adminNombre').value = reporte.nombre;
                    document.getElementById('adminFecha').value = new Date().toISOString().split('T')[0];
                };
            } else {
                btn.classList.add('d-none');
            }
        } else {
            alert("Socio no encontrado");
        }
    });
});