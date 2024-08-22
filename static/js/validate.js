
document.addEventListener("DOMContentLoaded", function() {
    
    const form = document.getElementById("exampleForm");

    // Escucha el evento de envío del formulario
    form.addEventListener("submit", function(event) {
        // Evitamos que el formulario se envíe automáticamente
        event.preventDefault();

        // Llama a la función de validación
        if (validateForm()) {
            form.submit(); // Si es válido, envía el formulario
        }
    });

    // Función de validación
    function validateForm() {
        // Obtenemos los campos del formulario
        const name = document.getElementById("name").value;
        const message = document.getElementById("message").value;

        // Verifica que el campo nombre no esté vacío
        if (name.trim() === "") {
            alert("Por favor, ingresa el titulo");
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

    document.getElementById('datetime').addEventListener('input', function() {
        const inputDate = new Date(this.value);
        const currentDate = new Date();
    
        if (inputDate < currentDate) {
          alert("No puedes seleccionar una fecha anterior a la actual.");
          this.value = ""; // Limpiar el valor si la fecha es anterior a la actual
        }
      });

  
 
});

