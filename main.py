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

from flask import Flask, request, session, jsonify
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('cart.db')
    conn.row_factory = sqlite3.Row  # Позволяет обращаться к колонкам по имени
    return conn

# Создание таблицы корзины (если она еще не существует)
def create_table():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS cart (
                        telegram_id INTEGER NOT NULL,
                        name TEXT NOT NULL,
                        price TEXT NOT NULL)''')
    conn.commit()
    conn.close()


create_table()

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    item = request.json.get('item')
    telegram_id = request.json.get('telegram_id')  # Получаем telegram_id из запроса
    
    if item and telegram_id:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO cart (telegram_id, name, price) VALUES (?, ?, ?)', 
                       (telegram_id, item['name'], item['price']))
        conn.commit()
        conn.close()
        return jsonify({'status': 'ok', 'message': 'Item added to cart'})
    return jsonify({'status': 'error', 'message': 'Invalid item or telegram_id'}), 400

@app.route('/view_cart', methods=['GET'])
def view_cart():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM cart')
    items = cursor.fetchall()
    cart = [{"name": item['name'], "price": item['price']} for item in items]
    conn.close()
    return jsonify(cart)

if __name__ == '__main__':
    app.run(debug=True)
