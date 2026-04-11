from playwright.sync_api import sync_playwright
import sqlite3
import time
import pandas as pd
class DataVault:
    def __init__(self,db_name = "category.db",url = "https://books.toscrape.com/"):
        self.db_name = db_name
        self.url = url
        self.create_table()
        
    def create_table(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS libary(
                           ID INTEGER PRIMARY KEY,
                           cate_gory TEXT,
                           title TEXT,
                           price REAL,
                           time TEXT
                       )
                       ''')
    def save_data(self, cate_gory , title , price):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        current_time = time.strftime("%Y %m %d- %H:%M:%S")
        cursor.execute('''
                       INSERT INTO libary(cate_gory,title,price,time)
                       VALUES(?,?,?,?)
                       ''',(cate_gory,title,price,current_time)
                       )
        conn.commit()
        print(f"✅ Đã cất vào két:")
    def play_wright_crawl(self):
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(self.url,timeout=30000)
                page.click("text='Travel'")
                page.wait_for_selector(".product_pod")
                products = page.locator(".product_pod").all()
                data = []
                for pro in products:
                    item ={
                        "title":pro.locator("h3 a").get_attribute("title"),
                        "price":pro.locator(".price_color").inner_text()
                    }
                    data.append(item)
                browser.close()
                return data
        except Exception as e:
            print(f"Error from sever {e}")
            return None
vault = DataVault()
raw_data = vault.play_wright_crawl()
if raw_data:
    for book in raw_data:
        clean_price = float(book['price'].replace("£",""))
        vault.save_data(cate_gory="Travel",title=book["title"],price=clean_price)
df = pd.DataFrame(raw_data)
print(df)
df['price'] = df['price'].str.replace('£', '').astype(float)
expensive_book = df.loc[df["price"].idxmax()]
print(f"Cuốn đắt nhất là: {expensive_book['title']} với giá {expensive_book['price']}")
cheapest_book = df.loc[df["price"].idxmin()]
print(f"Cuốn rẻ nhất là: {cheapest_book['title']} với giá {cheapest_book['price']}")
avg_price = df['price'].mean()
print(f'avt price {avg_price}')