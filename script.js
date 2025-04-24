// Функция для получения chat_id
async function getChatId() {
  const url = `https://api.telegram.org/bot${botToken}/getUpdates`;

  try {
    const response = await fetch(url);
    const data = await response.json();

    if (data && data.result && data.result.length > 0) {
      const chatId = data.result[0].message.chat.id; // Извлекаем chat_id первого сообщения
      console.log('Chat ID:', chatId);
      return chatId;
    } else {
      console.error('No updates found');
      return null;
    }
  } catch (error) {
    console.error("Error fetching chat id:", error);
    return null;
  }
}

// Функция для отправки заказа в Telegram
async function sendOrderToTelegram(cart) {
  const items = cart.map(item => `${item.name} — ${item.price}₽`);
  const total = cart.reduce((sum, item) => sum + item.price, 0);
  const message = `
    ● Товары:
    ${items.join('\n')}
    
    ● Итого:
    ${total}₽ (${cart.length} шт.)
  `;
  
  const chatId = await getChatId(); // Получаем chat_id динамически

  if (!chatId) {
    console.error("chatId is required");
    return;
  }

  const url = `https://api.telegram.org/bot${botToken}/sendMessage`;

  const body = {
    chat_id: chatId,
    text: message,
  };

  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    });
    const data = await response.json();
    console.log("Message sent", data);
  } catch (error) {
    console.error("Error sending message:", error);
  }
}

Telegram.WebApp.expand(); // развернуть окно

let cart = [];
let total = 0;

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

const cartSummary = document.getElementById("cart-summary");
const cartMenu = document.getElementById("cart-menu");
const cartItems = document.getElementById("cart-items");
const cartTotal = document.getElementById("cart-total");
const backButton = document.getElementById("buyButton");
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

// Когда пользователь нажимает кнопку "Оформить заказ"
backButton.addEventListener("click", async () => {
  const cartData = {
    items: cart.map(item => `${item.name} — ${item.price}₽`),
    total: cart.reduce((sum, item) => sum + item.price, 0),
    itemCount: cart.length
  };

  // Отправляем данные через WebApp.sendData
  Telegram.WebApp.sendData(JSON.stringify(cartData));

  // Закрываем WebApp
  Telegram.WebApp.close();

  // Уведомление для пользователя
  alert("Ваш заказ оформлен!");
  await sendOrderToTelegram(cart);
});
