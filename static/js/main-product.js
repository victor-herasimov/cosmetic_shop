import { initChrome, addToCart } from "./app.js";
import { PRODUCTS, CATEGORIES } from "./products.js";

initChrome();

const params = new URLSearchParams(location.search);
const id = params.get("id");
const product = PRODUCTS.find((p) => p.id === id) || PRODUCTS[0];

document.title = `${product.name} — ROBEAUTY`;

// document.getElementById("productRoot").innerHTML = `
//   <div class="pdp">
//     <div class="pdp__gallery">
//       <div class="pdp__main">
//         ${product.tag ? `<span class="card__tag ${product.tag === "sale" ? "card__tag--sale" : ""}">${product.tag === "sale" ? "Акція" : product.tag}</span>` : ""}
//         <img src="${product.img}" alt="${product.name}">
//       </div>
//       <div class="pdp__thumbs">
//         <button class="pdp__thumb is-active"><img src="${product.img}" alt=""></button>
//         <button class="pdp__thumb"><img src="/images/hero.png" alt=""></button>
//         <button class="pdp__thumb"><img src="/images/product-2.png" alt=""></button>
//       </div>
//     </div>

//     <div class="pdp__info">
//       <span class="card__cat">${catName}</span>
//       <h1 class="pdp__title">${product.name}</h1>
//       <div class="pdp__rating">
//         <span class="stars">${stars(product.rating)}</span>
//         <span>${product.rating} · ${product.reviews} відгуків</span>
//       </div>
//       <p class="pdp__desc">${product.desc}</p>
//       <div class="pdp__price">${priceHtml}</div>

//       <div class="pdp__buy">
//         <div class="qty" id="qty">
//           <button data-q="-1" aria-label="Менше">−</button>
//           <span id="qtyVal">1</span>
//           <button data-q="1" aria-label="Більше">+</button>
//         </div>
//         <button class="btn btn--primary btn--lg" id="addBtn">Додати в кошик</button>
//       </div>

//       <ul class="pdp__benefits">
//         ${benefits.map((b) => `<li>${b.icon}<span>${b.text}</span></li>`).join("")}
//       </ul>

//       <div class="accordion" id="accordion">
//         <div class="accordion__item is-open">
//           <button class="accordion__head">Опис<span>+</span></button>
//           <div class="accordion__body"><p>${product.desc} Засіб підходить для щоденного використання та делікатно діє навіть на чутливу шкіру.</p></div>
//         </div>
//         <div class="accordion__item">
//           <button class="accordion__head">Спосіб застосування<span>+</span></button>
//           <div class="accordion__body"><p>Нанесіть невелику кількість засобу на очищену шкіру вранці та/або ввечері. Рівномірно розподіліть масажними рухами до повного вбирання.</p></div>
//         </div>
//         <div class="accordion__item">
//           <button class="accordion__head">Склад<span>+</span></button>
//           <div class="accordion__body"><p>Aqua, Glycerin, Niacinamide, Sodium Hyaluronate, Panthenol, Tocopherol, рослинні екстракти та активні пептиди.</p></div>
//         </div>
//         <div class="accordion__item">
//           <button class="accordion__head">Доставка та оплата<span>+</span></button>
//           <div class="accordion__body"><p>Відправка Новою Поштою по всій Україні протягом 1–3 днів. Безкоштовна доставка від 1000 ₴. Оплата онлайн або при отриманні.</p></div>
//         </div>
//       </div>
//     </div>
//   </div>`;

// Кількість
let qty = 1;
const qtyVal = document.getElementById("qtyVal");
document.getElementById("qty").addEventListener("click", (e) => {
  const btn = e.target.closest("[data-q]");
  if (!btn) return;
  qty = Math.max(1, qty + Number(btn.getAttribute("data-q")));
  qtyVal.textContent = qty;
});

// Додати в кошик
document.getElementById("addBtn").addEventListener("click", () => {
  addToCart(product.id, qty);
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
