# 🔐 Smart Home Security System with IoT & AI

Proyek ini merupakan prototype sistem keamanan rumah berbasis **IoT dan AI** yang dikembangkan oleh **Kelompok UNI286 - Supernova** dari **UIN Sunan Gunung Djati Bandung**. Sistem ini mampu mendeteksi pergerakan manusia secara otomatis menggunakan sensor dan kamera, lalu mengidentifikasinya menggunakan teknologi **YOLO/OpenCV** untuk pengambilan keputusan secara cerdas, baik otomatis maupun manual oleh user.

## 🚀 Fitur Utama
- Deteksi suhu & kelembapan ruangan secara real-time (DHT11)
- Monitoring intensitas cahaya (LDR)
- Deteksi pergerakan manusia (PIR Sensor + ESP32-CAM)
- Pengenalan objek menggunakan AI (YOLO/OpenCV)
- Mode keamanan otomatis & manual (kendali buzzer)
- Visualisasi data sensor & kamera via Streamlit Dashboard
- Pengiriman dan penyimpanan data melalui Flask Server

## 🧠 Teknologi yang Digunakan
- ESP32-CAM & Sensor (PIR, DHT11, LDR)
- Python (Flask & Streamlit)
- OpenCV + YOLO (AI model untuk deteksi manusia)
- JSON (Data storage dan komunikasi antar komponen)
- Front-end Streamlit Dashboard

## 🧩 Alur Sistem
1. Sensor PIR mendeteksi gerakan → ESP32-CAM aktif
2. Gambar dikirim ke YOLO/OpenCV untuk deteksi manusia
3. Jika manusia terdeteksi, sistem merespons sesuai mode:
   - **Manual Mode:** Buzzer menyala jika tombol diklik oleh user
   - **Auto Mode:** Buzzer menyala otomatis
4. Data sensor dikirim ke Flask → disimpan ke JSON → ditampilkan oleh Streamlit

## 👥 Anggota Kelompok UNI286 - Supernova
- **Nisrina Aliya Tharifah**: Backend Developer  
- **Putri Puspita**: UI/UX Developer  
- **Irsyad Adfiansya Hidayat**: Hardware Designer, IoT Specialist  
- **Muhammad Irsyad Mustaqim**: AI Engineer  
