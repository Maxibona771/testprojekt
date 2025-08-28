from flask import Flask, request, redirect, url_for
import sqlite3   # ✅ Вместо psycopg2 используем sqlite3
import os

importer = Flask(__name__)

DB_FILE = "database.db"  # ✅ SQLite хранит данные в файле

# Функция подключения (здесь проще, чем в PostgreSQL)
def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # ✅ Чтобы удобно работать с колонками по имени
    return conn

# Создаём таблицу, если её ещё нет
def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL
        );
    """)
    conn.commit()
    conn.close()

# Маршрут для получения списка пользователей
@importer.route("/users", methods=["GET"])
def get_users():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, username, email FROM users;")
    rows = cur.fetchall()
    conn.close()

    users_list = "<br>".join([f"{row['id']} | {row['username']} | {row['email']}" for row in rows])

    form_html = """
    <hr>
    <h3>Добавить пользователя</h3>
    <form method="POST" action="/users">
      Имя: <input name="username" required><br>
      Email: <input name="email" required><br>
      <input type="submit" value="Добавить">
    </form>
    """
    return users_list + form_html

# Маршрут для добавления пользователя
@importer.route("/users", methods=["POST"])
def add_user():
    username = request.form.get("username")
    email = request.form.get("email")

    if not username or not email:
        return "Ошибка: не заполнены обязательные поля", 400

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username, email) VALUES (?, ?);", (username, email))
    conn.commit()
    conn.close()

    return redirect(url_for('get_users'))

# Запуск сервера Flask
if __name__ == '__main__':
    init_db()  # ✅ Инициализация базы при старте
    importer.run(host='0.0.0.0', port=5000)
