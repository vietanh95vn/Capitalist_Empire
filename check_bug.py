class GoldScraper:
    # Bản thiết kế đúc Điệp viên cào giá Vàng
    def __init__(self, target_url):
        self.url = target_url

    def get_price(self):
        try:
            print(f"Đang cào dữ liệu từ: {self.url}")
            
            # Giả sử đã dùng Playwright lấy được giá chữ
            text_price = "2050.50$" 
            
            # Lột bỏ dấu $
            clean_price = text_price.replace('$', '')
            
            # Trả về kết quả
            return clean_price
            
        except Exception as e:
            print("⚠️ LỖI RỒI! Chi tiết: {e}")

# Khu vực thực thi
if __name__ = "__main__":
    
    # Đúc Thực thể Điệp viên
    spy = GoldScraper()
    
    # Cướp giá
    current_price = spy.get_price()
    
    # Cộng thêm 100$ phí vận chuyển để báo cho Giám đốc
    total_cost = current_price + 100
    
    print(f"Tổng chi phí là: {total_cost}")