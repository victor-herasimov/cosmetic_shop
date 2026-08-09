import { init } from "./app.js";

init();

let qty;
const qtyVal = document.getElementById("qtyVal");
const qtyInput = document.getElementById("qtyInput");
document.getElementById("qty").addEventListener("click", (e) => {
  qty = Number(qtyVal.innerHTML);
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

// Відгуки
const writeReviewBtn = document.getElementById("writeReviewBtn");
const reviewFormContainer = document.getElementById("reviewFormContainer");

writeReviewBtn.addEventListener("click", () => {
  reviewFormContainer.classList.toggle("is-open");
  if (reviewFormContainer.classList.contains("is-open")) {
    writeReviewBtn.innerHTML = `
        <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 6px;"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
        Скасувати
      `;
    writeReviewBtn.classList.replace("btn--primary", "btn--ghost");
    setTimeout(() => {
      reviewFormContainer.scrollIntoView({
        behavior: "smooth",
        block: "nearest",
      });
    }, 300);
  } else {
    writeReviewBtn.innerHTML = `
        <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 6px;"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 1 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>
        Написати відгук
      `;
    writeReviewBtn.classList.replace("btn--ghost", "btn--primary");
  }
});
