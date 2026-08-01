import { init, scrollToElement } from "./app.js";

document.addEventListener("htmx:load", (event) => {
  init();
});

document.addEventListener("htmx:afterSwap", (event) => {
  console.log(event.detail.target);
  if (event.detail.target.id === "products") {
    scrollToElement("search-head-wrapper");
  }
});
