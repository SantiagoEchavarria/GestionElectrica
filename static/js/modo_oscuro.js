document.addEventListener("DOMContentLoaded", function () {
    const btn = document.getElementById("modoOscuroBtn");
    const body = document.body;

    // Aplicar el modo oscuro si estaba activado antes
    if (localStorage.getItem("modoOscuro") === "activado") {
        body.classList.add("modo-oscuro");
        btn.innerText = "☀️";
    }

    btn.addEventListener("click", () => {
        body.classList.toggle("modo-oscuro");

        if (body.classList.contains("modo-oscuro")) {
            localStorage.setItem("modoOscuro", "activado");
            btn.innerText = "☀️";  
        } else {
            localStorage.setItem("modoOscuro", "desactivado");
            btn.innerText = "🌙";  
        }
    });
});