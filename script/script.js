document.addEventListener("DOMContentLoaded", () => {
  const loginForm = document.getElementById("login-form");
  const userInput = document.getElementById("user_name");
  const passwordInput = document.getElementById("password");
  const loginMessage = document.getElementById("login-message");

  loginForm.addEventListener("submit", (event) => {
    event.preventDefault();

    const userName = userInput.value.trim();
    const password = passwordInput.value.trim();

    loginMessage.textContent = "";
    loginMessage.style.color = "";

    if (!userName || !password) {
      loginMessage.textContent = "Debes introducir usuario y contraseña.";
      loginMessage.style.color = "red";
      return;
    }

    if (userName === "admin" && password === "1234") {
      loginMessage.textContent = "Inicio de sesión correcto. Redirigiendo...";
      loginMessage.style.color = "green";

      setTimeout(() => {
        window.location.href = "formularios.html";
      }, 1000);
    } else {
      loginMessage.textContent = "Usuario o contraseña incorrectos.";
      loginMessage.style.color = "red";
    }
  });
});