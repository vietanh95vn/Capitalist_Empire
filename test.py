import sqlite3

conn = sqlite3.connect("ebay.db")
cursor = conn.cursor()
cursor.execute("DELETE FROM data_ebay")
conn.commit()
conn.close()