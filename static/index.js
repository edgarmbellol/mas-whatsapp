function enableSubmit() {
    var archivoCarga = document.getElementById('archivoCarga');
    var enviarBoton = document.getElementById('enviarBoton');

    // Habilitar el botón de enviar si se selecciona un archivo
    enviarBoton.disabled = !archivoCarga.value;
}

