<div align="center">

# 🛡️ Hệ thống Cảnh báo Sớm Tấn công Mạng Đa đầu vào
## Multi-Input Hybrid IDS (LSTM + DNN)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange?style=for-the-badge&logo=tensorflow)
![Status](https://img.shields.io/badge/Status-Development-green?style=for-the-badge)

**Đồ án Mạng Máy Tính - HK251** *Trường Đại học Bách Khoa - ĐHQG TP.HCM*

</div>

---

## 📖 Giới thiệu
Dự án xây dựng một hệ thống phát hiện xâm nhập (IDS) lai ghép sử dụng kỹ thuật **Học sâu (Deep Learning)**. Hệ thống áp dụng chiến thuật **Feature Splitting** (Tách đặc trưng) trên bộ dữ liệu chuẩn **CIC-IDS2017** để giả lập kiến trúc Đa đầu vào (Multi-Input) từ một nguồn dữ liệu duy nhất:

* ⏱️ **Input A (Temporal):** Các đặc trưng liên quan đến thời gian, chuỗi (Flow Duration, IAT...) -> Xử lý bởi mạng **LSTM**.
* 📊 **Input B (Statistical):** Các đặc trưng thống kê (Packet count, Flags...) -> Xử lý bởi mạng **DNN**.

**Mục tiêu:** Phát hiện và phân loại chính xác 15 loại tấn công mạng (DDoS, PortScan, Botnet...) và đưa ra cảnh báo sớm kèm mức độ rủi ro.

---

## 📂 Cấu trúc Dự án

```text
Multi-Input_IDS/
│
├── data/
│   ├── raw/                  # Chứa file CIC-IDS2017.csv (sau khi gộp)
│   └── processed/            # Chứa file .npy sau khi tiền xử lý (để train nhanh)
│
├── saved_models/             # Nơi lưu model.h5 và các scaler (.pkl)
│
├── src/                      # Source code chính
│   ├── __init__.py           # Đánh dấu package
│   ├── utils.py              # Cấu hình chung (Tên cột, Đường dẫn)
│   ├── preprocess.py         # Code làm sạch, chuẩn hóa & tách đặc trưng
│   ├── model.py              # Kiến trúc mạng lai LSTM + DNN
│   ├── train.py              # Script huấn luyện mô hình
│   └── alert_system.py       # Hệ thống cảnh báo & Dự đoán thời gian thực
│
├── setup_data.py             # Script gộp các file CSV con thành file tổng
├── requirements.txt          # Danh sách thư viện phụ thuộc
└── README.md                 # Tài liệu hướng dẫn
```
🛠️ Cài đặt Môi trường
Để tránh xung đột thư viện, vui lòng sử dụng môi trường ảo (venv).

1. Tạo và kích hoạt môi trường ảo
Mở Terminal tại thư mục gốc dự án và chạy:

# Tạo môi trường ảo tên là 'venv'
```
python -m venv venv
```
# Kích hoạt (Windows)
```
.\venv\Scripts\activate
```
# Kích hoạt (Mac/Linux)
```
source venv/bin/activate
```
(Sau khi kích hoạt, đầu dòng lệnh sẽ có chữ (venv) màu xanh)

2. Cài đặt thư viện
```bash
pip install -r requirements.txt
```

💾 Chuẩn bị Dữ liệu (Quan trọng)
Mô hình yêu cầu file dữ liệu tổng hợp CIC-IDS2017.csv. Hãy làm theo các bước sau:

Tải xuống: Truy cập Dataset CIC-IDS2017 hoặc Kaggle, tải file MachineLearningCSV.zip.

Giải nén: Giải nén file zip, bạn sẽ được một thư mục chứa 8 file CSV con (tương ứng các ngày trong tuần).

Di chuyển: Copy toàn bộ thư mục giải nén đó vào đường dẫn data/raw/MachineLearningCVE/.

Gộp file: Chạy script sau để tự động gộp 8 file con thành 1 file tổng:


```Bash

python setup_data.py
```
✅ Sau bước này, kiểm tra thư mục data/raw/ thấy có file CIC-IDS2017.csv (~2-3GB) là thành công.

🚀 Quy trình chạy (Workflow)
Lưu ý: Luôn chạy lệnh từ thư mục gốc dự án và sử dụng cấu trúc python -m src.ten_module để tránh lỗi import.

Bước 1: Tiền xử lý dữ liệu (Preprocessing)
Script này sẽ đọc file CSV lớn, làm sạch (xóa NaN/Inf), mã hóa nhãn, tách đặc trưng thành 2 nhóm (Time & Stat), chuẩn hóa MinMax và lưu kết quả vào data/processed/.

```Bash

python -m src.preprocess
```

Bước 2: Huấn luyện Mô hình (Training)
Xây dựng mô hình Hybrid, load dữ liệu đã xử lý và tiến hành huấn luyện (Training). Model tốt nhất sẽ được lưu vào saved_models/hybrid_model.h5.

```bash
python -m src.train
```
Bước 3: Chạy Hệ thống Cảnh báo (Alert System)
Load model đã train, giả lập luồng dữ liệu mạng mới và in ra cảnh báo nếu phát hiện tấn công.

```Bash
python -m src.alert_system.py
```
