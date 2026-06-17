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
        console.log("claer");
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

    // const inc = t.closest("[data-inc]");
    // if (inc) return changeQty(inc.getAttribute("data-inc"), 1);
    // const dec = t.closest("[data-dec]");
    // if (dec) return changeQty(dec.getAttribute("data-dec"), -1);
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      document.querySelectorAll(".modal.is-open").forEach(closeModal);
    }
  });
}

// ===== Ініціалізація =====
export function init() {
  bindGlobalEvents();
}
