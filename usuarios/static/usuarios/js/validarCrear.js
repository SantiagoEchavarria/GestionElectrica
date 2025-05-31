 document.addEventListener("DOMContentLoaded", function () {
        const nombre = document.getElementById("id_nombre");
        const email = document.getElementById("id_email");
        const telefono = document.getElementById("id_telefono");
        const fecha = document.getElementById("id_fecha_nacimiento");
        const password1 = document.getElementById("id_password1");
        const password2 = document.getElementById("id_password2");

        function showError(input, message) {
            document.getElementById("error_" + input.id.split("id_")[1]).textContent = message;
        }

        function clearError(input) {
            document.getElementById("error_" + input.id.split("id_")[1]).textContent = "";
        }

        // Función para validar fortaleza de contraseña
        function validarFortalezaContrasena(contrasena) {
            const tieneMinuscula = /[a-z]/.test(contrasena);
            const tieneMayuscula = /[A-Z]/.test(contrasena);
            const tieneNumero = /[0-9]/.test(contrasena);
            const tieneEspecial = /[^a-zA-Z0-9]/.test(contrasena);
            
            return tieneMinuscula && tieneMayuscula && tieneNumero && tieneEspecial;
        }

        // Función para validar ambas contraseñas
        function validarContrasenas() {
            // Validar primera contraseña
            if (password1.value.length < 8) {
                showError(password1, "La contraseña debe tener al menos 8 caracteres.");
            } else if (!validarFortalezaContrasena(password1.value)) {
                showError(password1, "Debe incluir mayúsculas, minúsculas, números y símbolos.");
            } else {
                clearError(password1);
            }

            // Validar coincidencia (solo si hay algo en password2)
            if (password2.value.length > 0) {
                if (password2.value !== password1.value) {
                    showError(password2, "Las contraseñas no coinciden.");
                } else {
                    clearError(password2);
                }
            }
        }

        // Event listeners para las contraseñas
        password1.addEventListener("blur", validarContrasenas);
        password2.addEventListener("blur", validarContrasenas);
        // Validar mientras se escribe
        password1.addEventListener("input", validarContrasenas);
        password2.addEventListener("input", validarContrasenas);

        nombre.addEventListener("blur", () => {
            if (nombre.value.trim().length === 0) {
                showError(nombre, "El nombre es obligatorio.");
            } else {
                clearError(nombre);
            }
        });

        email.addEventListener("blur", () => {
            if (!email.value.includes("@")) {
                showError(email, "Debe ingresar un correo válido.");
            } else {
                clearError(email);
            }
        });

        telefono.addEventListener("blur", () => {
            if (!/^\d+$/.test(telefono.value)) {
                showError(telefono, "El teléfono solo debe contener números.");
            } else {
                clearError(telefono);
            }
        });

        fecha.addEventListener("blur", () => {
            if (!fecha.value) {
                showError(fecha, "Debe seleccionar una fecha.");
                return;
            }
            
            if (!/^\d{4}-\d{2}-\d{2}$/.test(fecha.value)) {
                showError(fecha, "Formato de fecha inválido. Use YYYY-MM-DD.");
                return;
            }
            
            const fechaIngresada = new Date(fecha.value);
            const hoy = new Date();
            hoy.setHours(0, 0, 0, 0);
        
            if (isNaN(fechaIngresada.getTime())) {
                showError(fecha, "Fecha inválida.");
                return;
            }
        
            if (fechaIngresada >= hoy) {
                showError(fecha, "La fecha debe ser anterior a hoy.");
            } else {
                clearError(fecha);
            }
        });
    });