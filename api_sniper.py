import os
import sqlite3
import requests
import re
from datetime import datetime


# ==========================================
# MODULE 1: THE COMMUNICATIONS WEAPON (TELEGRAM)
# ==========================================
class TelegramNotifier:
    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{self.token}/sendMessage"

    def send_alert(self, message):
        payload = {"chat_id": self.chat_id, "text": message, "parse_mode": "HTML"}
        try:
            res = requests.post(self.api_url, data=payload)
            if res.status_code == 200:
                print("🚀 [TELEGRAM] Đã bắn tin nhắn Cảnh báo thành công!")
            else:
                print(f"🔥 [TELEGRAM] Bắn xịt: {res.text}")
        except Exception as e:
            print(f"🔥 [TELEGRAM] Lỗi mạng: {e}")

# ==========================================
# MODULE 2: THE DATA VAULT (SQLITE)
# ==========================================
class EventDatabase:
    def __init__(self, db_name="capitalist_vault.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        # Tạo bảng nếu chưa có. ID là PRIMARY KEY để chống trùng lặp tuyệt đối!
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id TEXT PRIMARY KEY,
                name TEXT,
                date_time TEXT,
                location TEXT,
                price TEXT,
                url TEXT,
                scraped_at TEXT
            )
        ''')
        self.conn.commit()

    def save_event(self, event_data):
        
        try:
            self.cursor.execute('''
                INSERT INTO events (id, name, date_time, location, price, url, scraped_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                event_data['id'], event_data['name'], event_data['date_time'],
                event_data['location'], event_data['price'], event_data['url'],
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ))
            self.conn.commit()
            return True  # True nghĩa là Data MỚI, đã lưu thành công!
        except sqlite3.IntegrityError:
            return False # False nghĩa là Data CŨ, đã có trong Két sắt!

# ==========================================
# MODULE 3: THE EXTRACTION ENGINE (API SNIPER)
# ==========================================
class EventbriteSniper:
    def __init__(self):
        self.html_url = "https://www.eventbrite.com/d/ca--san-mateo/events/"
        self.api_url = "https://www.eventbrite.com/api/v3/destination/events/"
        self.headers = {
            "accept": "*/*",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

    def harvest_ids(self):
        print("🔍 [SNIPER] Đang cào ID từ HTML...")
        res = requests.get(self.html_url, headers=self.headers)
        matches = re.findall(r'"eventbrite_event_id":"(\d+)"', res.text)
        return ",".join(list(set(matches)))

    def snipe_data(self, id_string):
        if not id_string:
            return []
        print("🎯 [SNIPER] Đang bắn API lấy JSON Sạch...")
        params = {
            "event_ids": id_string,
            "expand": "primary_venue,ticket_availability",
            "page_size": "50"
        }
        res = requests.get(self.api_url, params=params, headers=self.headers)
        if res.status_code == 200:
            return res.json().get("events", [])
        return []

# ==========================================
# MODULE 4: THE SYSTEMS ORCHESTRATOR (BỘ CHỈ HUY)
# ==========================================
def run_capitalist_machine():
    print("⚙️ KHỞI ĐỘNG CỖ MÁY TƯ BẢN...\n")

    # 1. Hít Token từ Đám mây (Hoặc thay bằng file config nếu chạy Local)
    TOKEN = os.environ.get("TOKEN", "ĐIỀN_TOKEN_CỦA_CẬU_NẾU_CHẠY_LOCAL")
    CHAT_ID = os.environ.get("CHAT_ID", "ĐIỀN_CHAT_ID_CỦA_CẬU_NẾU_CHẠY_LOCAL")

    # 2. Khởi tạo các Đối tượng OOP
    sniper = EventbriteSniper()
    vault = EventDatabase()
    bot = TelegramNotifier(token=TOKEN, chat_id=CHAT_ID)

    # 3. Chuỗi cung ứng Dữ liệu (The Data Pipeline)
    id_payload = sniper.harvest_ids()
    raw_events = sniper.snipe_data(id_payload)

    new_events_count = 0

    for event in raw_events:
        # --- CHUẨN HÓA DỮ LIỆU ---
        event_id = event.get("id")
        name = event.get("name", "Unknown Name")
        url = event.get("url", "No Link")
        
        start_date = event.get("start_date", "")
        start_time = event.get("start_time", "")
        date_time = f"{start_date} {start_time}".strip()
        
        try:
            location = event["primary_venue"]["name"]
        except KeyError:
            location = "Unknown Venue"

        try:
            raw_price = event["ticket_availability"]["minimum_ticket_price"]["display"]
            price = "Free" if "0.00" in raw_price else raw_price
        except (KeyError, TypeError):
            price = "Unknown"

        # Đóng gói thành Dictionary
        clean_data = {
            "id": event_id, "name": name, "date_time": date_time,
            "location": location, "price": price, "url": url
        }

        # --- LOGIC CHỐNG SPAM ---
        # Thử nhét vào Két sắt. Hàm save_event sẽ trả về True nếu là sự kiện mới tinh.
        is_new = vault.save_event(clean_data)

        if is_new:
            new_events_count += 1
            print(f"✅ Đã lưu MỚI: {name} | Giá: {price}")
            
            # CHỈ bắn Telegram nếu là sự kiện MỚI và MIỄN PHÍ
            if price == "Free":
                alert_msg = (
                    f"🚨 <b>SỰ KIỆN MIỄN PHÍ MỚI!</b> 🚨\n\n"
                    f"🎯 <b>Tên:</b> {name}\n"
                    f"⏰ <b>Giờ:</b> {date_time}\n"
                    f"📍 <b>Nơi:</b> {location}\n"
                    f"🔗 {url}"
                )
                bot.send_alert(alert_msg)

    print(f"\n🛑 HOÀN TẤT! Cào {len(raw_events)} sự kiện. Phát hiện {new_events_count} sự kiện mới.")

# KÍCH NỔ
if __name__ == "__main__":
    run_capitalist_machine()