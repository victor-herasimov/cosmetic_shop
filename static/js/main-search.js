import { init, scrollToElement } from "./app.js";

document.addEventListener("htmx:load", (event) => {
  init();
  const target = event.detail.elt;
  if (target.id === "catalogGrid") {
    scrollToElement("pagination", "catalog-head");
  }
});
