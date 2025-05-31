document.addEventListener("DOMContentLoaded", function () {
    const hoy = new Date().toISOString().split("T")[0];
    const fechaInicio = document.querySelector('input[name="fecha_inicio"]');
    const fechaFin = document.querySelector('input[name="fecha_fin"]');
    const form = document.querySelector("form");

    fechaInicio.max = hoy;
    fechaFin.max = hoy;

    const errorInicio = document.createElement("div");
    const errorFin = document.createElement("div");

    errorInicio.className = "text-danger small";
    errorFin.className = "text-danger small";

    fechaInicio.parentNode.appendChild(errorInicio);
    fechaFin.parentNode.appendChild(errorFin);

    function validarFechas() {
        const valInicio = fechaInicio.value;
        const valFin = fechaFin.value;

        let esValido = true;

        errorInicio.textContent = "";
        errorFin.textContent = "";

        // Convertir a objeto Date para comparar
        const fechaI = new Date(valInicio);
        const fechaF = new Date(valFin);

        if (valInicio > hoy) {
            errorInicio.textContent = "La fecha de inicio no puede ser mayor a hoy.";
            esValido = false;
        }

        if (valFin > hoy) {
            errorFin.textContent = "La fecha de fin no puede ser mayor a hoy.";
            esValido = false;
        }

        if (valInicio && valFin) {
            if (valInicio > valFin) {
                errorInicio.textContent = "La fecha de inicio no puede ser posterior a la fecha de fin.";
                esValido = false;
            } else if (valInicio === valFin) {
                errorInicio.textContent = "Las fechas no pueden ser iguales.";
                esValido = false;
            } else {
                const diffDias = (fechaF - fechaI) / (1000 * 60 * 60 * 24);
                if (diffDias < 1) {
                    errorInicio.textContent = "Debe haber al menos 1 día de diferencia.";
                    esValido = false;
                }
            }
        }

        return esValido;
    }

    fechaInicio.addEventListener("input", validarFechas);
    fechaFin.addEventListener("input", validarFechas);

    form.addEventListener("submit", function (e) {
        if (!validarFechas()) {
            e.preventDefault();
        }
    });
});
