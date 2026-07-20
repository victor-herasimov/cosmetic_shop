import { init } from "./app.js";

document.addEventListener("DOMContentLoaded", () => {
  init();
  document.querySelectorAll(".accordion-header").forEach((header) => {
    header.addEventListener("click", (e) => {
      e.preventDefault();
      header.parentElement.classList.toggle("is-collapsed");
    });
  });
});
