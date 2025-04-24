import os
import telebot
import json
from dotenv import load_dotenv
from telebot import types
from telebot.types import WebAppInfo

load_dotenv()

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

CREATOR_USERNAME = "@clinkz_main"
bot.send_message(5500332720, "Bot started")

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)

    # Меню
    miniapp_button1 = types.KeyboardButton(text="Открыть меню", web_app=WebAppInfo(url="https://fyreks1.github.io/Timur228"))
    markup1.add(miniapp_button1)

    # Поддержка
    btn = types.KeyboardButton("Поддержка")
    markup1.add(btn)

    # Отзыв
    btn1 = types.KeyboardButton("Отзыв или предложение по улучшению")
    markup1.add(btn1)

    # Сообщение с кнопками
    bot.send_message(message.chat.id, """Добро пожаловать в магазин "Гастрономчик"👋
Нажмите кнопку "Открыть приложение" чтобы просмотреть каталог/меню🛒🍜
Наши контакты:
📍 Адрес:
🙍‍♀️ Менеджер по всем вопросам (укажите username)
📞 +7(000)000-00-00
🏪 Работаем 24/7
🚛 Доставляем по всему городу
""", reply_markup=markup1)

# Обработчик данных из WebApp
@bot.message_handler(func=lambda message: message.text)
def handle_cart_data(message):
    try:
        cart_data = json.loads(message.text)

        items = "\n".join(cart_data["items"])
        total = cart_data["total"]
        item_count = cart_data["itemCount"]

        order_message = f"""
        ● Товары:
        {items}
        
        ● Итого:
        {total}₽ ({item_count} шт.)
        """

        bot.send_message(message.chat.id, order_message)
        bot.send_message(5500332720, f"Новый заказ: \n{order_message}")
    except json.JSONDecodeError:
        bot.send_message(message.chat.id, "Ошибка при получении данных. Пожалуйста, попробуйте снова.")

# Другие обработчики
@bot.message_handler(func=lambda message: message.text == "Поддержка")
def send_creator(message):
    bot.send_message(message.chat.id, f"Вы можете связаться с нами тут - {CREATOR_USERNAME}")

@bot.message_handler(func=lambda message: message.text == "Отзыв или предложение по улучшению")
def feedback(message):
    bot.send_message(message.chat.id, "Отправьте ваш отзыв")

# Запуск бота
bot.infinity_polling()
