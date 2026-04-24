from fastapi import FastAPI, HTTPException, Query
import sqlite3
import os

# 1. API INSTANTIATION (Khởi tạo Cỗ máy API)
app = FastAPI(
    title="Capitalist Empire - WWR Data API",
    description="Data Provisioning Layer for Extracted Remote Jobs",
    version="1.0.0"
)

# 2. PATH RESOLUTION (Định vị Hầm chứa)
# Đảm bảo đường dẫn tuyệt đối hoặc tương đối trỏ ĐÚNG vào thư mục data_vault
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # cú pháp mặc định
DB_PATH = os.path.join(BASE_DIR, "data_vault", "wwr_jobs.db") # > folder data_vault > www_jobs.db

def get_db_connection():
    """Tạo kết nối tới SQLite và ép kiểu trả về dạng Dictionary thay vì Tuple"""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row # Cực kỳ quan trọng để JSON Serialization hoạt động
        return conn
    except sqlite3.Error as e:
        print(f"❌ [DB CRASH]: Không thể kết nối Hầm chứa - {e}")
        raise HTTPException(status_code=500, detail="Internal Database Error")

# 3. ENDPOINT DEFINITIONS (Mở Cổng Giao tiếp)

@app.get("/")
def health_check():
    """Ping Endpoint: Kiểm tra xem Cỗ máy API có đang sống không (Heartbeat)"""
    return {"status": "Operational", "engine": "FastAPI", "db_path": DB_PATH}

@app.get("/api/v1/jobs")
def fetch_jobs(keyword: str = Query(None, description="Lọc công việc theo từ khóa trong tiêu đề")):
    """
    Data Endpoint: Lấy danh sách công việc. 
    Nếu có ?keyword=python, hệ thống sẽ lọc dữ liệu trực tiếp bằng SQL Query.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        if keyword:
            # SỬ DỤNG PARAMETERIZED QUERY ĐỂ CHỐNG SQL INJECTION (Hack Database)
            query = "SELECT * FROM jobs WHERE LOWER(title) LIKE ? ORDER BY timestamp DESC"
            cursor.execute(query, (f"%{keyword.lower()}%",))
        else:
            query = "SELECT * FROM jobs ORDER BY timestamp DESC"
            cursor.execute(query)
            
        rows = cursor.fetchall()
        
        # SERIALIZATION: Chuyển đổi dữ liệu SQLite thô thành JSON Payload chuẩn
        jobs_payload = [dict(row) for row in rows]
        
        return {
            "status": "Success",
            "count": len(jobs_payload),
            "data": jobs_payload
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close() # LUÔN PHẢI ĐÓNG KẾT NỐI SAU KHI DÙNG XONG!