# DBMS

# 🧬 MRI Data Query System (Text + Image)

Hệ thống này cho phép **quản lý dữ liệu bệnh nhân** (text từ Excel + ảnh MRI dạng DICOM), hỗ trợ:

- Upload dữ liệu bệnh nhân từ Excel + thư mục ảnh `.ima`.
- Lưu trữ ảnh vào MongoDB GridFS.
- Tìm kiếm bệnh nhân theo **keyword trong chẩn đoán** hoặc theo **patient_id**.
- Truy vấn lịch sử y khoa (progress note).
- Trả về kết quả bao gồm **metadata + ảnh dạng Base64**.

---

## ⚙️ Chuẩn bị dữ liệu

1. Mặc định, dữ liệu MRI cần đặt trong thư mục được chỉ định bởi biến `DATA_DIR` trong file `main.py`:

```python
DATA_DIR = Path(r"C:\Users\ADMIN\Documents\BK_Document\Năm-IV\251\DBMS\EW\Clone\01_MRI_Data")
```

Bạn cần chỉnh lại DATA_DIR để trỏ tới thư mục chứa dữ liệu MRI trên máy của bạn.

2. Trong thư mục DATA_DIR phải có file Excel: Radiologists Report.xlsx

- File này chứa các cột:

* patient_id
* diagnosis
* regimen

3. Cấu trúc thư mục:

01*MRI_Data/

├── Radiologists Report.xlsx # File Excel chứa patient_id, diagnosis, regimen

├── 0001/ # Patient 0001

│ └── L-SPINE_LSS_20160309_091629_240000/ # Study folder (một bệnh nhân có 1 study)

│ ├── LOCALIZER_0001/ # Series 1

│ │ ├── file1.ima

│ │ ├── file2.ima

│ │ └── ...

│ ├── POSDISP*[4]\_T2_TSE_TRA_384_5001/ # Series 2

│ │ ├── file1.ima

│ │ ├── file2.ima

│ │ └── ...

│ └── ... # Các series khác

├── 0002/ # Patient 0002

│ └── L-SPINE_LSS_20160315_141500_240000/

│ ├── LOCALIZER_0001/

│ │ └── ...

│ └── ...

└── ...

👉 Quy ước:

- `0001`, `0002`, … là mã bệnh nhân (ID được zero-padding 4 chữ số).
- Trong mỗi patient có duy nhất **1 study folder**.
- Trong study có nhiều series (mỗi series là 1 tập hợp ảnh `.ima`).
- File Excel `Radiologists Report.xlsx` phải nằm trực tiếp trong thư mục `DATA_DIR`.

🚀 Cài đặt & Chạy server

Tạo và kích hoạt môi trường ảo:

`python -m venv venv # tạo môi trường ảo`

`venv\Scripts\activate # Windows`

`source venv/bin/activate # Linux / MacOS`

Cài đặt dependencies:

`pip install -r requirements.txt`

Chạy server FastAPI:

`uvicorn main:app --reload --port 8000`

Mặc định server sẽ chạy ở:
👉 http://localhost:8000

📡 Các API chính

1. Kiểm tra server
   GET /

2. Upload toàn bộ dữ liệu từ Excel + thư mục ảnh
   GET /upload

3. Thêm bệnh nhân mới từ file zip (chứa ảnh .ima)
   POST /add_patient_from_folder
   Form-data:

- diagnosis: str
- regimen: str
- zip_file: file.zip

4. Truy vấn theo keyword trong chẩn đoán
   GET /search_keyword_with_images?keyword=xxx&page=1&page_size=10

5. Truy vấn theo patient_id
   GET /search_patient_by_id?patient_id=1

6. Thêm lịch sử y khoa (progress note)
   POST /medical-history
   Body (JSON):
   {
   "patient_id": 1,
   "progress_note": "Bệnh nhân có tiến triển tốt"
   }

7. Lấy lịch sử y khoa theo patient_id
   GET /medical-history/{patient_id}
