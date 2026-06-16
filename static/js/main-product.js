import { init } from "./app.js";

init();

// Кількість
// let qty = 1;
// const qtyVal = document.getElementById("qtyVal");
// document.getElementById("qty").addEventListener("click", (e) => {
//   const btn = e.target.closest("[data-q]");
//   if (!btn) return;
//   qty = Math.max(1, qty + Number(btn.getAttribute("data-q")));
//   qtyVal.textContent = qty;
// });

let qty = 1;
const qtyVal = document.getElementById("qtyVal");
const qtyInput = document.getElementById("qtyInput");
document.getElementById("qty").addEventListener("click", (e) => {
  const btn = e.target.closest("[data-q]");
  if (!btn) return;
  qty = Math.max(1, qty + Number(btn.getAttribute("data-q")));
  qtyVal.textContent = qty;
  qtyInput.value = qty;
});

// Галерея — перемикання активної мініатюри
document.querySelectorAll(".pdp__thumb").forEach((thumb) => {
  thumb.addEventListener("click", () => {
    const mainImg = document.querySelector(".pdp__main img");
    const src = thumb.querySelector("img").getAttribute("src");
    mainImg.setAttribute("src", src);
    document
      .querySelectorAll(".pdp__thumb")
      .forEach((t) => t.classList.remove("is-active"));
    thumb.classList.add("is-active");
  });
});

// Акордеон
document.getElementById("accordion").addEventListener("click", (e) => {
  const head = e.target.closest(".accordion__head");
  if (!head) return;
  head.parentElement.classList.toggle("is-open");
});
