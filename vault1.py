import sqlite3
import time

class EventObject:
    def __init__(self,name:str,date_time:str,location:str,price:str,event_url:str):
        self.name = name
        self.date_time = date_time
        self.location = location
        self.price = price
        self.event_url = event_url
       
class EventDataBase:
    def __init__(self,db_name ="event_object.db"):
        self.db_name = db_name
    def create_table(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS data_event(
                           id INTEGER PRIMARY KEY,
                           name TEXT,
                           price TEXT,
                           location TEXT,
                           date_time TEXT,
                           url_event TEXT,
                           time TEXT
                       )
                       ''')
        conn.commit()
        conn.close()
    def save_data(self,event:EventObject):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
                       INSERT INTO data_event(name,price,location,date_time,url_event,time)
                       VALUES(?,?,?,?,?,?)
                       ''',(event.name,event.price,event.location,event.date_time,event.event_url,current_time))
        conn.commit()
        conn.close()