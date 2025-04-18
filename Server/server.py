from flask import Flask, request, jsonify
import json
from datetime import datetime
import os
import requests

app = Flask(__name__)
DATA_FILE = 'data.json'

# Token dan URL Ubidots (Ganti dengan token dan URL endpoint yang benar)
UBIDOTS_TOKEN = "BBUS-Uy8rd1RimrqsQc8ojVkhSD9Zz3rZZA"
UBIDOTS_API_URL = "https://industrial.api.ubidots.com/api/v1.6/devices/esp32-monitor/"

ESP32_BUZZER_URL = "http://10.200.14.247/buzzer"  # Ganti dengan endpoint ESP32-mu

# Buat file jika belum ada
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump([], f)

def send_to_ubidots(payload):
    """Fungsi untuk mengirim data ke Ubidots"""
    headers = {
        "X-Auth-Token": UBIDOTS_TOKEN,
        "Content-Type": "application/json"
    }

    # Menyiapkan data yang akan dikirim ke Ubidots
    data = {
        "temperature": payload.get("temperature"),
        "humidity": payload.get("humidity"),
        "light": payload.get("light"),
        "motion": payload.get("motion")
    }

    try:
        print(f"🔍 Mengirim data ke Ubidots: {data}")
        response = requests.post(UBIDOTS_API_URL, headers=headers, json=data)
        print(f"🔍 Response dari Ubidots: {response.status_code} - {response.text}")

        if response.status_code == 201:
            print("✅ Data berhasil dikirim ke Ubidots!")
        else:
            print(f"❌ Gagal mengirim data ke Ubidots. Status code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"❌ Error saat mengirim data ke Ubidots: {e}")

@app.route('/trigger-buzzer', methods=['POST'])
def trigger_buzzer():
    try:
        response = requests.get(ESP32_BUZZER_URL, timeout=3)
        if response.status_code == 200:
            return jsonify({"status": "success", "message": "Buzzer triggered!"})
        else:
            return jsonify({"status": "fail", "message": "ESP32 error"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/send-data', methods=['POST'])
def receive_data():
    payload = request.json
    print("✅ DATA DITERIMA DARI ESP32:", payload)  # Tambahan debug

    if not payload:
        return jsonify({"status": "error", "message": "No JSON received"}), 400

    payload['timestamp'] = datetime.now().isoformat()

    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)

        # Tambahkan data baru jika tidak ada di dalam data.json
        data.append(payload)

        # Cek apakah data terbaru sudah berubah dibandingkan data sebelumnya
        if len(data) > 1:
            last_data = data[-2]  # Ambil data sebelumnya
            if (last_data["temperature"] != payload["temperature"] or
                last_data["humidity"] != payload["humidity"] or
                last_data["light"] != payload["light"] or
                last_data["motion"] != payload["motion"]):
                # Kirim data terbaru ke Ubidots
                send_to_ubidots(payload)

        # Simpan data ke file
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f)

        print("📂 Data disimpan ke file:", DATA_FILE)

        return jsonify({"status": "received", "data": payload})
    
    except Exception as e:
        print("❌ Gagal menyimpan data:", e)
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
