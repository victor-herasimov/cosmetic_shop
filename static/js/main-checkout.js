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

// Handle form submission
// const form = document.getElementById("checkoutForm")
// if (form) {
//   form.addEventListener("submit", (e) => {
//     e.preventDefault()

//     // В реальності тут була б відправка даних на сервер
//     const formData = new FormData(form)
//     const data = Object.fromEntries(formData.entries())
//     console.log("Order submitted:", data)

//     // Імітація успішного замовлення
//     localStorage.removeItem(CART_KEY)

//     // Показуємо повідомлення про успіх
//     const root = document.querySelector(".checkout")
//     if (root) {
//       root.innerHTML = `
//         <div class="catalog-empty" style="padding: 80px 20px; border: none; background: var(--surface); border-radius: var(--radius); box-shadow: var(--shadow);">
//           <div style="width: 80px; height: 80px; background: var(--accent-soft); color: var(--accent); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 24px;">
//             ${icons.check}
//           </div>
//           <h2 style="font-family: var(--font-serif); font-size: 32px; margin-bottom: 12px;">Дякуємо за замовлення!</h2>
//           <p style="color: var(--ink-soft); max-width: 400px; margin: 0 auto 24px;">
//             Ми отримали вашу заявку. Наш менеджер зв'яжеться з вами найближчим часом для підтвердження.
//           </p>
//           <a href="/index.html" class="btn btn--primary">На головну</a>
//         </div>
//       `
//       window.scrollTo({ top: 0, behavior: 'smooth' })
//     }

//     // Оновлюємо лічильник кошика в хедері
//     document.querySelectorAll("[data-cart-count]").forEach(el => {
//       el.textContent = "0"
//       el.style.display = "none"
//     })
//   })
// }
