import numpy as np
import pandas as pd  # <--- Thêm thư viện này để đọc file CSV
import joblib
import time
from tensorflow.keras.models import load_model
from src.utils import *

# --- CẤU HÌNH MỨC ĐỘ NGUY HIỂM ---
ATTACK_SEVERITY = {
    # Nhóm Rất Nguy Hiểm (Cần chặn ngay)
    'DDoS': 'HIGH',
    'DoS Hulk': 'HIGH',
    'DoS GoldenEye': 'HIGH',
    'Bot': 'HIGH',
    'Web Attack \x12 Brute Force': 'HIGH',
    'Web Attack \x12 Sql Injection': 'HIGH',
    'Web Attack \x12 XSS': 'HIGH',
    'Heartbleed': 'HIGH',
    'Infiltration': 'HIGH',

    # Nhóm Trung Bình (Cần theo dõi sát)
    'PortScan': 'MEDIUM',
    'FTP-Patator': 'MEDIUM',
    'SSH-Patator': 'MEDIUM',
    
    # Nhóm Thấp (Ít rủi ro)
    'DoS slowloris': 'LOW', 
    'DoS Slowhttptest': 'LOW'
}

class AlertSystem:
    def __init__(self):
        print("--- [GĐ4] Khởi động hệ thống cảnh báo... ---")
        # Load các thành phần cần thiết
        self.model = load_model(MODEL_PATH)
        self.scaler_time = joblib.load(SCALER_TIME_PATH)
        self.scaler_stat = joblib.load(SCALER_STAT_PATH)
        self.le = joblib.load(LABEL_ENCODER_PATH)
        print("Hệ thống đã sẵn sàng!")

    def predict_and_alert(self, raw_time_data, raw_stat_data):
        # 1. Tiền xử lý dữ liệu mới
        # Scale
        processed_time = self.scaler_time.transform(raw_time_data)
        processed_stat = self.scaler_stat.transform(raw_stat_data)
        
        # Reshape cho LSTM
        processed_time = processed_time.reshape(processed_time.shape[0], 1, processed_time.shape[1])

        # 2. Dự đoán (Lưu ý thứ tự input: [Time, Stat])
        probs = self.model.predict([processed_time, processed_stat], verbose=0)
        
        # 3. Phân tích kết quả
        for i, prob in enumerate(probs):
            risk_score = np.max(prob)
            class_idx = np.argmax(prob)
            attack_name = self.le.inverse_transform([class_idx])[0]

            self._trigger_alert(attack_name, risk_score)

    def _trigger_alert(self, attack_name, score):
        # 1. Nếu là người thường -> Bỏ qua
        if attack_name == "BENIGN":
            print(f"✅ Normal Traffic (Score: {score:.2f})")
            return

        # 2. Lấy độ nghiêm trọng từ từ điển (Mặc định là LOW nếu không tìm thấy)
        severity = ATTACK_SEVERITY.get(attack_name, 'LOW')

        # 3. Logic Cảnh báo Ưu tiên kết hợp (Severity + Score)
        # TH1: Tấn công RẤT NGUY HIỂM và AI khá tự tin (> 70%) -> BÁO ĐỘNG ĐỎ
        if severity == 'HIGH' and score > 0.7:
            print(f"🚨 [CRITICAL - BLOCK IP] Phát hiện tấn công nguy hiểm: {attack_name} (Risk: {score:.2f})")
        
        # TH2: Tấn công TRUNG BÌNH hoặc AI rất tự tin (> 90%) -> CẢNH BÁO VÀNG
        elif severity == 'MEDIUM' or score > 0.9:
            print(f"⚠️ [WARNING - LOGGING] Nghi ngờ xâm nhập: {attack_name} (Risk: {score:.2f})")
        
        # TH3: Các trường hợp còn lại -> THÔNG TIN
        else:
            print(f"ℹ️ [INFO] Cảnh báo mức thấp: {attack_name} (Risk: {score:.2f})")

# --- PHẦN CHẠY THỬ VỚI DỮ LIỆU THẬT ---
if __name__ == "__main__":
    bot = AlertSystem()
    
    print("\n⏳ Đang tải một ít dữ liệu thực tế để test (Vui lòng đợi)...")
    # Load dữ liệu thật để có mẫu tấn công chuẩn
    df = pd.read_csv(RAW_DATA_PATH)
    df.columns = df.columns.str.strip() # Sửa lỗi tên cột
    
    # --- CHỌN 3 MẪU ĐIỂN HÌNH ĐỂ TEST ---
    print("⚙️  Đang chọn lọc các mẫu tấn công...")
    
    # THAY ĐỔI SỐ LƯỢNG Ở ĐÂY (Ví dụ: Lấy 5 mẫu mỗi loại)
    n_samples = 5 
    
    # 1. Lấy n mẫu DDoS
    sample_ddos = df[df[LABEL_COLUMN] == 'DDoS'].sample(n_samples)
    
    # 2. Lấy n mẫu PortScan
    sample_portscan = df[df[LABEL_COLUMN] == 'PortScan'].sample(n_samples)
    
    # 3. Lấy n mẫu BENIGN
    sample_normal = df[df[LABEL_COLUMN] == 'BENIGN'].sample(n_samples)

    # Gộp lại (Tổng cộng sẽ là 15 mẫu)
    test_batch = pd.concat([sample_ddos, sample_portscan, sample_normal])
    
    # Tráo đổi ngẫu nhiên thứ tự để nhìn cho sinh động (lúc xanh, lúc đỏ xen kẽ)
    test_batch = test_batch.sample(frac=1).reset_index(drop=True)

    print(f"🚀 Bắt đầu kiểm tra hệ thống với {len(test_batch)} gói tin:\n")
    
    for i, (_, row) in enumerate(test_batch.iterrows()):
        # Tạo dataframe 1 dòng
        row_df = pd.DataFrame([row])
        
        # Lấy đúng các cột đặc trưng từ file utils
        input_time = row_df[TIME_FEATURES].values
        input_stat = row_df[STAT_FEATURES].values
        
        # Gọi hàm dự đoán
        bot.predict_and_alert(input_time, input_stat)
        
        # Nghỉ xíu cho dễ nhìn
        time.sleep(0.5)