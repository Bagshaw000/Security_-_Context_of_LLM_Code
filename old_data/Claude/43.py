import sqlite3


conn = sqlite3.connect('bicycle_shop.db')


cursor = conn.cursor()


cursor.execute()

cursor.execute()

cursor.execute()


conn.commit()
conn.close()