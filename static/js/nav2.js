const nav = document.querySelector(".navb");
const searchIcon = document.querySelector("#searchIcon");
const navOpenBtn = document.querySelector(".navbOpenBtn");
const navCloseBtn = document.querySelector(".navbCloseBtn");

navOpenBtn.addEventListener("click", () => {
  nav.classList.add("openNavb");
});
navCloseBtn.addEventListener("click", () => {
  nav.classList.remove("openNavb");
});