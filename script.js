Telegram.WebApp.expand(); // развернуть окно


document.getElementById('add-to-cart').addEventListener('click', function() {
    // Например, можно отправить запрос на сервер для добавления товара в корзину
    fetch('/add_to_cart', {
      method: 'POST',
      body: JSON.stringify({
        item: {
          name: 'Пельмени куриные',
          price: '438₽/кг',
        },
        telegram_id: '123456789'  // Пример телеграм ID пользователя
      }),
      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(response => response.json())
    .then(data => {
      console.log('Товар добавлен в корзину:', data);
    })
    .catch(error => {
      console.error('Ошибка при добавлении в корзину:', error);
    });
  });
  