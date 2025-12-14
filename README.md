<div align="center">

# 🛡️ Hệ thống Cảnh báo Sớm Tấn công Mạng Đa đầu vào
## Multi-Input Hybrid IDS (LSTM + DNN)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange?style=for-the-badge&logo=tensorflow)
![Status](https://img.shields.io/badge/Status-Completed-success?style=for-the-badge)

**Đồ án Mạng Máy Tính - HK251** *Trường Đại học Bách Khoa - ĐHQG TP.HCM*

</div>

---

## 📖 Giới thiệu
Dự án xây dựng một hệ thống phát hiện xâm nhập (IDS) lai ghép sử dụng kỹ thuật **Học sâu (Deep Learning)**. Hệ thống áp dụng chiến thuật **Feature Splitting** (Tách đặc trưng) trên bộ dữ liệu chuẩn **CIC-IDS2017** để giả lập kiến trúc Đa đầu vào (Multi-Input) từ một nguồn dữ liệu duy nhất:

* ⏱️ **Input A (Temporal):** Các đặc trưng liên quan đến thời gian, chuỗi (Flow Duration, IAT...) -> Xử lý bởi mạng **LSTM** để nắm bắt quy luật thời gian.
* 📊 **Input B (Statistical):** Các đặc trưng thống kê (Packet count, Flags...) -> Xử lý bởi mạng **DNN** để phân tích cường độ lưu lượng.

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
│   ├── demo_attack.py        # Demo tấn công giả lập (Visual Demo)
│   ├── evaluate_mass.py      # Script đánh giá diện rộng (Batch Testing)
│   └── alert_system.py       # Hệ thống cảnh báo & Dự đoán thời gian thực
│
├── setup_data.py             # Script gộp các file CSV con thành file tổng
├── requirements.txt          # Danh sách thư viện phụ thuộc
└── README.md                 # Tài liệu hướng dẫn
```
# 🛠️ Cài đặt Môi trường
Để tránh xung đột thư viện, vui lòng sử dụng môi trường ảo (venv).

## 1. Tạo và kích hoạt môi trường ảo
Mở Terminal tại thư mục gốc dự án và chạy:
### Tạo môi trường ảo
```bash
python -m venv venv
```
### Kích hoạt (Windows)
```bash
.\venv\Scripts\activate
```
### Kích hoạt (Mac/Linux)
```bash
source venv/bin/activate
```
## 2. Cài đặt thư viện
```bash
pip install -r requirements.txt
```
# 💾 Chuẩn bị Dữ liệu (Bắt buộc)
Tải xuống: Truy cập [Dataset CIC-IDS2017](http://cicresearch.ca/CICDataset/CIC-IDS-2017/Dataset/) hoặc Kaggle, tải file ```MachineLearningCSV.zip.```

Giải nén: Copy toàn bộ các file CSV đã giải nén vào đường dẫn ```data/raw/MachineLearningCVE/.```

Gộp file: Chạy script sau để tự động gộp 8 file con thành 1 file tổng:
```bash
python setup_data.py
```
✅ Kiểm tra: Thư mục data/raw/ có file CIC-IDS2017.csv (~2-3GB) là thành công.
# 🚀 Hướng dẫn Sử dụng (Workflow)
Lưu ý: Luôn chạy lệnh từ thư mục gốc dự án để tránh lỗi import.

## 1️ Tiền xử lý dữ liệu (Preprocessing)
Làm sạch dữ liệu (xóa NaN/Inf), mã hóa nhãn, tách đặc trưng và chuẩn hóa.
```bash
python -m src.preprocess
```
## 2️ Huấn luyện Mô hình (Training)
Xây dựng mô hình Hybrid và huấn luyện. Model sẽ được lưu vào ```saved_models/hybrid_model.h5.```
```bash
python -m src.train
```
## 3️ Đánh giá diện rộng (Mass Evaluation) 🔥 Mới
Chạy kiểm thử trên tập dữ liệu lớn (ví dụ: 500,000 mẫu) để lấy chỉ số chính xác thực tế.
```bash
python -m src.evaluate_mass
```
## 4️ Chạy Demo Tấn công (Visual Demo) 🔥 Mới
Giả lập các cuộc tấn công cụ thể để xem hệ thống cảnh báo "bắt trộm" như thế nào.
```bash
python -m src.demo_attack
```
# 📊 Kết quả Thực nghiệm
Dựa trên kết quả kiểm thử với 500,000 mẫu dữ liệu thực tế:

Độ chính xác tổng thể (Accuracy): ~94%

Khả năng phát hiện (Recall):

✅ DDoS / PortScan / DoS: Đạt 99% - 100%. Mô hình hoạt động cực tốt với các tấn công lưu lượng lớn.

⚠️ Web Attacks (XSS, SQLi): Hiệu quả thấp (< 10%). Lý do: Các tấn công này nằm ở tầng ứng dụng (payload), khó phát hiện chỉ bằng thông số thống kê lưu lượng (Flow Stats).

