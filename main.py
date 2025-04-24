import telebot
import os
from dotenv import load_dotenv
from telebot import types
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

load_dotenv()

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

CREATOR_USERNAME = "@clinkz_main"
bot.send_message(5500332720, "started")

# Обработчик команды /start
@bot.message_handler(commands=['start'])

def send_welcome(message):
    markup1 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)

#меню
    miniapp_button1 = KeyboardButton(text="Открыть меню", web_app=WebAppInfo(url="https://fyreks1.github.io/Timur228"))
    markup1.add(miniapp_button1)

#поддержка
    btn = KeyboardButton("Поддержка")
    markup1.add(btn)

#отзыв или предложение по улучшению
    btn1 = KeyboardButton("Отзыв или предложение по улучшению")
    markup1.add(btn1)

#сообщение с кнопками
    bot.send_message(message.chat.id, "Приветствуем вас в магазине Гастрономчик", reply_markup=markup1)

@bot.message_handler(func=lambda message: message.text == "Поддержка")

def send_creator(message):
    bot.send_message(message.chat.id, f"Вы можете связаться с нами тут - {CREATOR_USERNAME}, либо же через кнопку отзыва")

@bot.message_handler(func=lambda message: message.text == "Отзыв или предложение по улучшению")

def feedback(message):
    bot.send_message(message.chat.id, "Отправьте ваш отзыв")

@bot.message_handler(func=lambda message: message.text)

def send_feedack(message):
    bot.send_message(5500332720, f"У вас новый отзыв - {message.text}")

# Запуск бота
bot.infinity_polling()

