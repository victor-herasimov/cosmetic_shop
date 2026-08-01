import { init, scrollToElement } from "./app.js";
init();

document.addEventListener("htmx:afterSwap", (event) => {
  console.log(event.detail.target);
  if (event.detail.target.id === "ordersContainer") {
    scrollToElement("orders-head-wrapper");
  }
});
