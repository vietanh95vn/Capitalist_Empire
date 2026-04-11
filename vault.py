import sqlite3
import time
class Object:
    def __init__(self,name,price):
        self.name = name
        self.price =price
class DataObject:
    def __init__(self,db_name="ebay.db"):
        self.db_name = db_name
        self.create_table()
    def create_table(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS data_ebay(
                           id INTEGER PRIMARY KEY,
                           name TEXT,
                           price REAL,
                           time TEXT
                       )
                       ''')
        conn.commit()
        conn.close()
    def save_data(self , data:Object):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        current_time = time.strftime("%Y %m %d %H:%M:%S")
        cursor.execute('''
                       INSERT INTO data_ebay(name,price,time)
                       VALUES(?,?,?)
                       ''',(data.name,data.price,current_time))
        conn.commit()
        conn.close()
        print(f"DataBase has saved {data.name} in to the Vault")
    def get_last_price(self, name_product):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
                       SELECT price FROM data_ebay
                       WHERE name = ?
                       ORDER BY time DESC
                       LIMIT 1
                       ''',(name_product,))
        result = cursor.fetchone()
        conn.close()
        if result:
            return float(result[0])
        else:
            return None
