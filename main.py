import telebot
import os
from dotenv import load_dotenv
from telebot import types
load_dotenv()

TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN)
bot.send_message(5500332720, "started")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Создаем клавиатуру с кнопкой, которая будет открывать Web App
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text="Перейти в мини-приложение", url="https://fyreks1.github.io/Timur228")
    markup.add(button)

    # Отправляем приветственное сообщение с кнопкой
    bot.send_message(message.chat.id, "Привет! Нажми на кнопку ниже, чтобы перейти в мини-приложение.", reply_markup=markup)

# Запуск бота
if __name__ == '__main__':
    bot.polling(none_stop=True)