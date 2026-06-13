import { CATEGORIES, PRODUCTS, formatPrice } from "./data.js";
import { icons } from "./icons.js";

const CART_KEY = "robeauty_cart";

// ===== Стан корзини =====
function loadCart() {
  try {
    return JSON.parse(localStorage.getItem(CART_KEY)) || [];
  } catch {
    return [];
  }
}

let cart = loadCart();

function saveCart() {
  localStorage.setItem(CART_KEY, JSON.stringify(cart));
  updateCartCount();
}

export function addToCart(productId, qty = 1) {
  const product = PRODUCTS.find((p) => p.id === productId);
  if (!product) return;
  const existing = cart.find((i) => i.id === productId);
  if (existing) {
    existing.qty += qty;
  } else {
    cart.push({ id: productId, qty });
  }
  saveCart();
  renderCart();
  showToast(`«${product.name}» додано в кошик`);
}

function changeQty(productId, delta) {
  const item = cart.find((i) => i.id === productId);
  if (!item) return;
  item.qty += delta;
  if (item.qty <= 0) {
    cart = cart.filter((i) => i.id !== productId);
  }
  saveCart();
  renderCart();
}

function removeFromCart(productId) {
  cart = cart.filter((i) => i.id !== productId);
  saveCart();
  renderCart();
}

function cartTotal() {
  return cart.reduce((sum, item) => {
    const p = PRODUCTS.find((x) => x.id === item.id);
    return sum + (p ? p.price * item.qty : 0);
  }, 0);
}

function cartCount() {
  return cart.reduce((sum, i) => sum + i.qty, 0);
}

function updateCartCount() {
  document.querySelectorAll("[data-cart-count]").forEach((el) => {
    const count = cartCount();
    el.textContent = count;
    el.style.display = count > 0 ? "flex" : "none";
  });
}

// ===== Рендер корзини =====
function renderCart() {
  const itemsEl = document.getElementById("cartItems");
  const footEl = document.getElementById("cartFoot");
  if (!itemsEl) return;

  if (cart.length === 0) {
    itemsEl.innerHTML = `
      <div class="cart__empty">
        <div>${icons.bag}</div>
        <p>Ваш кошик поки порожній</p>
      </div>`;
    if (footEl) footEl.style.display = "none";
    return;
  }

  itemsEl.innerHTML = cart
    .map((item) => {
      const p = PRODUCTS.find((x) => x.id === item.id);
      if (!p) return "";
      return `
      <div class="cart-item">
        <div class="cart-item__img"><img src="${p.img}" alt="${p.name}"></div>
        <div>
          <div class="cart-item__name">${p.name}</div>
          <div class="cart-item__price">${formatPrice(p.price)}</div>
          <div class="cart-item__qty">
            <button data-dec="${p.id}" aria-label="Менше">−</button>
            <span>${item.qty}</span>
            <button data-inc="${p.id}" aria-label="Більше">+</button>
          </div>
        </div>
        <button class="cart-item__remove" data-remove="${p.id}" aria-label="Видалити">${icons.trash}</button>
      </div>`;
    })
    .join("");

  if (footEl) {
    footEl.style.display = "block";
    const total = cartTotal();
    const discount = Math.round(total * 0.1);
    footEl.innerHTML = `
      <div class="cart__row"><span>Сума</span><span>${formatPrice(total)}</span></div>
      <div class="cart__row"><span>Знижка за промокодом BEAUTY10</span><span>−${formatPrice(discount)}</span></div>
      <div class="cart__total"><span>До сплати</span><span>${formatPrice(total - discount)}</span></div>
      <button class="btn btn--primary btn--block">Оформити замовлення</button>`;
  }
}

// ===== Модальні вікна =====
function openModal(id) {
  const modal = document.getElementById(id);
  if (!modal) return;
  modal.classList.add("is-open");
  document.body.classList.add("no-scroll");
}

function closeModal(modal) {
  modal.classList.remove("is-open");
  if (!document.querySelector(".modal.is-open")) {
    document.body.classList.remove("no-scroll");
  }
}

// ===== Toast =====
let toastTimer;
function showToast(message) {
  let toast = document.getElementById("toast");
  if (!toast) {
    toast = document.createElement("div");
    toast.id = "toast";
    toast.className = "toast";
    document.body.appendChild(toast);
  }
  toast.innerHTML = `${icons.check} ${message}`;
  toast.style.display = "flex";
  toast.style.alignItems = "center";
  toast.style.gap = "8px";
  // force reflow
  void toast.offsetWidth;
  toast.classList.add("is-show");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove("is-show"), 2400);
}

// ===== Глобальна делегація подій =====
function bindGlobalEvents() {
  document.addEventListener("click", (e) => {
    const t = e.target;

    const openCart = t.closest("[data-open-cart]");
    if (openCart) {
      e.preventDefault();
      renderCart();
      openModal("cartModal");
      return;
    }

    const openCats = t.closest("[data-open-categories]");
    if (openCats) {
      e.preventDefault();
      openModal("categoriesModal");
      return;
    }

    const openSearch = t.closest("[data-open-search]");
    if (openSearch) {
      e.preventDefault();
      openModal("searchModal");
      const input = document.getElementById("searchInput");
      if (input) {
        input.value = "";
        const clearBtn = document.getElementById("searchClear");
        if (clearBtn) clearBtn.style.display = "none";
        setTimeout(() => input.focus(), 150);
      }
      return;
    }

    const tagBtn = t.closest("[data-search-term]");
    if (tagBtn) {
      e.preventDefault();
      const term = tagBtn.getAttribute("data-search-term");
      const input = document.getElementById("searchInput");
      if (input) {
        input.value = term;
        const clearBtn = document.getElementById("searchClear");
        if (clearBtn) clearBtn.style.display = "flex";
        input.focus();
        input.dispatchEvent(new Event("input"));
      }
      return;
    }

    const clearSearch = t.closest("#searchClear");
    if (clearSearch) {
      e.preventDefault();
      const input = document.getElementById("searchInput");
      if (input) {
        input.value = "";
        input.focus();
        clearSearch.style.display = "none";
        document.querySelector(".search-suggest").classList.remove("hidden");
        document.getElementById("searchAnswer").classList.add("hidden");
      }
      return;
    }

    const addBtn = t.closest("[data-add]");
    if (addBtn) {
      e.preventDefault();
      addToCart(addBtn.getAttribute("data-add"));
      return;
    }

    if (
      t.closest("[data-close-modal]") ||
      t.classList.contains("modal__overlay")
    ) {
      const modal = t.closest(".modal");
      if (modal) closeModal(modal);
      return;
    }

    const inc = t.closest("[data-inc]");
    if (inc) return changeQty(inc.getAttribute("data-inc"), 1);
    const dec = t.closest("[data-dec]");
    if (dec) return changeQty(dec.getAttribute("data-dec"), -1);
    const rem = t.closest("[data-remove]");
    if (rem) return removeFromCart(rem.getAttribute("data-remove"));
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      document.querySelectorAll(".modal.is-open").forEach(closeModal);
    }
  });
}

// ===== Ініціалізація =====
export function initChrome() {
  // injectChrome();
  bindGlobalEvents();
  updateCartCount();
  renderCart();
}
