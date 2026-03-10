from flask import Flask, render_template, redirect
import sqlite3

app = Flask(__name__)

# Database connection
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


# Create database tables
def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS food(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        price INTEGER
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        food_name TEXT,
        price INTEGER
    )
    ''')

    conn.commit()
    conn.close()


# Home page
@app.route('/')
def index():
    return render_template('index.html')


# Menu page
@app.route('/menu')
def menu():
    conn = get_db_connection()
    foods = conn.execute('SELECT * FROM food').fetchall()
    conn.close()

    return render_template('menu.html', foods=foods)


# Order food
@app.route('/order/<int:id>')
def order(id):

    conn = get_db_connection()

    food = conn.execute(
        'SELECT * FROM food WHERE id=?', (id,)
    ).fetchone()

    conn.execute(
        'INSERT INTO orders (food_name, price) VALUES (?,?)',
        (food['name'], food['price'])
    )

    conn.commit()
    conn.close()

    return redirect('/success')


# Order success page
@app.route('/success')
def success():
    return render_template('order_success.html')


if __name__ == '__main__':
    create_tables()
    app.run(debug=True)