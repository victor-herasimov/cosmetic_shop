import { init } from "./app.js";

init();

// Маска для номера телефону
function phoneNumberMask(selector, mask, parent = document) {
  const element = parent.querySelector(selector);
  if (!element) return;
  const maskOptions = {
    mask: mask,
  };
  IMask(element, maskOptions);
}

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
