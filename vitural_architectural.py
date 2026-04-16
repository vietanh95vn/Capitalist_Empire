import sqlite3
import requests
import time
from datetime import datetime
from urllib.parse import urljoin
from curl_cffi import requests
from config import CHAT_ID
from key_telegram import TOKEN
# ==========================================
# MODULE 1: THE INFILTRATOR (CrawData)
# ==========================================
class CrawlData:
    def __init__(self):
        # ⚠️ ARCHITECT'S TRAP: Đây là API giả định. Cậu phải tự tìm API thật trong tab HEADERS!
        self.api_url = "https://discovery.tekoapis.com/api/v2/search-skus-v2"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0",
            "Accept": "application/json"
        }
        # ⚠️ ARCHITECT'S TRAP: Đây là Payload giả định. Cậu phải tự copy từ tab PAYLOAD!
        self.payload = {
            "terminalId": 4, # Quan trọng: Phân biệt nền tảng (Web/App)
            "page": 1,
            "pageSize": 40,
            "slug": "/c/may-tinh-bang",
            "filter": {},
            "isNeedFeaturedProducts": True,
            "returnFilterable": [],
            "sorting": {
                "sort": "SORT_BY_CREATED_AT",
                "order": "ORDER_BY_DESCENDING"
            }
        }

    def fetch_tablets(self):
        try:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 🚀 Bắn tín hiệu chọc thủng API Phong Vũ...")
            # Sử dụng POST hoặc GET tùy thuộc vào method cậu thấy trong tab Headers
            res = requests.post(self.api_url, headers=self.headers, json=self.payload, timeout=(5,15), impersonate="chrome110")
            res.raise_for_status()
            
            # Phân tích JSON. Đường dẫn này phụ thuộc vào cấu trúc thực tế của Phong Vũ.
            # Dựa vào ảnh cậu gửi, nó có vẻ nằm trong: res.json().get('result', {}).get('products', [])
            # Tôi sẽ viết logic cơ bản, cậu phải tự điều chỉnh Key JSON!
            raw_data = res.json()
            # ⚠️ GẮN MÁY QUÉT TIA X VÀO ĐÂY ĐỂ XEM PHONG VŨ TRẢ VỀ CÁI GÌ!
            print(f"🔍 [X-RAY API RESPONSE]: {raw_data}")
            # Giả định data nằm trong raw_data['result']['products']
            return raw_data.get("data", {}).get("products", [])

        except requests.exceptions.RequestException as e:
            print(f"❌ [LỖI MẠNG]: API sập hoặc chặn truy cập: {e}")
            return []
        except ValueError:
            print("❌ [LỖI JSON]: Phản hồi không phải là JSON!")
            return []
        except Exception as e:
            print(f"❌ [LỖI HỆ THỐNG CÀO]: {e}")
            return []

# ==========================================
# MODULE 2: THE VAULT (SaveData)
# ==========================================
class SaveData:
    def __init__(self, db_name="PhongVu_Tracker.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS tablets (
            id TEXT PRIMARY KEY,
            name TEXT,
            price REAL,
            timestamp TEXT
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def save_bulk_data(self, product_list):
        # Bẫy lỗi trùng lặp: INSERT OR IGNORE
        query = "INSERT OR IGNORE INTO tablets (id, name, price, timestamp) VALUES (?, ?, ?, ?)"
        try:
            # Máy dập thủy lực: Thực thi toàn bộ list trong 1 thao tác
            cursor = self.conn.executemany(query, product_list)
            self.conn.commit()
            return cursor.rowcount # Trả về số lượng bản ghi MỚI thực sự được thêm vào
        except Exception as e:
            print(f"❌ [LỖI DATABASE]: {e}")
            return 0

# ==========================================
# MODULE 3: THE MESSENGER (TelegramNotice)
# ==========================================
class TelegramNotice:
    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id

    def send_report(self, message):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        payload = {"chat_id": self.chat_id, "text": message, "parse_mode": "HTML"}
        try:
            res = requests.post(url, json=payload)
            if res.status_code != 200:
                print(f"❌ [TELEGRAM REJECTED]: {res.text}")
        except Exception as e:
            print(f"❌ [KHÔNG BẮN ĐƯỢC MESSAGE]: {e}")

# ==========================================
# THE ORCHESTRATOR (MAIN LOOP)
# ==========================================
if __name__ == "__main__":

    crawler = CrawlData()
    vault = SaveData()
    notifier = TelegramNotice(TOKEN, CHAT_ID)

    print("⚙️ KÍCH HOẠT CỖ MÁY SĂN HÀNG PHONG VŨ (10 PHÚT/LẦN)...")

    while True:
        products = crawler.fetch_tablets()
        
        if products:
            db_batch = []
            alert_items = []

            for p in products:
                # Trích xuất dữ liệu dựa vào cấu trúc JSON thật (Cậu phải tự soi ảnh chụp của cậu)
                p_id = str(p.get("sku", "UNKNOWN"))
                name = p.get("name", "Unknown Product")
                brand = p.get("brandName", "Unknown Brand") # +1 
                
                # Logic xử lý giá: Lấy latestPrice, nếu null thì = 0.0
                raw_price = p.get("latestPrice")
                price = float(raw_price) if raw_price else 0.0
                # 3. TRÍCH XUẤT VÀ CHUẨN HÓA URL (URL NORMALIZATION)
                canonical_path = p.get("canonical", "")
                # urljoin sẽ tự động xử lý dấu "/" thừa hoặc thiếu. Tuyệt đối an toàn! #+1
                full_url = urljoin("https://phongvu.vn/", canonical_path)
                
                # Chuẩn bị Data cho DB
                db_batch.append((p_id, name, price, datetime.now().isoformat()))

                # Nếu là hàng ngon (Ví dụ: Dưới 5,000,000 VND)
                if price > 0 and price < 5000000:
                    alert_items.append(f"• [{brand}]- {name} - <b>{price:,.0f} VND</b>\n"
                                       f"  🔗 <a href='{full_url}'>Mở Website Phong Vũ</a>\n") #+1
                elif price == 0.0:
                    alert_items.append(f"• [{brand}] <b>{name}</b>\n"
                        f"  💰 Giá: Unknown Price\n"
                        f"  🔗 <a href='{full_url}'>Kiểm tra thủ công</a>\n")

            # Thực thi việc lưu trữ
            new_records_count = vault.save_bulk_data(db_batch)
            print(f"✅ Đã quét {len(products)} sản phẩm. Lưu mới: {new_records_count} sản phẩm.")

            # Nếu có sản phẩm mới VÀ có sản phẩm nằm trong danh sách báo động
            if new_records_count > 0 and alert_items:
                summary_msg = f"🔥 <b>BÁO CÁO PHONG VŨ MỚI!</b>\n\n" + "\n".join(alert_items)
                notifier.send_report(summary_msg)
            else:
                print("💤 Không có kèo mới. Hệ thống im lặng để chống Spam.")

        else:
            print("⚠️ Không lấy được dữ liệu. Kiểm tra lại API Endpoint hoặc Payload.")

        # Ngủ 10 phút (600 giây)
        time.sleep(600)