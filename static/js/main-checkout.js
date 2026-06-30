import { init, phoneNumberMask } from "./app.js";

init();

window.phoneNumberMask = phoneNumberMask;

document.addEventListener("DOMContentLoaded", () => {
  phoneNumberMask("#id_phone", "{+38 (\\0}00) 000-00-00");

  const checkoutMain = document.getElementById("checkoutMain");
  if (checkoutMain) {
    checkoutMain.addEventListener("htmx:afterRequest", () => {
      // Шукаємо інпут всередині нашого контейнера
      phoneNumberMask("#id_phone", "{+38 (\\0}00) 000-00-00", checkoutMain);
    });
  }
});
