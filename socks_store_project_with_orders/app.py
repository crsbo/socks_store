
from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3, os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def get_db_connection():
    conn = sqlite3.connect('store.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return render_template('index.html', products=products)

@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'admin123':
            session['admin'] = True
            return redirect('/admin')
    return render_template('login.html')

@app.route('/admin')
def admin():
    if not session.get('admin'):
        return redirect('/admin/login')
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return render_template('admin.html', products=products)

@app.route('/admin/add', methods=['POST'])
def add_product():
    if not session.get('admin'):
        return redirect('/admin/login')
    name = request.form['name']
    price = request.form['price']
    image = request.form['image']
    conn = get_db_connection()
    conn.execute('INSERT INTO products (name, price, image) VALUES (?, ?, ?)', (name, price, image))
    conn.commit()
    conn.close()
    return redirect('/admin')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/admin/login')

if __name__ == '__main__':
    if not os.path.exists('store.db'):
        conn = sqlite3.connect('store.db')
        conn.execute('CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, price TEXT, image TEXT)')
        conn.commit()
        conn.close()
    app.run(debug=True)
