Telegram.WebApp.expand(); // развернуть окно

let cart = [];
let total = 0;

const cartSummary = document.getElementById("cart-summary");
const cartMenu = document.getElementById("cart-menu");
const cartItems = document.getElementById("cart-items");
const cartTotal = document.getElementById("cart-total");
const backButton = document.getElementById("buy-button");
const productList = document.querySelector(".product-list");

function applyThemeColors() {
  const theme = Telegram.WebApp.themeParams;

  document.documentElement.style.setProperty('--bg-color', theme.bg_color || '#ffffff');
  document.documentElement.style.setProperty('--text-color', theme.text_color || '#000000');
  document.documentElement.style.setProperty('--button-color', theme.button_color || '#d7ffd7');
  document.documentElement.style.setProperty('--button-text-color', theme.button_text_color || '#000000');
  document.documentElement.style.setProperty('--hint-color', theme.hint_color || '#2ea12e');
  document.documentElement.style.setProperty('--link-color', theme.link_color || '#0000ee');
  document.documentElement.style.setProperty('--secondary-bg-color', theme.secondary_bg_color || '#e7ffe7');
}

applyThemeColors();


// Функция обновления корзины
function updateCart() {
  cartItems.innerHTML = "";
  total = 0;

  cart.forEach(item => {
    const div = document.createElement("div");
    div.textContent = `${item.name} — ${item.price}₽`;
    cartItems.appendChild(div);
    total += item.price;
  });

  cartTotal.textContent = `Итого: ${total}₽`;
  cartSummary.textContent = `Корзина: ${total}₽`;
}

// Клик по кнопке "в корзину"
document.querySelectorAll(".product").forEach(product => {
  const button = product.querySelector("button");
  const name = product.querySelector("h3").textContent;
  const priceText = product.querySelector(".price").textContent;
  const price = parseInt(priceText.match(/\d+/)[0]);


  button.addEventListener("click", () => {
    cart.push({ name, price });
    updateCart();
  });
});

// Клик по зелёной кнопке
cartSummary.addEventListener("click", () => {
  
  halal.style.display = "none";
  productList.style.display = "none";
  cartMenu.style.display = "block";
  cartSummary.style.display = "none";
});

// Назад к товарам
buyButton.addEventListener("click", () => {
  courier.style.display = "flex";
  pickup.style.display = "flex";
  buyButton.style.display = "none";
});
