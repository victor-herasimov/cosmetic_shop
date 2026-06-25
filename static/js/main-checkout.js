import { init } from "./app.js";

init();

// Маска для номера телефону
function phoneNumberMask(selector, mask) {
  const element = document.querySelector(selector);
  if (!element) return;
  const maskOptions = {
    mask: mask,
  };
  const phone_mask = IMask(element, maskOptions);
}

phoneNumberMask("#id_phone", "{+38 (\\0}00) 000-00-00");
