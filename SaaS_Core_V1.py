import sqlite3
import time
from playwright.sync_api import sync_playwright
from key_telegram import TOKEN
import telebot
class DataVault:
    def __init__(self,data = "saas_core_v1.db"):
        self.data = data
        self.create_table()
    def create_table(self):
        conn = sqlite3.connect(self.data)
        cursor = conn.cursor()
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS client_data(
                           id INTEGER PRIMARY KEY,
                           chat_id INTEGER,
                           url TEXT,
                           title TEXT,
                           price REAL,
                           time TEXT
                       )
                       ''')
    def save_data(self,chat_id, url, title, price):
        conn = sqlite3.connect(self.data)
        cursor = conn.cursor()
        current_time = time.strftime("%Y %m %d - %H:%M:%S")
        cursor.execute('''
                       INSERT INTO client_data(chat_id,url,title,price,time)
                       VALUES(?,?,?,?,?)
                       ''',(chat_id,url,title,price,current_time))
        conn.commit()
        print(f"✅ Đã cất vào két:")
    def get_all_urls(self):
        conn = sqlite3.connect(self.data)
        cursor = conn.cursor()
        # Lệnh SELECT lấy cột url
        cursor.execute("SELECT url FROM client_data")
        rows = cursor.fetchall() # Lấy toàn bộ kết quả
        conn.close()
        
        # SQL trả về một List các Gói hàng (Tuple), ví dụ: [('link1',), ('link2',)]
        # Dòng này để bóc cái List đó ra thành các link sạch sẽ: ['link1', 'link2']
        list_link = [row[0] for row in rows] 
        return list_link
    def get_old_data(self,url):
        conn = sqlite3.connect(self.data)
        cursor = conn.cursor()
        cursor.execute(
                       "SELECT price FROM client_data WHERE url = ?",(url,)
                       )
        result = cursor.fetchone()
        conn.close()
        if result is not None:
            return result[0]
        return 0
    def update_price(self,url,new_price):
        conn = sqlite3.connect(self.data)
        cursor = conn.cursor()
        current_time = time.strftime("%Y %h %d - %H:%M:%S")
        cursor.execute('''
                       UPDATE client_data
                       SET price = ? , time = ?
                       WHERE url = ?
                       ''',(new_price,current_time,url))
        conn.commit()        
#Playwright crawl data       
def crawl_data(url_target):
    try:
        with sync_playwright() as p:
            brower = p.chromium.launch(headless=True)
            page = brower.new_page()
            page.goto(url_target,timeout= 30000)
            text_price = page.locator("p.price_color").first.inner_text()
            float_price = float(text_price.replace("£",""))
            name_data = page.locator(".product_main h1").inner_text()
            brower.close()
            return float_price,name_data
    except Exception as e:
        print(f"Error {e}")
        return None
    
    
    
    
    
bot = telebot.TeleBot(TOKEN)
ket_sat_saas = DataVault()
@bot.message_handler(commands=['track'])
def handle_track_command(message):
    chat_id = message.chat.id
    text = message.text # Lấy toàn bộ tin nhắn (Ví dụ: "/track https://link...")
    parts = text.split(" ")
    if len(parts) < 2: # Nếu số lượng mảnh ghép ít hơn 2 (nghĩa là không có link)
        bot.reply_to(message, "⚠️ Lỗi: Sai cú pháp. Hãy gõ /track [Link_Sách]")
        return 
    
    url_target = parts[1] # Nếu an toàn rồi mới được lấy link
    
    # Kiểm tra xem link có trống không
    if url_target == "/track":
        bot.reply_to(message, "⚠️ Lỗi: Sai cú pháp. Hãy gõ /track [Link_Sách]")
        return # Dừng lại luôn
        

    if "books.toscrape.com" not in url_target:
        bot.reply_to(message, "⚠️ Lỗi: Tao chỉ nhận link của trang books.toscrape.com thôi!")
        return # Dừng lại luôn
        
    bot.reply_to(message, f"✅ Đã nhận lệnh! Đang cử Điệp viên đến: {url_target}")
    
    ket_qua = crawl_data(url_target)
    if ket_qua is not None:
        gia_tien,ten_sach = ket_qua
        ket_sat_saas.save_data(chat_id,url_target,ten_sach ,gia_tien)
        bot.reply_to(message,f"✅Cướp thành công!\n👉 Giá hiện tại và tên sách {ten_sach} : £{gia_tien}\n💾Đã lưu vào Két sắt SaaS của ngài!")
    else:
        bot.reply_to(message,"❌ Điệp viên tử trận! Không thể lấy được giá. Web có thể đang sập.")
print("Dây chuyền Lắp ráp SaaS đã hoàn tất. Chờ lệnh từ Telegram...")


@bot.message_handler(commands=['kiemtra_toanbo'])
def handle_kiemtra_command(message):
    bot.reply_to(message, "⏳ Đang trích xuất dữ liệu Két Sắt và cử Điệp viên đi tuần tra...")
    
    # BƯỚC 1: Gọi Kế toán lấy danh sách
    danh_sach_link = ket_sat_saas.get_all_urls()
    
    if len(danh_sach_link) == 0:
        bot.reply_to(message, "⚠️ Két sắt trống rỗng! Không có mục tiêu nào để tuần tra.")
        return

    # BƯỚC 2: Chuẩn bị Cuốn sổ tay (Dict)

    bao_cao_gia = {}
    # BƯỚC 3: Xua Điệp viên đi cào (Vòng lặp For)
    for link in danh_sach_link:
        ket_qua = crawl_data(link)
        if ket_qua is not None:
            gia_tien, ten_sach = ket_qua
            gia_cu =ket_sat_saas.get_old_data(link)
            if gia_tien < gia_cu:
                trang_thai = f"📉 GIẢM (Cũ: £{gia_cu})"
            elif gia_tien > gia_cu:
                trang_thai = f"📈 TĂNG (Cũ: £{gia_cu})"
            else:
                trang_thai = "➖ Giữ nguyên"
            bao_cao_gia[ten_sach] = f"{gia_tien} [{trang_thai}]"
            ket_sat_saas.update_price(link,gia_tien)
    loi_nhan = "📊 BÁO CÁO BIẾN ĐỘNG TỪ KÉT SẮT:\n"
    loi_nhan += "----------------------------\n"
    for ten, gia_va_trang_thai in bao_cao_gia.items():
        loi_nhan += f"📖 {ten} --- {gia_va_trang_thai}\n"
        
    bot.reply_to(message, loi_nhan)     
bot.polling()       


    