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
      // renderCart();
      openModal("cartModal");
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

// Закриваємо модальні вікна після Реєстрації/Логіна
document.body.addEventListener("userLoggedIn", function (event) {
  closeAllModals();
});

// Закриваємо модальні вікна після Логаута
document.body.addEventListener("userLoggedOut", function (event) {
  closeAllModals();
});

document.body.addEventListener("showPasswordResetModal", function (event) {
  closeAllModals();
  setTimeout(() => openModal("passwordResetModal"), 200);
});

document.body.addEventListener("htmx:configRequest", (event) => {
  const name = "csrftoken";
  const matches = document.cookie.match(
    new RegExp(
      "(?:^|; )" +
        name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, "\\$1") +
        "=([^;]*)",
    ),
  );
  const token = matches ? decodeURIComponent(matches[1]) : null;
  if (token) {
    event.detail.headers["X-CSRFToken"] = token;
  }
});

// ===== Ініціалізація =====
export function init() {
  bindGlobalEvents();
}
