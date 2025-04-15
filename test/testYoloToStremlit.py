# app.py
import streamlit as st
import time

st.set_page_config(page_title="Deteksi Orang", layout="centered")

st.title("🔍 Deteksi Orang Otomatis (YOLOv3-Tiny)")
status_box = st.empty()

# Auto-refresh setiap 2 detik
while True:
    try:
        with open("status.txt", "r") as f:
            status = f.read().strip()

        if status == "1":
            status_box.error("🚨 Orang terdeteksi!")
        else:
            status_box.success("✅ Aman, tidak ada orang.")
    except FileNotFoundError:
        status_box.warning("⚠️ Menunggu data...")

    time.sleep(2)
