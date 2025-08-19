from flask import Flask, request, redirect, url_for
import psycopg2
import time

importer = Flask(__name__)

def connect_with_retry():
    while True:
        try:
            conn = psycopg2.connect(
                host="db",           # Имя хоста базы данных (docker-compose service)
                database="postgres", # Имя базы данных
                user="postgres",     # Пользователь базы данных
                password="postgres"  # Пароль
            )
            return conn
        except Exception as e:
            print("❌ Ошибка подключения:", e)
            time.sleep(1)

# Маршрут для проверки версии PostgreSQL
@importer.route("/version")
def version():
    conn = connect_with_retry()
    cur = conn.cursor()
    cur.execute("SELECT version();")
    result = cur.fetchone()
    cur.close()
    conn.close()
    return f"PostgreSQL версия: {result[0]}"

# Маршрут для получения списка пользователей (GET-запрос)
@importer.route("/users", methods=["GET"])
def get_users():
    conn = connect_with_retry()
    cur = conn.cursor()
    cur.execute("SELECT id, username, email FROM users;")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    # Возвращаем в виде простого текста с переносами строк
    users_list = "<br>".join([f"{row[0]} | {row[1]} | {row[2]}" for row in rows])
    
    # Добавляем простую HTML форму для добавления пользователя (будет отображаться на странице)
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

# Маршрут для добавления пользователя (POST-запрос)
@importer.route("/users", methods=["POST"])
def add_user():
    username = request.form.get("username")
    email = request.form.get("email")

    if not username or not email:
        return "Ошибка: не заполнены обязательные поля", 400

    conn = connect_with_retry()
    cur = conn.cursor()
    # Вставляем нового пользователя в таблицу
    cur.execute("INSERT INTO users (username, email) VALUES (%s, %s);", (username, email))
    conn.commit()
    cur.close()
    conn.close()

    # После добавления делаем редирект обратно на GET /users чтобы увидеть обновленный список
    return redirect(url_for('get_users'))

# Запуск сервера Flask
if __name__ == '__main__':
    # host=0.0.0.0 чтобы сервер был доступен извне контейнера
    importer.run(host='0.0.0.0', port=5000)
