import cv2
import numpy as np
import streamlit as st

st.title("Human Detection (YOLOv3-tiny)")
status_box = st.empty()

# Inisialisasi kamera lokal
cap = cv2.VideoCapture(0)

# Load model YOLOv3-tiny dan kelas-kelas dari file
net = cv2.dnn.readNet("yolov3-tiny.weights", "yolov3-tiny.cfg")
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers().flatten()]

# Placeholder untuk menampilkan video live
stframe = st.empty()

# Tombol dan opsi
stop = st.button("Stop")
capture_button = st.button("Capture Image")
enable_auto_capture = st.checkbox("Aktifkan Auto Capture", value=True)

# Container untuk menampilkan hasil capture
with st.container():
    st.subheader("📸 Hasil Manual Capture")
    manual_capture_box = st.empty()

with st.container():
    st.subheader("🤖 Hasil Auto Capture")
    auto_capture_box = st.empty()

running = True
captured = False
auto_captured = False

def update_status(detected):
    if detected:
        status_box.error("🚨 Orang terdeteksi!")
    else:
        status_box.success("✅ Aman, tidak ada orang.")

while cap.isOpened() and running:
    ret, frame = cap.read()
    if not ret:
        st.warning("Gagal mengambil frame dari kamera")
        break

    height, width = frame.shape[:2]
    
    # Preprocessing: konversi frame ke blob untuk YOLO
    blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    boxes, confidences = [], []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if classes[class_id] == "person" and confidence > 0.2:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    detected = len(indexes) > 0

    # Menuliskan status deteksi ke file (opsional)
    with open("status.txt", "w") as f:
        f.write("1" if detected else "0")

    update_status(detected)

    # Gambar bounding box untuk semua deteksi pada frame
    if len(indexes) > 0:
        for i in indexes.flatten():
            x, y, w, h = boxes[i]
            label = f"Person: {confidences[i]:.2f}"
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Tampilkan frame live ke Streamlit
    stframe.image(frame, channels='BGR', use_container_width=True)

    # Handle tombol Stop
    if stop:
        running = False

    # Manual capture: mengambil gambar penuh ketika tombol capture ditekan
    if capture_button and not captured:
        captured_image = frame.copy()
        manual_capture_box.image(captured_image, channels='BGR', use_container_width=True)
        # Jika diperlukan, simpan ke file dengan cv2.imwrite("manual_capture.jpg", captured_image)
        captured = True
    if not capture_button:
        captured = False

    # Auto capture: tampilkan frame dengan highlight deteksi confidence tertinggi (tanpa teks info)
    if enable_auto_capture and detected and not auto_captured:
        # Temukan indeks deteksi dengan confidence tertinggi
        max_conf_idx = -1
        max_conf_val = 0
        for i in indexes.flatten():
            if confidences[i] > max_conf_val:
                max_conf_val = confidences[i]
                max_conf_idx = i

        if max_conf_idx != -1:
            # Buat salinan frame untuk diberi highlight
            temp_frame = frame.copy()
            x, y, w, h = boxes[max_conf_idx]
            # Gambar bounding box dengan warna merah untuk menyorot deteksi tertinggi
            cv2.rectangle(temp_frame, (x, y), (x + w, y + h), (0, 0, 255), 3)
            auto_capture_box.image(temp_frame, channels='BGR', use_container_width=True)
            auto_captured = True

    if not detected:
        auto_captured = False

cap.release()
