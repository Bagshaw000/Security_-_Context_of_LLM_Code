import sqlite3
from sqlite3 import Error



def create_connection():
    conn = None
    try:
        conn = sqlite3.connect("bicycle.db")
        return conn
    except Error as e:
        print(e)



def create_table(conn):
    sql_create_bicycles_table = 

    try:
        cur = conn.cursor()
        cur.execute(sql_create_bicycles_table)
    except Error as e:
        print(e)



def insert_data(conn, make, model, year, price):
    sql_insert_data = 

    try:
        cur = conn.cursor()
        cur.execute(sql_insert_data, (make, model, year, price))
        conn.commit()
    except Error as e:
        print(e)



def select_data(conn):
    sql_select_all = 

    try:
        cur = conn.cursor()
        cur.execute(sql_select_all)
        rows = cur.fetchall()
        for row in rows:
            print(row)
    except Error as e:
        print(e)



def main():
    conn = create_connection()
    if conn is not None:
        create_table(conn)
        insert_data(conn, "Trek", "Road Bike", 2022, 1500.00)
        select_data(conn)
        conn.close()

if __name__ == "__main__":
    main()