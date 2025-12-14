import pandas as pd
import numpy as np
import joblib
from tensorflow.keras.models import load_model
from src.utils import *

# Tắt warning của TensorFlow cho gọn
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

def run_attack_demo():
    print("😈 ĐANG TẢI DỮ LIỆU TẤN CÔNG ĐỂ TEST (Vui lòng đợi)...")
    
    # 1. Load dữ liệu gốc
    df = pd.read_csv(RAW_DATA_PATH)
    df.columns = df.columns.str.strip()
    # --- BÍ QUYẾT Ở ĐÂY: Chỉ lấy những dòng KHÔNG PHẢI là BENIGN ---
    # Lọc lấy các loại tấn công cụ thể để demo cho đẹp
    attack_types = ['DDoS', 'PortScan', 'Bot', 'DoS Hulk']
    
    # Lọc dữ liệu chỉ chứa các loại tấn công trên
    attack_df = df[df[LABEL_COLUMN].isin(attack_types)]
    
    if attack_df.empty:
        print("❌ Không tìm thấy dữ liệu tấn công trong file CSV!")
        return

    print(f"✅ Đã tìm thấy {len(attack_df)} mẫu tấn công trong kho dữ liệu.")
    print("⚡ Bắt đầu giả lập tấn công vào hệ thống...\n")

    # Load các công cụ (Model, Scaler, Encoder)
    model = load_model(MODEL_PATH)
    scaler_time = joblib.load(SCALER_TIME_PATH)
    scaler_stat = joblib.load(SCALER_STAT_PATH)
    le = joblib.load(LABEL_ENCODER_PATH)

    # Lấy ngẫu nhiên 5 mẫu tấn công để test
    samples = attack_df.sample(5)

    for i, (_, row) in enumerate(samples.iterrows()):
        # Lấy nhãn thực tế để so sánh
        real_label = row[LABEL_COLUMN]
        
        # Tiền xử lý (Giống hệt lúc train)
        # 1. Tách đặc trưng
        row_df = pd.DataFrame([row]) # Tạo dataframe 1 dòng
        
        # Xử lý input Time
        X_time = row_df[TIME_FEATURES].values
        X_time = scaler_time.transform(X_time)
        X_time = X_time.reshape(1, 1, len(TIME_FEATURES)) # Reshape cho LSTM

        # Xử lý input Stat
        X_stat = row_df[STAT_FEATURES].values
        X_stat = scaler_stat.transform(X_stat)

        # 2. Dự đoán
        pred_prob = model.predict( [X_time,X_stat], verbose=0)
        pred_index = np.argmax(pred_prob)
        pred_label = le.inverse_transform([pred_index])[0]
        confidence = np.max(pred_prob) * 100

        # 3. In kết quả
        print(f"--- 🚨 CẢNH BÁO TẤN CÔNG #{i+1} ---")
        print(f"⚔️  Thực tế là:    {real_label}")
        print(f"🤖 AI dự đoán là: {pred_label}")
        print(f"🎯 Độ tin cậy:    {confidence:.2f}%")
        
        if real_label == pred_label:
            print("✅ KẾT QUẢ: CHÍNH XÁC TUYỆT ĐỐI!")
        else:
            print("❌ KẾT QUẢ: AI NHẦM LẪN")
        print("-" * 30 + "\n")

if __name__ == "__main__":
    run_attack_demo()