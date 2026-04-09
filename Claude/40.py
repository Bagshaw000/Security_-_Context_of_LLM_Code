import sqlite3

conn = sqlite3.connect('bicycle_shop.db')
c = conn.cursor()

c.execute()

c.execute()

c.execute()

conn.commit()
conn.close()