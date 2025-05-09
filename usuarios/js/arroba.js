document.addEventListener("DOMContentLoaded", function () {
    const usernameInput = document.getElementById("username");
    const errorDisplay = document.getElementById("usernameError");

    usernameInput.addEventListener("blur", function () {
        const value = usernameInput.value;
        if (value && !value.includes("@")) {
            errorDisplay.textContent = "El nombre de usuario debe contener un '@'";
        } else {
            errorDisplay.textContent = "";
        }
    });
});