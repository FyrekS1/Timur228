import telebot
import os
from dotenv import load_dotenv
from telebot import types
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

# Загрузка переменных окружения из .env
load_dotenv()

# Получение токена
TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

# Отправка сообщения при старте
bot.send_message(5500332720, "started")

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Создание клавиатуры для пользователя
    markup1 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    
    # Кнопка для запуска Mini App
    miniapp_button1 = KeyboardButton(
        text="Запустить Mini App", 
        web_app=WebAppInfo(url="https://fyreks1.github.io/Timur228")
    )
    
    # Добавление кнопки на клавиатуру
    markup1.add(miniapp_button1)
    
    # Отправка сообщения с клавиатурой
    bot.send_message(message.chat.id, "Привет! Нажми на кнопку для запуска Mini App.", reply_markup=markup1)

# Запуск бота
bot.infinity_polling()

