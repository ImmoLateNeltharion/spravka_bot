import sqlite3

conn = sqlite3.connect("database/database.db")
cur = conn.cursor()


def check_db():
    try:
        cur.execute("SELECT * FROM admin")

    except sqlite3.OperationalError:
        print("Database users does not exsist")
        if sqlite3.OperationalError:
            cur.execute(
                """CREATE TABLE admin(
                        id INTEGER PRIMARY KEY,
                        tg_id BIGINT,
                        name text
            )"""
            )
            conn.commit()


def sql_start():
    check_db()
    if conn:
        print("Успешное подключение к БД")
    else:
        print("Ошибка при подключении к БД")


def sql_stop():
    print("Закрываем БД")
    conn.close()


def add_admin(name, id):
    cur.execute("INSERT INTO admin (name, tg_id) VALUES(?, ?)", (name, id))
    conn.commit()

def check_adm(id):
    cur.execute("SELECT id FROM admin WHERE tg_id = (?)", (id))
    if len(cur.fetchone()[0]) == 0:
        return False
    else:
        return True
