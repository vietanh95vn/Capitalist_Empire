import sqlite3
conn = sqlite3.connect("saas_database.db")
cursor = conn.cursor()
cursor.execute("DELETEM FROM client_data WHERE id = 1")
conn.commit()