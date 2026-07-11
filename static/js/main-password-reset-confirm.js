import { init } from "./app.js";
init();

document.addEventListener("password_reset_confirm_success", () => {
  setTimeout(function () {
    window.location.href = "/";
  }, 5000);
});
