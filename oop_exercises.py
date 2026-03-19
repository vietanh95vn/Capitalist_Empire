# ==========================================
# 1. THE BASE BLUEPRINT (BẢN THIẾT KẾ GỐC)
# ==========================================
class Employee: # Sửa 'employer' (ông chủ) thành 'Employee' (người làm thuê)
    
    # Kỹ năng Khởi tạo: Cấp phát hành trang khi nhân viên mới vào công ty
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary
        self.status = "Sleep" # Trạng thái mặc định
        print(f"[HR] Đã tuyển dụng {self.name} với mức lương {self.salary}$.")

    # Kỹ năng Làm việc: KHÔNG truyền thêm tham số. Nó tự biết tên nó là gì!
    def work(self):
        self.status = "On Work"
        # Thò tay vào túi 'self' để lôi cái tên ra dùng
        print(f"   -> [{self.name}] is looking at the screen and status is: {self.status}.")


# ==========================================
# 2. THE INHERITED BLUEPRINT (BẢN THIẾT KẾ KẾ THỪA)
# ==========================================
class Director(Employee): # Kế thừa toàn bộ gen của Employee
    
    # Nâng cấp Khởi tạo: Giám đốc có thêm Quyền lực (Cổ phần)
    def __init__(self, name, salary, company_share):
        super().__init__(name, salary) # Gọi Bố ra để lo việc nhập Tên và Lương
        self.company_share = company_share # Nhét Cổ phần vào túi áo của Giám đốc

    # GHI ĐÈ KỸ NĂNG (OVERRIDING): Bắt buộc phải trùng tên hàm với Bố
    # LƯU Ý: Tuyệt đối không có def work(self, company_share). Chữ 'self' là đủ!
    def work(self):
        # Tự động lấy Cổ phần từ trong túi 'self' ra để in!
        print(f"   -> [{self.name}] đang chơi Golf và bóc lột nhân viên. Đang nắm giữ {self.company_share}% công ty!")


# ==========================================
# 3. THE EXECUTION (THỰC THI SỨC MẠNH)
# ==========================================
print("\n--- THE TEST BEGINS ---")

# Đúc ra 2 Thực thể (Objects) độc lập
worker_john = Employee("John", 1000)
director_linh = Director("Trúc Linh", 5000, 51)

print("\n--- THE WORKING HOURS ---")
# Kích hoạt hành động. Clean and Simple. Bấm nút là chạy!
worker_john.work()
director_linh.work()