import network
import urequests
import time
import dht
import ujson
from machine import Pin, ADC
import socket
import _thread

# WiFi & server
SSID = 'SIC'
PASSWORD = '12345678'
SERVER_URL = 'http://192.168.96.25:5000/send-data'




dht_sensor = dht.DHT11(Pin(4))      
ldr = ADC(Pin(34))                  
ldr.atten(ADC.ATTN_11DB)

pir_sensor = Pin(5, Pin.IN)         
led = Pin(2, Pin.OUT)               
buzzer = Pin(15, Pin.OUT)          



def connect_wifi():
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(SSID, PASSWORD)

    print("⏳ Menghubungkan ke WiFi...")
    while not station.isconnected():
        time.sleep(1)
        print(".", end="")

    print("\n✅ Terhubung!")
    print("📶 IP Address ESP32:", station.ifconfig()[0])
    

# Fungsi kirim data ke server
def send_data(temperature, humidity, light,motion):
    try:
        payload = {
            "temperature": temperature,
            "humidity": humidity,
            "light": light,
            "motion": motion
        }
        json_data = ujson.dumps(payload)
        headers = {'Content-Type': 'application/json'}

        print("📤 Mengirim data ke server:", payload)
        response = urequests.post(SERVER_URL, data=json_data, headers=headers)
        print("✅ Server merespon:", response.text)
        response.close()
    except Exception as e:
        print("❌ Gagal mengirim data:", e)

# Fungsi untuk menghidupkan buzzer
def trigger_buzzer():
    print("🔔 Buzzer ON")
    buzzer.on()
    time.sleep(10)  # Buzzer bunyi selama 1 detik
    buzzer.off()
    print("🔕 Buzzer OFF")

# Fungsi server HTTP mini
def start_http_server():
    addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print("🌐 HTTP Server aktif di port 80")

    while True:
        cl, addr = s.accept()
        print('📡 Permintaan dari', addr)
        request = cl.recv(1024)
        request_str = request.decode()

        if 'GET /buzzer' in request_str:
            trigger_buzzer()
            response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nBuzzer triggered!"
        else:
            response = "HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\n\r\nNot Found"

        cl.send(response)
        cl.close()

# Jalankan HTTP server di thread terpisah
connect_wifi()
_thread.start_new_thread(start_http_server, ())


while True:
    try:
        dht_sensor.measure()
        temp = dht_sensor.temperature()
        hum = dht_sensor.humidity()
        light_value = ldr.read()

        # Cek gerakan dari sensor PIR
        mot = pir_sensor.value()

        if mot:
            print("🚨 Gerakan terdeteksi!")
            for i in range(5):  # LED kedip 5x
                led.on()
                #buzzer.on()
                #time.sleep(0.2)
                led.off()
                time.sleep(0.2)
            #buzzer.off()
        else:
            led.off()
            #buzzer.off()
            print("🔇 Tidak ada gerakan.")

        # Kirim data sensor ke server
        send_data(temp, hum, light_value,mot)

    except Exception as e:
        print("⚠ Error membaca sensor:", e)

    time.sleep(5)