Telegram.WebApp.expand(); // развернуть окно

let cart = [];
let total = 0;

const cartSummary = document.getElementById("cart-summary");
const cartMenu = document.getElementById("cart-menu");
const cartItems = document.getElementById("cart-items");
const cartTotal = document.getElementById("cart-total");
const backButton = document.getElementById("buy-button");
const productList = document.querySelector(".product-list");

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
  const price = parseInt(priceText.replace(/[^\d]/g, ""));

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
