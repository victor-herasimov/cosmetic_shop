import { init, phoneNumberMask, closeModal } from "./app.js";
init();

window.phoneNumberMask = phoneNumberMask;

document.addEventListener("htmx:load", (event) => {
  const target = event.detail.elt;
  const phoneInput = target.querySelector
    ? target.querySelector("#id_phone")
    : null;
  if (phoneInput) {
    phoneNumberMask("#id_phone", "{+38 (\\0}00) 000-00-00", target);
  }
});

document.addEventListener("successFeedback", () => {
  const successModal = document.getElementById("successModal");
  if (successModal) {
    closeModal(successModal);
  }
});
