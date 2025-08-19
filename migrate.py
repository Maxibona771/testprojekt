import psycopg2
import time

def connect_with_retry():
    while True:
        try:
            conn = psycopg2.connect(
                host="db",
                database="postgres",
                user="postgres",
                password="postgres"
            )
            return conn
        except Exception as e:
            print("Ошибка подключения:", e)
            time.sleep(1)

def run_migrations():
    conn = connect_with_retry()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username TEXT NOT NULL,
        email TEXT NOT NULL
    );
    """)

    # Можно добавить начальные данные, если нужно
    cur.execute("""
    INSERT INTO users (username, email)
    VALUES ('testuser', 'test@example.com')
    ON CONFLICT DO NOTHING;
    """)

    conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    run_migrations()
    print("Миграции выполнены")
