document.addEventListener("DOMContentLoaded", () => {
  const loginForm = document.getElementById("login-form");
  const userInput = document.getElementById("user_name");
  const passwordInput = document.getElementById("password");
  const loginMessage = document.getElementById("login-message");
  const submitButton = loginForm?.querySelector('input[type="submit"]');

  if (!loginForm || !userInput || !passwordInput || !loginMessage) {
    return;
  }

  loginForm.addEventListener("submit", (event) => {
    event.preventDefault();

    const userName = userInput.value.trim();
    const password = passwordInput.value.trim();

    loginMessage.textContent = "";
    loginMessage.className = "";

    if (!userName || !password) {
      loginMessage.textContent = "Debes introducir usuario y contraseña.";
      loginMessage.classList.add("error");
      return;
    }

    if (userName === "admin" && password === "1234") {
      loginMessage.textContent = "Inicio de sesión correcto. Redirigiendo...";
      loginMessage.classList.add("success");

      if (submitButton) {
        submitButton.disabled = true;
        submitButton.value = "Entrando...";
      }

      setTimeout(() => {
        window.location.href = "formularios.html";
      }, 1000);
    } else {
      loginMessage.textContent = "Usuario o contraseña incorrectos.";
      loginMessage.classList.add("error");
    }
  });
});