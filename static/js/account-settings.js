import { init } from "./app.js";
init();

function passwordVisibilityToggles() {
  document.querySelectorAll(".sform-toggle-pass").forEach((btn) => {
    btn.addEventListener("click", () => {
      const targetId = btn.dataset.target;
      const input = document.getElementById(targetId);
      const eyeOpen = btn.querySelector(".eye-open");
      const eyeClosed = btn.querySelector(".eye-closed");

      if (input.type === "password") {
        input.type = "text";
        eyeOpen.style.display = "none";
        eyeClosed.style.display = "";
      } else {
        input.type = "password";
        eyeOpen.style.display = "";
        eyeClosed.style.display = "none";
      }
    });
  });
}

passwordVisibilityToggles();
