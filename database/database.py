import sqlite3

from config.config import id_admin

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
                        tg_id BIGINT
            )"""
            )
            conn.commit()
            cur.execute("INSERT INTO admin (tg_id) VALUES (?)", (id_admin,))
            conn.commit()
    try:
        cur.execute("SELECT * FROM operator")

    except sqlite3.OperationalError:
        print("Database operator does not exsist")
        if sqlite3.OperationalError:
            cur.execute(
                """CREATE TABLE operator(
                        id INTEGER PRIMARY KEY,
                        tg_id BIGINT,
                        count_orders INT,
                        name text
            )"""
            )
            conn.commit()
    try:
        cur.execute("SELECT * FROM orders")

    except sqlite3.OperationalError:
        print("Database orders does not exsist")
        if sqlite3.OperationalError:
            cur.execute(
                """CREATE TABLE orders(
                        id INTEGER PRIMARY KEY,
                        tg_id BIGINT,
                        sum INT
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


def add_admin(id):
    cur.execute("INSERT INTO admin (tg_id) VALUES(?)", (id,))
    conn.commit()


def add_operator(name, id):
    cur.execute("INSERT INTO operator (name, tg_id) VALUES(?, ?)", (name, id))
    conn.commit()


def add_order(id, sum):
    cur.execute("INSERT INTO orders (tg_id, sum) VALUES(?, ?)", (id, sum))
    conn.commit()


def check_adm(id):
    cur.execute("SELECT id FROM admin WHERE tg_id = (?)", (id,))
    temp = cur.fetchall()
    if len(temp) == 0:
        return False
    else:
        return True


def check_order(id):
    cur.execute("SELECT id FROM orders WHERE tg_id = (?)", (id,))
    temp = cur.fetchall()
    if len(temp) == 0:
        return False
    else:
        return True


def delete_order(id):
    cur.execute("DELETE FROM orders WHERE tg_id = (?)", (id,))
    conn.commit()


def take_op():
    cur.execute("SELECT tg_id FROM operator ORDER BY count_orders")
    temp = cur.fetchall()
    return temp[0][0]


def get_sum(id):
    cur.execute("SELECT sum FROM orders WHERE tg_id = (?)", (id,))
    temp = cur.fetchall()
    return temp[0][0]
