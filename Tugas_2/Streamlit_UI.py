import streamlit as st
import pandas as pd
import json
import time
import os

import requests
from PIL import Image
from io import BytesIO
from datetime import datetime

st.set_page_config(page_title="Face Recognition Monitor", layout="centered")
st.title("📊 ESP32 Real-time Sensor Dashboard")

DATA_FILE = 'data.json'
ESP32_CAM_URL = "http://10.200.7.163/capture"  # Ganti IP kamu
BUZZER_TRIGGER_URL = "http://192.168.96.25:5000/trigger-buzzer"  # URL ke Flask server


# Cek dan buat file jika belum ada
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump([], f)

if st.button("Ambil Foto dari ESP32-CAM"):
    try:
        response = requests.get(ESP32_CAM_URL, timeout=5)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            st.image(image, caption="Foto dari ESP32-CAM",use_container_width=True)
        else:
            st.error(f"❌ Gagal ambil foto: {response.status_code}")
    except Exception as e:
        st.error(f"🚨 Error: {e}")

if st.button("🔊 Bunyi Buzzer"):
    try:
        res = requests.post(BUZZER_TRIGGER_URL, timeout=3)
        if res.status_code == 200:
            st.success("✅ Buzzer berhasil diaktifkan!")
        else:
            st.error("❌ Gagal mengaktifkan buzzer.")
    except Exception as e:
        st.error(f"🚨 Error: {e}")

# Fungsi load data
def load_data():
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    return pd.DataFrame(data)

# Placeholder kontainer
placeholder = st.empty()

while True:
    with placeholder.container():
        df = load_data()

        if not df.empty:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.sort_values(by='timestamp', ascending=False).reset_index(drop=True)

            st.subheader("📋 Data Sensor Terbaru")
            st.dataframe(df.head(5), use_container_width=True)

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("🌡️ Suhu (°C)", f"{df['temperature'][0]:.1f}")
            with col2:
                st.metric("💧 Kelembaban (%)", f"{df['humidity'][0]:.1f}")
            with col3:
                st.metric("💡 Cahaya", df['light'][0])
            with col4:
                if 'motion' in df.columns:
                    motion = df['motion'][0]
                    motion_status = "🔴 Terdeteksi" if motion else "⚪ Tidak Ada"
                    st.metric("🚶 Gerakan", motion_status)
                else:
                    st.metric("🚶 Gerakan", "Data tidak tersedia")

            # Garis tren (grafik)
            st.subheader("📈 Grafik Sensor (24 Data Terakhir)")
            chart_df = df.head(24).sort_values(by='timestamp')

            st.line_chart(chart_df[['temperature', 'humidity', 'light']])

            if 'motion' in df.columns:
                st.area_chart(chart_df[['motion']])

    time.sleep(5)
