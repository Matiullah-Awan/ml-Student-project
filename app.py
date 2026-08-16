import os
import smtplib
import time
from email.message import EmailMessage

import cv2
import pygame
import streamlit as st
from ultralytics import YOLO

# Streamlit Page Setup
st.set_page_config(page_title="Threat Detection & Alert System", page_icon="🚨", layout="wide")

st.title("🚨 Real-Time Threat Detection & Alert System")
st.markdown("Detects threats (Knife, Scissors, Gun/Knife targets, etc.), plays alarm, captures images & sends email alerts.")

pygame.mixer.init()

DANGER_CLASSES = ["knife", "scissors", "cell phone"]

if not os.path.exists("captures"):
    os.makedirs("captures")

# --- Email Alert Function ---
def send_email_alert(image_path):
    sender_email = "mu1022579@gmail.com"
    app_password = "dynqtuskwvjquavx"
    receiver_email = "mu1022579@gmail.com"

    msg = EmailMessage()
    msg['Subject'] = '🚨 Alert: Threat Detected!'
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg.set_content('A threat was detected. Please see the attached image.')

    try:
        with open(image_path, 'rb') as f:
            file_data = f.read()
            file_name = os.path.basename(image_path)
            msg.add_attachment(file_data, maintype='image', subtype='jpeg', filename=file_name)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, app_password)
            smtp.send_message(msg)
            print("Email sent Successfully!")
    except Exception as e:
        print(f"Email Error: {e}")

@st.cache_resource
def load_model():
    return YOLO("yolov8n.pt")

model = load_model()

# --- Sidebar ---
st.sidebar.header("Controls & Settings")
confidence = st.sidebar.slider("Confidence Threshold", min_value=0.10, max_value=1.00, value=0.25)
run_detection = st.sidebar.checkbox("Start Threat Monitoring", value=False)

FRAME_WINDOW = st.image([])

last_alert_time = 0
ALERT_COOLDOWN = 15

if run_detection:
    cap = cv2.VideoCapture(0)

    while run_detection:
        ret, frame = cap.read()
        if not ret:
            st.warning("Webcam frame read fail!")
            continue

        # YOLO Detection Execution
        results = model(frame, conf=confidence)
        annotated_frame = results[0].plot()

        threat_found = False
        detected_item = ""

        for box in results[0].boxes:
            class_id = int(box.cls[0])
            class_name = model.names[class_id]

            if class_name in DANGER_CLASSES:
                threat_found = True
                detected_item = class_name
                break

        current_time = time.time()

        if threat_found and (current_time - last_alert_time > ALERT_COOLDOWN):
            last_alert_time = current_time

            # 1. Save Image Capture
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            img_path = f"captures/threat_{timestamp}.jpg"
            cv2.imwrite(img_path, frame)
            st.toast(f"🚨 Threat Detected ({detected_item})! Image Captured.", icon="📸")

            try:
                pygame.mixer.stop()
                os.system('powershell -c "[console]::beep(1000, 1000)"')
            except Exception:
                pass

            # 2. Send Email
            send_email_alert(img_path)

        # Live Display Update
        annotated_frame_rgb = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
        FRAME_WINDOW.image(annotated_frame_rgb)

    cap.release()
else:
    st.info("Sidebar to ' Please check the Start Threat Monitoring' .")