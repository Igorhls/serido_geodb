const municipios = document.querySelectorAll(".municipios path");
const tooltip = document.querySelector(".tooltip");
const currentName = document.querySelector("#municipio-atual");
const mapStage = document.querySelector(".rn-stage");

municipios.forEach((municipio) => {
  municipio.setAttribute("tabindex", "0");
  municipio.setAttribute("role", "button");
  municipio.setAttribute("aria-label", municipio.dataset.name);

  municipio.addEventListener("mouseenter", (event) => showMunicipio(municipio, event));
  municipio.addEventListener("mousemove", moveTooltip);
  municipio.addEventListener("focus", () => showMunicipio(municipio));
  municipio.addEventListener("mouseleave", hideMunicipio);
  municipio.addEventListener("blur", hideMunicipio);
});

function showMunicipio(municipio, event) {
  currentName.textContent = municipio.dataset.name;
  tooltip.classList.add("is-visible");

  if (event) {
    moveTooltip(event);
  }
}

function moveTooltip(event) {
  const bounds = mapStage.getBoundingClientRect();
  const x = event.clientX - bounds.left;
  const y = event.clientY - bounds.top;

  tooltip.style.left = `${x}px`;
  tooltip.style.top = `${y}px`;
}

function hideMunicipio() {
  currentName.textContent = "passe o mouse";
  tooltip.classList.remove("is-visible");
  tooltip.removeAttribute("style");
}
