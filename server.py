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
