from flask import Flask, request, jsonify
import json
from datetime import datetime
import os
import requests


app = Flask(__name__)
DATA_FILE = 'data.json'

ESP32_BUZZER_URL = "http://10.200.14.247/buzzer"  # Ganti dengan endpoint ESP32-mu

# Buat file jika belum ada
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump([], f)

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

        data.append(payload)

        with open(DATA_FILE, 'w') as f:
            json.dump(data, f)

        print("📂 Data disimpan ke file:", DATA_FILE)

        return jsonify({"status": "received", "data": payload})
    
    except Exception as e:
        print("❌ Gagal menyimpan data:", e)
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

