import os
import json
import telebot
from dotenv import load_dotenv
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

# Загрузка токена из .env
load_dotenv()
TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

# Жестко заданный ID владельца
ADMIN_CHAT_ID = 5500332720

# Команда /start — WebApp-кнопка и поддержка
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        KeyboardButton(
            text="Открыть меню",
            web_app=WebAppInfo(url="https://fyreks1.github.io/Timur228")
        )
    )
    markup.add("Поддержка", "Отзыв или предложение по улучшению")

    bot.send_message(
        message.chat.id,
        "Добро пожаловать в магазин «Гастрономчик»! 🛒\n"
        "Нажмите «Открыть меню» для выбора продуктов.",
        reply_markup=markup
    )

# Обработка JSON от WebApp (без подтверждения пользователю)
@bot.message_handler(func=lambda message: message)
def handle_webapp_data(message):
    try:
        data = json.loads(message.text)
    except json.JSONDecodeError:
        return

    if data.get("source") != "webapp":
        return

    items = data.get("items", [])
    total = data.get("total", 0)
    item_count = data.get("itemCount", 0)

    item_lines = [f"• {item['name']} — {item['price']}₽" for item in items]
    order_text = (
        "📦 *Новый заказ!*\n\n"
        + "\n".join(item_lines)
        + f"\n\n💰 Итого: *{total}₽* ({item_count} шт.)"
    )

    # Отправляем заказ только владельцу
    bot.send_message(ADMIN_CHAT_ID, order_text, parse_mode="Markdown")

    # Лог для отладки (опционально)
    print(f"[LOG] Получен заказ: {data}")

# Поддержка
@bot.message_handler(func=lambda message: message.text == "Поддержка")
def support_handler(message):
    bot.send_message(message.chat.id, "Свяжемся с вами в течение 5 минут 😊")

# Отзыв
@bot.message_handler(func=lambda m: m.text == "Отзыв или предложение по улучшению")
def feedback_handler(message):
    bot.send_message(message.chat.id, "Пожалуйста, напишите ваш отзыв или идею.")

if __name__ == "__main__":
    print("[INFO] Бот запущен. Ожидаем заказы...")
    bot.polling(none_stop=True)
