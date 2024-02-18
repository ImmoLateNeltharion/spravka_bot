import sqlite3

from config.config import id_admin

conn = sqlite3.connect("database/database.db")
cur = conn.cursor()


def check_db():
    cur.execute("DROP TABLE debt")
    conn.commit()

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
            cur.execute("INSERT INTO admin (tg_id) VALUES (?)", (501916570,))
            conn.commit()
            cur.execute("INSERT INTO admin (tg_id) VALUES (?)", (594621468,))
            conn.commit()
            cur.execute("INSERT INTO admin (tg_id) VALUES (?)", (621485395,))
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
            cur.execute(
                "INSERT INTO operator (tg_id, count_orders, name) VALUES (501916570, 0, 'Коля')"
            )
            conn.commit()

            cur.execute(
                "INSERT INTO operator (tg_id, count_orders, name) VALUES (6214853985, 0, 'Андрей')"
            )
            conn.commit()

            cur.execute(
                "INSERT INTO operator (tg_id, count_orders, name) VALUES (1512412351, 0, 'Илья')"
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
                        sum INT,
                        address text
            )"""
            )
            conn.commit()
            cur.execute(
                "INSERT INTO orders (tg_id, sum, address) VALUES (5862149582, 5000, 'Ул. 1')"
            )
            conn.commit()

    try:
        cur.execute("SELECT * FROM debt")
    except sqlite3.OperationalError:
        print("Database debt does not exsist")
        if sqlite3.OperationalError:
            cur.execute(
                """CREATE TABLE debt(
                        id INTEGER PRIMARY KEY,
                        address text,
                        debt float
            )"""
            )
            conn.commit()
            cur.execute("INSERT INTO debt (address, debt) VALUES ('Ул. 1', 0)")
            conn.commit()
            cur.execute("INSERT INTO debt (address, debt) VALUES ('Ул. 2', 3000)")
            conn.commit()
    try:
        cur.execute("SELECT * FROM month")
    except sqlite3.OperationalError:
        print("Database month does not exsist")
        if sqlite3.OperationalError:
            cur.execute(
                """CREATE TABLE month(
                        id INTEGER PRIMARY KEY,
                        tg_id BIGINT,
                        month int
            )"""
            )
            conn.commit()
            cur.execute("INSERT INTO month (tg_id, month) VALUES (5862149582, 1)")
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


def add_order(id, sum, adr):
    cur.execute(
        "INSERT INTO orders (tg_id, sum, address) VALUES(?, ?, ?)", (id, sum, adr)
    )
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


def get_addr_order(id):
    cur.execute("SELECT address FROM orders WHERE tg_id = (?)", (id,))
    temp = cur.fetchall()
    return temp[0][0]


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


def add_debt(addr, debt):
    cur.execute("INSERT INTO debt (address, debt) VALUES(?, ?)", (addr, debt))
    conn.commit()


def get_debt(addr):
    cur.execute("SELECT debt FROM debt WHERE address = (?)", (addr,))
    temp = cur.fetchone()[0]
    return temp


def update_debt(addr, sum):
    cur.execute("UPDATE debt SET debt = (?) WHERE address = (?)", (sum, addr))
    conn.commit()


def check_adr(addr):
    cur.execute("SELECT id FROM debt WHERE address = (?)", (addr,))
    temp = cur.fetchall()
    if len(temp) == 0:
        return False
    else:
        return True


def add_month(id, month):
    cur.execute("INSERT INTO month (tg_id, month) VALUES(?, ?)", (id, month))
    conn.commit()


def get_month(id):
    cur.execute("SELECT month FROM month WHERE tg_id = (?)", (id,))
    temp = cur.fetchall()
    print(temp)
    cur.execute("DELETE FROM month WHERE tg_id = (?)", (id,))
    conn.commit()
    return temp[0][0]
