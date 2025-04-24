// Разворачиваем WebApp сразу после загрузки
Telegram.WebApp.expand();

let cart = [];
let total = 0;

// Применить тему Telegram
function applyThemeColors() {
  const theme = Telegram.WebApp.themeParams;
  const root = document.documentElement.style;
  root.setProperty('--bg-color', theme.bg_color || '#ffffff');
  root.setProperty('--text-color', theme.text_color || '#000000');
  root.setProperty('--button-color', theme.button_color || '#d7ffd7');
  root.setProperty('--button-text-color', theme.button_text_color || '#000000');
  root.setProperty('--hint-color', theme.hint_color || '#2ea12e');
  root.setProperty('--link-color', theme.link_color || '#0000ee');
  root.setProperty('--secondary-bg-color', theme.secondary_bg_color || '#e7ffe7');
}

applyThemeColors();

// UI-элементы
const cartSummary = document.getElementById("cart-summary");
const cartMenu    = document.getElementById("cart-menu");
const cartItems   = document.getElementById("cart-items");
const cartTotal   = document.getElementById("cart-total");
const buyButton   = document.getElementById("buyButton");
const productList = document.querySelector(".product-list");
const halalTitle  = document.getElementById("halal");

// Обновление корзины в интерфейсе
function updateCart() {
  cartItems.innerHTML = "";
  total = 0;
  cart.forEach(item => {
    const div = document.createElement("div");
    div.textContent = `${item.name} — ${item.price}₽`;
    cartItems.appendChild(div);
    total += item.price;
  });
  cartSummary.textContent = `Корзина: ${total}₽`;
  cartTotal.textContent   = `Итого: ${total}₽ (${cart.length} шт.)`;
}

// Добавление товаров в корзину
document.querySelectorAll(".product").forEach(product => {
  const btn = product.querySelector("button");
  btn.addEventListener("click", () => {
    const name      = product.querySelector("h3").textContent;
    const priceText = product.querySelector(".price").textContent;
    const price     = parseInt(priceText.match(/\d+/)[0], 10);
    cart.push({ name, price });
    updateCart();
  });
});

// Показ корзины при клике на итоговый блок
cartSummary.addEventListener("click", () => {
  halalTitle.style.display  = "none";
  productList.style.display = "none";
  cartMenu.style.display    = "block";
  cartSummary.style.display = "none";
});

// Оформление заказа и отправка данных в Python-бота
buyButton.addEventListener("click", () => {
  // Берём реальный chat_id пользователя из Telegram WebApp
  const user   = Telegram.WebApp.initDataUnsafe.user;
  const chatId = user && user.id;

  // Собираем данные корзины + метку источника
  const cartData = {
    chatId,
    items     : cart.map(i => `${i.name} — ${i.price}₽`),
    total,
    itemCount : cart.length,
    source    : "webapp"
  };

  // Отправляем в main.py через sendData
  Telegram.WebApp.sendData(JSON.stringify(cartData));

  alert("Ваш заказ отправлен!");
  Telegram.WebApp.close();
});
