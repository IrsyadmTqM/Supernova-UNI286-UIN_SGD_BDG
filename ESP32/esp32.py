from machine import Pin, ADC, SoftI2C
import ssd1306
import dht
import time
import network
import urequests
import ujson
import socket
import _thread

# === Setup WiFi & Server ===
SSID = 'HAMZAH_ATAS'
PASSWORD = '0702051509'
SERVER_URL = 'http://192.168.96.25:5000/send-data'

# === Setup Sensor & Aktuator ===
dht_sensor = dht.DHT11(Pin(25))      
ldr = ADC(Pin(34))                  
ldr.atten(ADC.ATTN_11DB)
pir_sensor = Pin(33, Pin.IN)         
led = Pin(2, Pin.OUT)               
buzzer = Pin(32, Pin.OUT)

# === Setup OLED ===
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# === Koneksi WiFi ===
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
    
# === Kirim Data ke Server ===
def send_data(temperature, humidity, light, motion):
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

# === Buzzer Trigger ===
def trigger_buzzer():
    print("🔔 Buzzer ON")
    buzzer.on()
    time.sleep(10)
    buzzer.off()
    print("🔕 Buzzer OFF")

# === HTTP Mini Server untuk Trigger Buzzer ===
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

# === Jalankan ===
connect_wifi()
_thread.start_new_thread(start_http_server, ())

while True:
    try:
        dht_sensor.measure()
        temp = dht_sensor.temperature()
        hum = dht_sensor.humidity()
        light_value = ldr.read()
        mot = pir_sensor.value()
        motion_status = "Gerakan!" if mot else "Tidak ada"

        # === Tampilkan ke OLED ===
        oled.fill(0)
        oled.text("UNI286", 0, 0)
        oled.text("Suhu : {} C".format(temp), 0, 10)
        oled.text("Lembab: {} %".format(hum), 0, 20)
        oled.text("Cahaya: {}".format(light_value), 0, 30)
        oled.text("PIR: {}".format(motion_status), 0, 40)
        oled.show()

        # === Tindakan Jika Ada Gerakan ===
        if mot:
            print("🚨 Gerakan terdeteksi!")
            for i in range(5):
                led.on()
                time.sleep(0.2)
                led.off()
                time.sleep(0.2)
        else:
            led.off()
            print("🔇 Tidak ada gerakan.")

        # === Kirim ke Server ===
        send_data(temp, hum, light_value, mot)

    except Exception as e:
        print("⚠ Error membaca sensor:", e)
        oled.fill(0)
        oled.text("Error baca sensor", 0, 20)
        oled.show()

    time.sleep(5)
