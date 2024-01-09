// FUNCION PARA ENTRADA DE TEXTO, DE ACUERDO A LO SELECCIONADO POR USUARIO
function insertarTexto(valor) {
    // Obtén el input de tipo texto
    var input = document.getElementById('mensaje');

    // Determina el texto a insertar según el botón presionado
    var textoInsertar = `{${valor}}`;

    // Inserta el texto en el input en la posición del cursor
    if (document.selection) {
        // Para navegadores antiguos como IE
        input.focus();
        var sel = document.selection.createRange();
        sel.text = textoInsertar;
    } else if (input.selectionStart || input.selectionStart === 0) {
        // Para navegadores modernos
        var startPos = input.selectionStart;
        var endPos = input.selectionEnd;
        input.value = input.value.substring(0, startPos) + textoInsertar + input.value.substring(endPos, input.value.length);
        input.setSelectionRange(startPos + textoInsertar.length, startPos + textoInsertar.length);
    } else {
        // Si no se puede determinar la posición del cursor, simplemente añade al final
        input.value += textoInsertar;
    }
}