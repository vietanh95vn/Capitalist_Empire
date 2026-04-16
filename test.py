import sqlite3
conn = sqlite3.connect("PhongVu_Tracker.db")
cursor = conn.cursor()
cursor.execute("DELETE FROM tablets")
conn.commit()
conn.close()