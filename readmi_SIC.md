# SIC-SUPERNOVA_UNI286-AssignmentStage2

## 📌 Deskripsi Singkat
Assignment ini bertujuan untuk memenuhi penugasan stage 2 assignment 2 pada bootcamp samsung Innovate campus batch 6.Dalam assignment ini kami menghubungkan **ESP32** dengan sensor **DHT11 (suhu & kelembaban)** dan **light-dependent resistor (LDR) atau photoresistor (intensitas cahaya)**, lalu mengirimkan data ke **Ubidots** untuk divisualisasikan menggunakan widget. Selain itu, data juga dikirim ke **MongoDB** melalui backend berbasis **Flask**, sehingga dapat digunakan untuk analisis lebih lanjut.

## 🎯 Fitur Utama
- ✅ **ESP32 sebagai perangkat utama** untuk membaca data sensor
- ✅ **DHT11** untuk mengukur suhu & kelembaban
- ✅ **light-dependent resistor (LDR)** untuk mendeteksi intensitass cahaya
- ✅ **Pengiriman data ke Ubidots** untuk monitoring real-time
- ✅ **Visualisasi data di Ubidots** dengan dashboard & widget
- ✅ **Pengiriman data ke MongoDB** melalui Flask API
- ✅ **Flask API sebagai middleware** antara ESP32 dan MongoDB

## 🛠️ Teknologi yang Digunakan
- **ESP32** (Mikrokontroler utama)
- **Sensor DHT11 & light-dependent resistor (LDR)**
- **Ubidots** (IoT platform untuk monitoring)
- **Flask** (Backend API)
- **MongoDB** (Database untuk menyimpan data)
- **WiFi** (Koneksi ESP32 ke internet)

## 🔧 Alur Kerja Proyek
1. **ESP32 membaca data dari sensor DHT11 & light-dependent resistor (LDR)**
2. **Mengirimkan data ke Ubidots** menggunakan HTTP 
3. **Mengirimkan data ke Flask API**, yang kemudian menyimpan data di MongoDB
4. **Menampilkan data secara real-time di Ubidots** menggunakan widget


## 🖼️ Foto Rangkaian
<p align="center">
  <img src = "image/gambar1.jpg" width=700>
</p>
<p align="center">
  <img src = "image/gambar2.jpg" width=700>
</p>
<p align="center">
  <img src = "image/gambar3.jpg" width=700>
</p>
<p align="center">
  <img src = "image/gambar4.jpg" width=700>
</p>
<p align="center">
  <img src = "image/gambar5.jpg" width=700>
</p>
<p align="center">
  <img src = "image/gambar6.jpg" width=700>
</p>

