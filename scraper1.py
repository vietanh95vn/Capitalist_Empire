import os
from playwright.sync_api import sync_playwright
from vault1 import EventObject,EventDataBase
from telebot1 import TelegramNotifier

TOKEN = os.environ.get("TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
if not TOKEN:
    from key_telegram import TOKEN
    from config import CHAT_ID
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
    def fetch_data(self):
        print("🔍 Đang khởi động Mũi khoan Playwright...")
        db = EventDataBase()
        db.create_table()
        try:
            self.page.goto("https://www.eventbrite.com/d/ca--san-mateo/events/",timeout=60000,wait_until="domcontentloaded")
            print(self.page.title())
            event_cards = self.page.locator(".discover-vertical-event-card").all()
            print(f"🎯 Đã khóa mục tiêu: {len(event_cards)} sự kiện trên trang!\n")

            
            for index, card in enumerate(event_cards[:55]):
                print(f"--- ĐANG MỔ XẺ SỰ KIỆN THỨ {index + 1} ---")
                
                # BƯỚC 3: ĐÂM MŨI KHOAN *VÀO BÊN TRONG* TỪNG CARD
                # Tìm thẻ <h3> duy nhất trong Card này
                title = card.locator("h3").inner_text()
                # THE SNIPER RIFLE: TÌM THẺ SPAN CHỨA CHỮ "follower"
                # (Dùng chữ thường "follower" để nó bắt được cả "1 follower" lẫn "47 followers")
                follower_locator = card.locator("span", has_text="follower")
                
                # THE RADAR: KIỂM TRA SỰ TỒN TẠI TRƯỚC KHI CÀO
                if follower_locator.count() > 0:
                    # Nếu tìm thấy ít nhất 1 thẻ, lấy thẻ đầu tiên (.first) và rút chữ
                    followers = follower_locator.first.inner_text()
                else:
                    # Nếu đếm = 0 (không tìm thấy), tự động gán giá trị mặc định
                    followers = "0 followers"
            
                print(f"Tên: {title}")
                
                # THE HACK: Lấy toàn bộ nội dung của các thẻ <p> NẰM TRONG CARD NÀY
                # .all_inner_texts() sẽ trả về một List các chuỗi văn bản
                p_texts = card.locator("p").all_inner_texts()
                p_texts.append(followers)
                date_time = "Unknown"
                location = "Unknown"
                price = "Unknown"

                # 1. KHAI BÁO TỪ ĐIỂN RÁC (BLACK LIST)
                # Cậu thấy web có từ rác nào mới, cứ ném thêm vào đây!
                junk_words = ["sales end", "promoted", "almost full", "going fast", "sales end soon","followers","check ticket"]

                for text in p_texts:
                    text = text.strip()
                    if not text: # Bỏ qua chuỗi rỗng
                        continue 
                    
                    # 2. KIỂM TRA QUÉT RÁC BẰNG HÀM ANY() VÀ LIST COMPREHENSION
                    # "Nếu BẤT KỲ (any) từ rác nào có mặt trong văn bản (text.lower()) -> Bỏ qua (continue)"
                    if any(junk in text.lower() for junk in junk_words):
                        continue
                    
                    # 3. BỘ LỌC CHÍNH (MAIN FILTERS)
                    if "$" in text or "Free" in text:
                        price = text
                    elif " AM" in text or " PM" in text or "•" in text:
                        date_time = text
                    

                    else:
                        if location == "Unknown":
                        # Rác đã bị lọc sạch ở trên. 
                        # Đã loại trừ Giá và Thời gian.
                        # Thứ còn sót lại ĐÍCH THỊ là Địa điểm (hoặc Tên Ban tổ chức)!
                            location = text
                    try:
                            # Lấy link href từ thẻ a đầu tiên
                        event_url = card.locator("a").first.get_attribute("href") 
                    except:
                        event_url = "No Link" 
                    # In cái List này ra để nghiên cứu xem dữ liệu Thời gian, Địa điểm, Giá nằm ở Index số mấy!
                print(f"Dữ liệu các thẻ P: {p_texts}\n")
                    # BƯỚC 4: RULE-BASED ARRAY PARSING V2 (ĐỘNG CƠ DANH SÁCH ĐEN)
                event_container = EventObject(name=title,date_time=date_time,location=location,price=price,event_url=event_url)
                
                db.save_data(event_container)
                if "Free" in event_container.price.lower():
                    alert_msg= (f"🚨 <b>PHÁT HIỆN SỰ KIỆN MIỄN PHÍ!</b> 🚨\n\n"
                            f"🎯 <b>Tên:</b> {event_container.name}\n"
                            f"⏰ <b>Thời gian:</b> {event_container.date_time}\n"
                            f"📍 <b>Địa điểm:</b> {event_container.location}\n"
                            f"🔗 <b href='{event_container.event_url}'>Bấm vào đây để xem")
                    bot = TelegramNotifier(token=TOKEN,chat_id=CHAT_ID)
                    bot.send_report(alert_msg)
                

            print("✅ ĐÃ CHỐT HẠ VÀ KHÓA TRONG KÉT SẮT!\n")
                

                
        except Exception as e:
            print(f"🔥 Lỗi hệ thống: {e}")


scarp = ObjectScraper()
scarp.fetch_data()