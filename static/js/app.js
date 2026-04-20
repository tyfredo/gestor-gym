document.addEventListener('DOMContentLoaded', () => {
    const btnOpenSearch = document.getElementById('btnOpenSearch');
    const btnCloseSearch = document.getElementById('btnCloseSearch');
    const searchOverlay = document.getElementById('searchOverlay');
    const consultaInput = document.getElementById('consultaId');

    const openSearch = () => {
        searchOverlay.style.display = 'flex';
        setTimeout(() => consultaInput.focus(), 100);
    };

    const closeSearch = () => {
        searchOverlay.style.display = 'none';
        document.getElementById('searchPlaceholder').classList.remove('d-none');
        document.getElementById('resultadoConsulta').classList.add('d-none');
        consultaInput.value = '';
    };

    btnOpenSearch.addEventListener('click', openSearch);
    btnCloseSearch.addEventListener('click', closeSearch);

    document.addEventListener('keydown', (e) => {
        if (e.key === "Escape") closeSearch();
    });

    const formAdmin = document.getElementById('formAdmin');
    formAdmin.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Aquí agregamos la captura de la membresía elegida
        const datos = {
            id: document.getElementById('adminId').value,
            nombre: document.getElementById('adminNombre').value,
            id_membresia: document.getElementById('adminMembresia').value,
            fecha: document.getElementById('adminFecha').value,
            id_recepcionista: document.getElementById('adminRecepcionista').value
        };

        const res = await fetch('/api/guardar', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(datos)
        });
        
        if (res.ok) {
            alert("✅ Registro actualizado con éxito.");
            formAdmin.reset();
        } else {
            alert("❌ Ocurrió un error al guardar.");
        }
    });

    const formConsulta = document.getElementById('formConsulta');
    formConsulta.addEventListener('submit', async (e) => {
        e.preventDefault();
        const id = consultaInput.value.toUpperCase();
        
        try {
            const res = await fetch(`/api/consultar/${id}`);

            if (res.ok) {
                const reporte = await res.json();
                
                document.getElementById('searchPlaceholder').classList.add('d-none');
                const resultadoDiv = document.getElementById('resultadoConsulta');
                resultadoDiv.classList.remove('d-none');

                document.getElementById('resNombre').textContent = reporte.nombre;
                document.getElementById('resMensaje').textContent = reporte.mensaje;
                document.getElementById('resAvatar').src = `https://i.pravatar.cc/150?u=${id}`;

                const badge = document.getElementById('resBadge');
                const actionBox = document.getElementById('actionBox');

                if(reporte.estadoBootstrap === "danger") {
                    badge.style.backgroundColor = "#dc3545";
                    actionBox.classList.remove('d-none');
                } else {
                    badge.style.backgroundColor = "#198754";
                    actionBox.classList.add('d-none');
                }

                document.getElementById('btnRenovar').onclick = () => {
                    closeSearch();
                    document.getElementById('adminId').value = id;
                    document.getElementById('adminNombre').value = reporte.nombre;
                    document.getElementById('adminFecha').value = new Date().toISOString().split('T')[0];
                };

            } else {
                alert("Socio no encontrado.");
            }
        } catch (error) {
            console.error(error);
        }
    });
});