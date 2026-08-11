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

// ===== Глобальна делегація подій =====
function bindGlobalEvents() {
  document.addEventListener("click", (e) => {
    const t = e.target;

    const openCart = t.closest("[data-open-cart]");
    if (openCart) {
      e.preventDefault();
      openModal("cartModal");
      return;
    }

    const openDeleteAccountModal = t.closest("[data-open-delete-account]");
    if (openDeleteAccountModal) {
      console.log("delete modal");
      e.preventDefault();
      openModal("accountDeleteModal");
      return;
    }

    const openCats = t.closest("[data-open-categories]");
    if (openCats) {
      e.preventDefault();
      openModal("categoriesModal");
      return;
    }

    const openLogin = t.closest("[data-open-login]");
    if (openLogin) {
      e.preventDefault();
      const loginForm = document.getElementById("loginForm");
      if (loginForm) loginForm.reset();
      openModal("loginModal");
      return;
    }

    const openProfile = t.closest("[data-open-profile]");
    if (openProfile) {
      e.preventDefault();
      openModal("userModal");
      return;
    }

    const openFilters = t.closest("[data-open-filters]");
    if (openFilters) {
      e.preventDefault();
      openModal("filtersModal");
      return;
    }

    const switchToRegister = t.closest("[data-switch-to-register]");
    if (switchToRegister) {
      e.preventDefault();
      const loginModal = document.getElementById("loginModal");
      if (loginModal) closeModal(loginModal);
      const registerForm = document.getElementById("registerForm");
      if (registerForm) registerForm.reset();
      openModal("registerModal");
      return;
    }

    const switchToLogin = t.closest("[data-switch-to-login]");
    if (switchToLogin) {
      e.preventDefault();
      const registerModal = document.getElementById("registerModal");
      if (registerModal) closeModal(registerModal);
      const loginForm = document.getElementById("loginForm");
      if (loginForm) loginForm.reset();
      openModal("loginModal");
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
    if (
      t.closest("[data-close-modal]") ||
      t.classList.contains("modal__overlay")
    ) {
      const modal = t.closest(".modal");
      if (modal) closeModal(modal);
      return;
    }
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      document.querySelectorAll(".modal.is-open").forEach(closeModal);
    }
  });
}

// Маска для номера телефону
export function phoneNumberMask(selector, mask, parent = document) {
  const element = parent.querySelector(selector);
  if (!element) return;
  const maskOptions = {
    mask: mask,
  };
  IMask(element, maskOptions);
}

// Прокрутка до певногоблока блока
// export function scrollToElement(eventInitId, toScrollEl) {
//   const initialEl = document.getElementById(eventInitId);
//   if (initialEl) {
//     initialEl.addEventListener("htmx:afterRequest", (e) => {
//       const targetElement = document.getElementById(toScrollEl);
//       console.log(targetElement);
//       if (targetElement) {
//         targetElement.scrollIntoView({ behavior: "smooth" });
//       }
//     });
//   }
// }

export function scrollToElement(toScrollEl) {
  const targetElement = document.getElementById(toScrollEl);
  if (targetElement) {
    targetElement.scrollIntoView({ behavior: "smooth" });
  } else {
    console.warn(`[Scroll] Елемент #${toScrollEl} не знайдено`);
  }
}

function closeAllModals() {
  const modals = document.querySelectorAll(".modal.is-open");
  if (modals) {
    modals.forEach((modal) => {
      closeModal(modal);
    });
  }
}

document.addEventListener("htmx:load", (event) => {
  const target = event.detail.elt;
  const phoneInput = target.querySelector
    ? target.querySelector("#id_register_phone")
    : null;
  if (phoneInput) {
    phoneNumberMask("#id_register_phone", "{+38 (\\0}00) 000-00-00", target);
  }
});

document.addEventListener("DOMContentLoaded", function () {
  const urlParams = new URLSearchParams(window.location.search);

  // Якщо прийшли після редіректу без HTMX
  if (urlParams.get("login_required") === "1") {
    openModal("loginModal");
    window.history.replaceState({}, document.title, window.location.pathname);
  }
});

// Закриваємо модальні вікна після Реєстрації/Логіна
document.body.addEventListener("userLoggedIn", function (event) {
  closeAllModals();
  const favoriteIds = event.detail.favoriteIds || [];

  if (favoriteIds) {
    favoriteIds.forEach((id) => {
      // Wishlist button on product card
      const productCard = document.getElementById(`product-${id}`);
      if (productCard) {
        const productCardWishlistBtn =
          productCard.querySelector(".card__wishlist");
        if (productCardWishlistBtn) {
          productCardWishlistBtn.classList.add("is-wishlisted");
          productCardWishlistBtn.setAttribute(
            "aria-label",
            "Видалити з обраного",
          );
          productCardWishlistBtn.setAttribute("aria-pressed", "true");
        }
      }

      // Wishlist button on detail page
      const wishlistBtn = document.getElementById(`product-wishlist-btn-${id}`);
      if (wishlistBtn) {
        wishlistBtn.classList.add("is-wishlisted");
        wishlistBtn.setAttribute("aria-label", "Видалити з обраного");
        wishlistBtn.setAttribute("aria-pressed", "true");
      }
    });
  }
});

// Відкриваємо Модальне вікно логіну
document.body.addEventListener("openLoginModal", function (event) {
  openModal("loginModal");
});

// Закриваємо модальні вікна після Логаута
document.body.addEventListener("userLoggedOut", function (event) {
  closeAllModals();
  const productDetailWishlistBtn = document.querySelector(
    ".pdp__wishlist.is-wishlisted",
  );
  if (productDetailWishlistBtn) {
    productDetailWishlistBtn.classList.remove("is-wishlisted");
    productDetailWishlistBtn.setAttribute("aria-label", "Додати в обране");
    productDetailWishlistBtn.setAttribute("aria-pressed", "false");
  }

  const productCardWishlistBtn = document.querySelectorAll(
    ".card__wishlist.is-wishlisted",
  );
  if (productCardWishlistBtn) {
    productCardWishlistBtn.forEach((wishlistBtn) => {
      wishlistBtn.classList.remove("is-wishlisted");
      wishlistBtn.setAttribute("aria-label", "Додати в обране");
      wishlistBtn.setAttribute("aria-pressed", "false");
    });
  }
});

document.body.addEventListener("showPasswordResetModal", function (event) {
  closeAllModals();
  setTimeout(() => openModal("passwordResetModal"), 200);
});

// document.body.addEventListener("htmx:configRequest", (event) => {
//   const name = "csrftoken";
//   const matches = document.cookie.match(
//     new RegExp(
//       "(?:^|; )" +
//         name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, "\\$1") +
//         "=([^;]*)",
//     ),
//   );
//   const token = matches ? decodeURIComponent(matches[1]) : null;
//   if (token) {
//     event.detail.headers["X-CSRFToken"] = token;
//   }
// });

document.addEventListener("htmx:afterRequest", (event) => {
  // Перевіряємо, чи повернув сервер новий токен у заголовку
  const newToken = event.detail.xhr.getResponseHeader("X-CSRFToken");
  if (newToken) {
    // Оновлюємо атрибут hx-headers у body для всіх наступних HTMX-запитів
    document.body.setAttribute(
      "hx-headers",
      JSON.stringify({ "X-CSRFToken": newToken }),
    );
  }
});

// ===== Ініціалізація =====
export function init() {
  bindGlobalEvents();
}
