import { init, phoneNumberMask } from "./app.js";
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
document.addEventListener("htmx:load", (event) => {
  const target = event.detail.elt;
  const phoneInput = target.querySelector
    ? target.querySelector("#phone_change")
    : null;
  console.log(phoneInput);
  if (phoneInput) {
    phoneNumberMask("#phone_change", "{+38 (\\0}00) 000-00-00", target);
  }
});
