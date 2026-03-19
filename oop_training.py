class CHOSANTBC:
    def __init__(self,ten_cho,nguong_bao_dong):
        self.ten = ten_cho
        self.nguong = nguong_bao_dong
        self.trang_thai = "Đang ngủ"
        print(f"[LÒ RÈN] Đã đúc thành công con chó săn: {self.ten}")
    def di_tuan(self,gia_hien_tai):
        self.trang_thai = "Đang săn mồi"
        print(f"[{self.ten}] đang ngửi mùi thị trường... Giá hiện tại: {gia_hien_tai}$")
        
        if gia_hien_tai < self.nguong:
            self.sua_len()
        else:
            print(f"[{self.ten}] Mọi thứ an toàn ")
            
    def sua_len(self):
        print(f"🚨🚨🚨 [{self.ten}]: GÂU GÂU! THỊ TRƯỜNG SẬP! BÁO ĐỘNG ĐỎ! 🚨🚨🚨")      
print("--- MỞ CỬA LÒ RÈN ---")
# Thay vì hì hục code lại từ đầu, tôi chỉ cần 2 dòng code để tạo ra 2 hệ thống độc lập!
cho_san_crypto = CHOSANTBC("Kẻ Hủy Diệt BTC", 60000)
cho_san_chung_khoan = CHOSANTBC("Sát Thủ Tesla", 180)
cho_san_vang =CHOSANTBC("Săn vàng", 2000)
print("\n--- BẮT ĐẦU CA TRỰC ---")
# Thả chó ra cắn (Truyền giá thị trường giả định vào)
cho_san_crypto.di_tuan(65000)   # Giá vẫn cao hơn 60k -> An toàn
cho_san_crypto.di_tuan(58000)   # Giá sập dưới 60k -> Nổ còi!

print("-" * 20)
cho_san_chung_khoan.di_tuan(190) # An toàn
cho_san_vang.di_tuan(3000)
cho_san_vang.di_tuan(1500)  

class CHOSANBANTIA(CHOSANTBC):
    def __init__(self, ten_cho, nguong_bao_dong,dan_duoc):
        super().__init__(ten_cho, nguong_bao_dong)
        self.dan = dan_duoc
        print("[LÒ RÈN] Đã NÂNG CẤP thành công Sát thủ Bắn tỉa: {self.ten} với {self.dan}$ đạn dược!")
    def bop_co(self):
        print(f"💥💥💥 [{self.ten}] ĐÃ BÓP CÒ! Khớp lệnh TỰ ĐỘNG BẮT ĐÁY với số tiền: {self.dan}$! 💥💥💥")
    def sua_len(self):
        print(f"🤫🤫🤫 [{self.ten}]: (Im lặng tuyệt đối)... Đã khóa mục tiêu. Chuẩn bị tiêu diệt! 🤫🤫🤫")
print("\n--- TEST THỬ PHIÊN BẢN PRO ---")
# Đúc ra một con Bắn Tỉa. Nó cần 3 thông số: Tên, Ngưỡng sập, Số tiền mua đáy
sat_thu_solana = CHOSANBANTIA("Sniper SOL", 100, 5000)

# Kịch bản thực chiến:
gia_solana_hien_tai = 90 # Giá sập dưới ngưỡng 100

# Nó vẫn có thể xài lệnh di_tuan() của đời Bố một cách bình thường!
sat_thu_solana.di_tuan(gia_solana_hien_tai) 

if gia_solana_hien_tai < sat_thu_solana.nguong:
    # Sau khi sủa (được thừa kế), nó lập tức dùng kỹ năng bóp cò của riêng nó!
    sat_thu_solana.bop_co()