import { PRODUCTS, CATEGORIES, formatPrice } from "./data.js"

export function productCard(p) {
  const tagHtml = p.tag
    ? `<span class="card__tag ${p.tag === "sale" ? "card__tag--sale" : ""}">${
        p.tag === "sale" ? "Акція" : p.tag
      }</span>`
    : ""
  const catName = (CATEGORIES.find((c) => c.id === p.cat) || {}).name || ""
  const priceHtml = p.oldPrice
    ? `<b>${formatPrice(p.price)}</b><s>${formatPrice(p.oldPrice)}</s>`
    : `<b>${formatPrice(p.price)}</b>`

  return `
    <article class="card">
      <a class="card__media" href="/product.html?id=${p.id}">
        ${tagHtml}
        <img src="${p.img}" alt="${p.name}">
      </a>
      <div class="card__body">
        <span class="card__cat">${catName}</span>
        <a class="card__name" href="/product.html?id=${p.id}">${p.name}</a>
        <div class="card__price">${priceHtml}</div>
        <div class="card__actions">
          <button class="btn btn--primary card__add" data-add="${p.id}">До кошику</button>
          <a class="btn btn--ghost" href="/product.html?id=${p.id}">Детальніше</a>
        </div>
      </div>
    </article>`
}

export function renderProducts(targetId, list) {
  const el = document.getElementById(targetId)
  if (!el) return
  el.innerHTML = list.map(productCard).join("")
}

export { PRODUCTS, CATEGORIES, formatPrice }
