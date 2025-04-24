import telebot
import os
from dotenv import load_dotenv
from telebot import types
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
import json

load_dotenv()

TOKEN = os.getenv("TOKEN")  # Читаем токен из переменной окружения
bot = telebot.TeleBot(TOKEN)

CREATOR_USERNAME = "@clinkz_main"
bot.send_message(5500332720, "Bot started")

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup1 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)

    # Меню
    miniapp_button1 = KeyboardButton(text="Открыть меню", web_app=WebAppInfo(url="https://fyreks1.github.io/Timur228"))
    markup1.add(miniapp_button1)

    # Поддержка
    btn = KeyboardButton("Поддержка")
    markup1.add(btn)

    # Отзыв
    btn1 = KeyboardButton("Отзыв или предложение по улучшению")
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

# Обработчик данных, отправленных из WebApp
@bot.message_handler(func=lambda message: message.text)
def handle_cart_data(message):
    try:
        # Добавляем отладочную печать
        print("Получены данные от WebApp:", message.text)
        
        cart_data = json.loads(message.text)
        
        items = "\n".join(cart_data["items"])
        total = cart_data["total"]
        item_count = cart_data["itemCount"]

        # Формируем сообщение
        order_message = f"""
        ● Товары:
        {items}
        
        ● Итого:
        {total}₽ ({item_count} шт.)
        """

        # Отправляем сообщение с данными о заказе
        bot.send_message(message.chat.id, order_message)
        # Отправляем данные администратору (или в другой чат)
        bot.send_message(5500332720, f"Новый заказ: \n{order_message}")
    except json.JSONDecodeError as e:
        print(e)
        bot.send_message(message.chat.id, "Ошибка при получении данных. Пожалуйста, попробуйте снова.")

# Обработчики для других кнопок
@bot.message_handler(func=lambda message: message.text == "Поддержка")
def send_creator(message):
    bot.send_message(message.chat.id, "Наш менеджер свяжется с вами через 5 минут. 😇")

@bot.message_handler(func=lambda message: message.text == "Отзыв или предложение по улучшению")
def send_review(message):
    bot.send_message(message.chat.id, "Пожалуйста, напишите ваш отзыв или предложение")

# Запускаем бота
bot.polling(none_stop=True)
