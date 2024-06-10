$(document).ready(function() {
    // Obtiene el nombre y dirección del cliente al cargar la página
    $.ajax({
        url: "/obtener_informacion_cliente", // Ruta de la función Python para obtener la información del cliente
        type: "GET",
        success: function(data) {
            $("#nombre").val(data.nombre);
            $("#direccion").val(data.direccion);
        }
    });

    // Valida el método de pago antes de enviar el formulario
    $("#paymentForm").submit(function(event) {
        var metodoPago = $("#metodo_pago").val();
        if (metodoPago !== "tarjeta_credito" && metodoPago !== "tarjeta_debito" && metodoPago !== "orden_compra") {
            alert("Por favor seleccione un método de pago válido.");
            event.preventDefault();
        }
    });
});
