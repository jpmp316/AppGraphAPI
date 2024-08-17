// Espera a que el DOM esté completamente cargado
document.addEventListener("DOMContentLoaded", function() {
    // Obtén el formulario
    const form = document.getElementById("exampleForm");

    // Escucha el evento de envío del formulario
    form.addEventListener("submit", function(event) {
        // Evita que el formulario se envíe automáticamente
        event.preventDefault();

        // Llama a la función de validación
        if (validateForm()) {
            form.submit(); // Si es válido, envía el formulario
        }
    });

    // Función de validación
    function validateForm() {
        // Obtén los campos del formulario
        const name = document.getElementById("name").value;
        const message = document.getElementById("message").value;

        // Verifica que el campo nombre no esté vacío
        if (name.trim() === "") {
            alert("Por favor, ingresa tu nombre.");
            return false;
        }

        // Verifica que el mensaje no esté vacío
        if (message.trim() === "") {
            alert("Por favor, ingresa un mensaje.");
            return false;
        }

        // Si todas las validaciones pasan, devuelve true
        return true;
    }

  
 
});

