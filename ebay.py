from playwright.sync_api import sync_playwright
import sqlite3
import time
import requests
from config import CHAT_ID , key_telegram
class Object: #tạo một class object 
    def __init__(self,name,price,): # truyền name và price vào global varible
        self.name = name # set self name
        self.price = price # set self price
class DataObject: # create a class contaitn data of Object 
    def __init__(self,db_name = "ebay.db"): #create e file ebay.db is a vault
         self.db_name = db_name # khai báo dbname
         self.create_table() # funtion create table (acction)
    def create_table(self): # action create table
        conn = sqlite3.connect(self.db_name) # syntax connect to vault
        cursor = conn.cursor() # magicpen
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS data_ebay(
                           id INTEGER PRIMARY KEY,
                           name TEXT,
                           price REAL,
                           time TEXT
                       )
                       ''')
        # If table not exist so create a table name data_ebay with colum id , name ,price , time
        conn.commit() # end of the action put data
        conn.close() # close action
    def save_data(self, data : Object): #function save_data connect to object contain "name and price"
        conn = sqlite3.connect(self.db_name) # syntax to connect data vault
        cursor = conn.cursor() # pen magic
        current_time = time.strftime("%Y-%m-%d %H:%M:%S") # set current time GT +0
        cursor.execute('''
                       INSERT INTO data_ebay(name , price , time)
                       VALUES(?,?,?)
                       ''',(data.name,data.price,current_time)
                       )
        # syntax execute add value in data  vault with 3 values , name , price , time 
        conn.commit() # end of the action put data
        conn.close() # after put data need closing data 
        print(f"DataBase has saved {data.name} in to the Vault")
    def get_last_price(self, name_product): # funtion find the last price data in vault 
     
        conn = sqlite3.connect(self.db_name) # connect data value (data_ebay)
        cursor = conn.cursor() # pen magic
        cursor.execute('''
            SELECT price FROM data_ebay 
            WHERE name = ? 
            ORDER BY time DESC 
            LIMIT 1
        ''', (name_product,))
        # choice colume Price want to fetch with condition WHERE m ORDER BY time EDESC LIMIT 1 is arrange in order follow time add to data vault  và chọn nhưng kết quả mới nhất
        # 3. Chụp lấy kết quả
        result = cursor.fetchone() # Choice price chỉ chọn giá trị đầu tiên
        conn.close() # after do the action need to close vault
        
      
        if result: # condition if result is exit so return float result[0]
            return float(result[0]) 
        else:
            return None # return none is result is empty or error or Zero
class ObjectScaper: # Create class Onject scaper the place use playwright to crawl data
    def __init__(self): 
        self.playwright = sync_playwright().start() # syntax start playwright
        self.browser = self.playwright.chromium.launch(headless=True) # choice browser chromium.launch ( headless = True is run in silent , background processes)
        fake_user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        my_proxy = {
            "server":"209.38.154.7:1080"
            
        }
        self.context = self.browser.new_context( # set proxy
            user_agent= fake_user_agent,
            viewport={"width":1920,'height':1080}, # size viewport of browser
            timezone_id="Asia/Ho_Chi_Minh", # time zone
            locale="en-US" # language
        )
        self.page = self.context.new_page() # run in new page 
        print("🎭 Đã kích hoạt Giao thức Ngụy trang. Dấu vân tay hệ thống đã bị xóa bỏ!")
    def clean_price(self,raw_price_string): # clean the price after we got raw price 
        try:
            clean_str = raw_price_string.replace("VND","").replace(",","").replace("$","").strip() # delete VND , "," , % in data 
            return float(clean_str) # focus string to float
        except Exception as e: # if trap return eror
            print(f"Error {e}")
            return 0.0
    def fetch_data(self): # Place crawl dataa 
        print("🔍 Đang khởi động Mũi khoan Playwright...")
        scrap_data = [] # create a list contant all data
        hot_deals = [] # data with good price 
        try:
            self.page.goto("https://www.ebay.com/sch/i.html?_nkw=macbook+pro+m1",timeout= 60000, wait_until="domcontentloaded") #  link URL want to go , with timeout = 60000 if out of 60000 return error , wait_ultil = "domcontentloaded" main syntax
            self.page.wait_for_selector(".s-card") # chờ cho đến khi cả cái trang đó hiệ nra hết 
            table = self.page.locator(".s-card").all() # get all element in class s-card
            for s in table: # loop throw in talbe and try to get name , price 
                name_object = s.locator('.s-card__title').first.inner_text().replace("Opens in a new window or tab","").strip()
                if not name_object:  # if can't get name object or error skip it 
                    continue # skip
                if "Shop on eBay" in name_object: # avoid ads 
                    print("🗑️ Đã phát hiện và tiêu diệt Thẻ Quảng Cáo Trojan!")
                    continue # skip it
                name_lower = name_object.lower() 
                
                # Bước B: Định nghĩa Danh sách đen
                blacklist = ["for parts", "not working", "broken", "cracked", "icloud", "locked", "mdm", "water damage", "read"]
                
                # Bước C: Kích hoạt Radar. Nếu Tên chứa BẤT KỲ từ nào trong blacklist -> Tiêu diệt!
                if any(bad_word in name_lower for bad_word in blacklist):
                    print(f"☢️ CẢNH BÁO PHẾ LIỆU! Đã chặn hàng hỏng: {name_object}")
                    continue
                # syntax get text and if have Opens is a new window or table replace it with nothing , and  strip delete all space
                price_object = s.locator('.s-card__price').first.inner_text() # syntax get price with class s-card__price
                clean_val  = self.clean_price(price_object) # call action clean_price() we built on top 
                print(f"📦 Lấy được: {name_object} | Giá thô: {price_object}")
                

                
                new_product = Object(name= name_object,price= clean_val) # set new_prodcut and connect class Onject containt name and price
                scrap_data.append(new_product) # add to list scrap_data contain all data crawl form playwright
                market_median = 10500000 # 10.5M VNDc # set median
                desired_margin = 500000  # 500k VND # set margin 
                max_buy_price = market_median - desired_margin  # 10.0M VND
                min_real_price = 6000000  # 6.0M VND
            
                if min_real_price <= clean_val <= max_buy_price: # conditian 
                    # NẾU NGON -> KÉO CÒI BÁO ĐỘNG!
                    print(f"🚨 KÈO THƠM TẠI TRẬN! Giá: {clean_val}")
                    hot_deals.append(new_product) # add to hot deal the place only send text , message to Telegram
                    # LƯU Ý: Chỗ này cậu sẽ dùng bot.send_report() nếu cậu đã truyền biến bot vào đây.
                    #bot.send_report(f"KÈO NGON: {name_object} - Giá: {clean_val}")
                else:
                    # NẾU ĐẮT HOẶC QUÁ RẺ (RÁC) -> IM LẶNG BỎ QUA, KHÔNG SPAM TELEGRAM!
                    print(f"➖ Hàng thường/Không đủ Margin: {clean_val}. Im lặng bỏ qua.")
            return scrap_data , hot_deals
        except Exception as e:
            print(f"❌ Lỗi: {e}")
            return []
class TelegramNotifier: # config Telegram bot
    def __init__(self,token , chat_id):
        self.token = token
        self.chat_id =chat_id
        self.api_url = f"https://api.telegram.org/bot{self.token}/sendMessage"
    def send_report(self,list_item):
        report = "Report Object On eBay\n" + "0" + "\n"
        for s in list_item[:10]: # make title more short because telegram just contain 2500 character we find list item 0-10
            short_name = s.name[:50]+"...." if len(s.name)> 50 else s.name
            report += f"{short_name} : {s.price}\n"
        pay_load = {
            "chat_id":self.chat_id,
            "text": report
        }
        try:
            response = requests.post(self.api_url , data= pay_load) # use post not use  get for telegram
            if response.status_code == 200: # check trap error
                
                print("🚀 TELEGRAM: Đã bắn tin nhắn báo cáo thành công!")
            else:
                print(f"❌ LỖI API TELEGRAM: {response.text}")
        except Exception as e:
            print(f"❌ LỖI TELEGRAM: Không thể bắn tin nhắn! {e}")
            
        
def main():
    

    print("🚀 BẮT ĐẦU CHUỖI KHỞI ĐỘNG HỆ THỐNG...")
    scraper = ObjectScaper() # set varible connect object scaper
    db = DataObject() # set varible connect Data onject
    bot = TelegramNotifier(token=key_telegram,chat_id=CHAT_ID) # set varible connect TelegramNotifier    
    print("⚡ Kích hoạt Mũi khoan Playwright...")
    # CHỈ GỌI FETCH_DATA 1 LẦN DUY NHẤT! Hứng 2 cái giỏ.
    all_data, vip_deals = scraper.fetch_data() # call all_data and vip_deals contain in one time we crawl data
    
    # 1. XỬ LÝ GIỎ HÀNG THƯỜNG (LƯU VÀO KÉT SẮT SQL)
    if all_data and len(all_data) > 0: # process normal data with condition if > 0 is not empty
        print(f"🎯 Đã tóm được {len(all_data)} mục tiêu. Bắt đầu đẩy vào Data Lake!")
        for item in all_data:
            db.save_data(item) # Lặp qua từng món và lưu lại! Không ném cả giỏ! 
        print("💾 Đã lưu xong toàn bộ sản phẩm vào Data Lake.")
    else:
        print("⚠️ Không lấy được dữ liệu nào từ Mũi khoan.")

    # 2. XỬ LÝ GIỎ HÀNG VIP (BẮN TELEGRAM)
    if vip_deals and len(vip_deals) > 0:
        print(f"📱 Có {len(vip_deals)} kèo thơm! Đang gọi Telegram báo động...")
        bot.send_report(vip_deals) # Hàm send_report ĐÃ ĐƯỢC THIẾT KẾ ĐỂ NHẬN LIST, nên truyền cả giỏ là ĐÚNG!
    else:
        print("🔕 Không có kèo thơm nào trong chu kỳ này. Telegram tiếp tục ngủ.")
def run_forever():

    print("⚙️ KÍCH HOẠT ĐỘNG CƠ TỰ ĐỘNG HÓA VÔ CỰC...")
    cycle = 1
    while True:
        print(f"\n" + "="*50)
        print(f"🚀 BẮT ĐẦU CHU KỲ QUÉT SỐ {cycle}")
        print("="*50)
        try :
            main()
            print("\n⏳ Chu kỳ hoàn tất. Cỗ máy đi ngủ 60 phút")
            time.sleep(3600)
            cycle += 1
        except Exception as e:
            print(f"🔥 LỖI CHÍ MẠNG TRONG CHU KỲ {cycle}: {e}")
            print("⏳ Cỗ máy bị vấp! Chờ 5 phút rồi tự động thử lại...")
            time.sleep(300) #"
if __name__ == "__main__":
    # ĐỪNG GỌI MAIN NỮA, GỌI ĐỘNG CƠ VĨNH CỬU!
    run_forever()