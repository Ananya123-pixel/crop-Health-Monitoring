import streamlit as st
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import random

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="AgroScan AI", layout="centered")

st.title("🌾 AgroScan AI - Smart Agriculture System")
st.markdown("---")

# =========================
# IMAGE UPLOAD
# =========================
uploaded_file = st.file_uploader("📤 Upload Crop / Soil Image", type=["jpg","png","jpeg"])

# =========================
# FUNCTIONS
# =========================

# 🌱 Crop Health Detection
def analyze_crop(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    lower_green = np.array([25,40,40])
    upper_green = np.array([90,255,255])

    mask = cv2.inRange(hsv, lower_green, upper_green)
    diseased = cv2.bitwise_not(mask)

    green = cv2.countNonZero(mask)
    total = img.shape[0]*img.shape[1]

    health = (green/total)*100
    disease = 100 - health

    return health, disease, diseased

# 🧠 Disease Classification
def classify_disease(d):
    if d < 20:
        return "Healthy"
    elif d < 40:
        return "Mild Disease"
    elif d < 70:
        return "Moderate Disease"
    else:
        return "Severe Disease"

# 🌱 Soil Analysis
def analyze_soil(img):
    avg = np.mean(img, axis=(0,1))

    if avg[0] > avg[1] and avg[0] > avg[2]:
        return "Red Soil","5.5-6.5","Iron rich","Wheat, Millet"
    elif avg[1] > avg[0]:
        return "Alluvial Soil","6.5-7.5","Balanced","Rice, Sugarcane"
    else:
        return "Black Soil","7.5-8.5","Potassium rich","Cotton, Soybean"

# 💧 Moisture Detection
def moisture(img):
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    val = np.mean(gray)

    if val < 80:
        return "High Moisture"
    elif val < 150:
        return "Moderate Moisture"
    else:
        return "Low Moisture"

# 🌦 Weather Risk Simulation
def weather_factor():
    return random.randint(20,80)

# 🔮 Future Risk Prediction
def predict_risk(disease, weather):
    score = (0.7*disease + 0.3*weather)

    if score < 30:
        return "Low Risk"
    elif score < 60:
        return "Medium Risk"
    else:
        return "High Risk"

# 💊 Advice System
def advice(disease_level, soil):
    if disease_level == "Healthy":
        return "Maintain irrigation and sunlight"
    elif disease_level == "Mild Disease":
        return "Use neem spray + remove infected leaves"
    elif disease_level == "Moderate Disease":
        return "Apply fungicide + improve soil drainage"
    else:
        return "Apply pesticide immediately and isolate crops"

# =========================
# MAIN
# =========================

if uploaded_file:

    image = Image.open(uploaded_file)
    img = np.array(image.convert("RGB"))

    st.image(image, caption="📷 Uploaded Image")

    # Crop Analysis
    health, disease, mask = analyze_crop(img)
    disease_type = classify_disease(disease)

    # Soil Analysis
    soil, ph, nutrients, crops = analyze_soil(img)
    moisture_level = moisture(img)

    # Weather + Risk
    weather = weather_factor()
    risk = predict_risk(disease, weather)

    # Highlight
    highlighted = img.copy()
    highlighted[mask > 0] = [255,0,0]

    st.image(highlighted, caption="🔴 Diseased Area Highlighted")

    # =========================
    # RESULTS
    # =========================
    st.subheader("📊 Crop Health")
    st.metric("🌱 Health %", f"{health:.2f}")
    st.metric("🍂 Disease %", f"{disease:.2f}")
    st.success(f"🧠 Disease Type: {disease_type}")

    # =========================
    # SOIL
    # =========================
    st.subheader("🌱 Soil Intelligence")
    
    st.write(f"⚗️ pH Level: {ph}")
    st.write(f"🧪 Nutrients: {nutrients}")
    st.write(f"🌾 Suitable Crops: {crops}")
    st.write(f"💧 Moisture: {moisture_level}")

    # =========================
    # WEATHER + RISK
    # =========================
    st.subheader("🔮 Future Prediction")
    st.write(f"🌦 Weather Stress: {weather}/100")
    st.error(f"⚠️ Risk Level: {risk}")

    # =========================
    # ADVICE
    # =========================
    st.subheader("💊 Smart Recommendation")
    st.info(advice(disease_type, soil))

    # =========================
    # GRAPH
    # =========================
    fig, ax = plt.subplots()
    ax.pie([health, disease], labels=["Healthy","Diseased"], autopct="%1.1f%%")
    st.pyplot(fig)

else:
    st.info("👆 Upload image to start analysis")
