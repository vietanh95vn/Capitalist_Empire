from playwright.sync_api import sync_playwright
from vault import Object
class ObjectScraper:
    def __init__(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=True)
        fake_user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        self.context = self.browser.new_context(
            user_agent= fake_user_agent,
            viewport={'width':1920,'height':1080},
            timezone_id="Asia/Ho_Chi_Minh",
            locale="en-US"
        )
        self.page = self.context.new_page()
        print("🎭 Đã kích hoạt Giao thức Ngụy trang. Dấu vân tay hệ thống đã bị xóa bỏ!")
    def clean_price(self,raw_price_string:str)->float:
        try:
            clean_str = raw_price_string.replace("VND","").replace(",","").replace("$","").strip()
            return float(clean_str)
        except Exception as e:
            print(f"Error {e}")
            return 0.0

    def fetch_data(self):
        print("🔍 Đang khởi động Mũi khoan Playwright...")
        scrap_data = []
        hot_deals = []
        try:
            self.page.goto("https://www.ebay.com/sch/i.html?_nkw=macbook+pro+m1",timeout=60000,wait_until="domcontentloaded")
            self.page.wait_for_selector(".s-card")
            table = self.page.locator(".s-card").all()
            for s in table:
                name_object = s.locator('.s-card__title').first.inner_text().replace("Opens in a new window or tab","").strip()
                if not name_object:
                    continue
                if "Shop on eBay" in name_object:
                    print("🗑️ Đã phát hiện và tiêu diệt Thẻ Quảng Cáo Trojan!")
                    continue
                name_lower = name_object.lower()
                blacklist = ["for parts", "not working", "broken", "cracked", "icloud", "locked", "mdm", "water damage", "read"]
                
                # Bước C: Kích hoạt Radar. Nếu Tên chứa BẤT KỲ từ nào trong blacklist -> Tiêu diệt!
                if any(bad_word in name_lower for bad_word in blacklist):
                    print(f"☢️ CẢNH BÁO PHẾ LIỆU! Đã chặn hàng hỏng: {name_object}")
                    continue
                # syntax get text and if have Opens is a new window or table replace it with nothing , and  strip delete all space
                price_object = s.locator('.s-card__price').first.inner_text() # syntax get price with class s-card__price
                clean_val  = self.clean_price(price_object) # call action clean_price() we built on top 
                print(f"📦 Lấy được: {name_object} | Giá thô: {price_object}")
                
                
                
                new_product = Object(name= name_object,price= clean_val)
                scrap_data.append(new_product)
                market_median = 10500000
                desired_margin = 500000
                max_buy_price = market_median - desired_margin
                min_real_price = 6000000
                
                if min_real_price <= clean_val <= max_buy_price:
                    print(f"🚨 KÈO THƠM TẠI TRẬN! Giá: {clean_val}")
                    hot_deals.append(new_product)
                
            else:
                print(f"➖ Hàng thường/Không đủ Margin: {clean_val}. Im lặng bỏ qua.")
            return scrap_data , hot_deals
        except Exception as e:
            print(f"❌ Lỗi: {e}")
    def stop_engine(self):
        """Công tắc dọn dẹp tài nguyên sau khi cào xong"""
        try:
            self.context.close()
            self.browser.close()
            self.playwright.stop()
            
            print("🛑 Đã tắt Động cơ Playwright và giải phóng RAM an toàn!")
        except Exception as e:
            print(f"⚠️ Lỗi khi tắt động cơ: {e}")
    