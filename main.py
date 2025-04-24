import os
import json
import telebot
from dotenv import load_dotenv
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

# Загрузка токена из .env
load_dotenv()
TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

ADMIN_CHAT_ID = 5500332720  # ваш админ-чат

# /start — даём кнопку для WebApp и альтернативы
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    markup.add(
        KeyboardButton(
            text="Открыть меню",
            web_app=WebAppInfo(url="https://fyreks1.github.io/Timur228")
        )
    )
    markup.add(KeyboardButton("Поддержка"))
    markup.add(KeyboardButton("Отзыв или предложение по улучшению"))

    bot.send_message(
        message.chat.id,
        "Добро пожаловать в магазин «Гастрономчик»👋\n"
        "Нажмите «Открыть меню» для каталога🛒\n"
        "📞 +7(000)000-00-00 — 24/7",
        reply_markup=markup
    )

# Универсальный обработчик: ждём JSON от WebApp
@bot.message_handler(func=lambda m: True)
def handle_webapp_data(message):
    text = message.text or ""
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        # Не JSON — обычное сообщение, игнорируем
        return

    # Проверяем маркер и источник
    if data.get("source") != "webapp":
        return

    # Извлекаем параметры
    chat_id   = data.get("chatId", message.chat.id)
    items     = data.get("items", [])
    total     = data.get("total", 0)
    itemCount = data.get("itemCount", 0)

    # Формируем текст заказа
    order_msg = "● Товары:\n" + "\n".join(items)
    order_msg += f"\n\n● Итого: {total}₽ ({itemCount} шт.)"

    # Отправляем пользователю
    bot.send_message(chat_id, order_msg)
    # Дублируем админу
    bot.send_message(ADMIN_CHAT_ID, f"Новый заказ от {chat_id}:\n{order_msg}")

# Поддержка
@bot.message_handler(func=lambda m: m.text == "Поддержка")
def support_handler(message):
    bot.send_message(message.chat.id, "Наш менеджер свяжется с вами в течение 5 минут. 😇")

# Отзыв
@bot.message_handler(func=lambda m: m.text == "Отзыв или предложение по улучшению")
def feedback_handler(message):
    bot.send_message(message.chat.id, "Пожалуйста, пришлите ваш отзыв или предложение.")

if __name__ == "__main__":
    bot.polling(none_stop=True)
