import { init, scrollToElement } from "./app.js";

function accordionEvents(filterForm) {
  filterForm.querySelectorAll(".accordion-header").forEach((header) => {
    header.addEventListener("click", (e) => {
      e.preventDefault();
      header.parentElement.classList.toggle("is-collapsed");
    });
  });
}

// Збереження стану (шукаємо тільки закриті з is-collapsed)
function saveCurrentState() {
  const allGroups = document.querySelectorAll(".accordion-group");
  let visibleGroup = null;

  for (let group of allGroups) {
    // offsetParent !== null означає, що елемент дійсно відображається на екрані (не display: none)
    if (group.offsetParent !== null) {
      visibleGroup = group;
      break;
    }
  }

  const activeContainer = visibleGroup
    ? visibleGroup.closest("form") || document
    : document;

  const openNames = [];
  const openElements = activeContainer.querySelectorAll(
    ".accordion-group:not(.is-collapsed)",
  );
  openElements.forEach((item) => {
    const name = item.getAttribute("data-filter-name");
    if (name && !openNames.includes(name)) {
      openNames.push(name);
    }
  });
  sessionStorage.setItem("openFilters", JSON.stringify(openNames));
}

// Відновлення стану
function restoreAccordions() {
  const savedData = sessionStorage.getItem("openFilters");
  if (!savedData) return;

  const openFilters = JSON.parse(savedData);

  document.body.classList.add("no-transitions");

  document.querySelectorAll(".accordion-group").forEach((item) => {
    item.classList.add("is-collapsed");
  });
  openFilters.forEach((filterName) => {
    const groups = document.querySelectorAll(
      `.accordion-group[data-filter-name="${filterName}"]`,
    );
    groups.forEach((group) => {
      group.classList.remove("is-collapsed");
    });
  });

  void document.body.offsetHeight;

  document.body.classList.remove("no-transitions");
}

// Перед тим як HTMX замінить контент — фіксуємо, що закрив/відкрив користувач
document.addEventListener("htmx:beforeSwap", function () {
  saveCurrentState();
});

document.addEventListener("htmx:load", (event) => {
  init();
  const target = event.detail.elt;
  const filterForm = target.querySelector("#filter-form");
  const mobileFilterForm = target.querySelector("#mobile-filter-form");
  if (filterForm) {
    accordionEvents(filterForm);
  }
  if (mobileFilterForm) {
    accordionEvents(mobileFilterForm);
  }

  if (sessionStorage.getItem("openFilters") === null) {
    // Якщо перший візит — зчитуємо початкові is-collapsed від Django
    saveCurrentState();
  } else {
    // Якщо вже є дані — відновлюємо їх на новому/старому HTML
    restoreAccordions();
  }
});

document.addEventListener("htmx:afterSwap", (event) => {
  if (event.detail.target.id === "products") {
    scrollToElement("catalog-head-wrapper");
  }
});
