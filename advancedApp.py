import streamlit as st
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="AgroScan AI Pro",
    page_icon="🌾",
    layout="wide"
)

st.title(" AgroScan AI Pro - Smart Agriculture Intelligence System")
st.markdown("---")

# =========================
# INPUT
# =========================
uploaded_file = st.file_uploader("📤 Upload Crop Image", type=["jpg", "png", "jpeg"])

# =========================
# DISEASE DATABASE (SIMPLIFIED AI KNOWLEDGE BASE)
# =========================
disease_db = {
    "Healthy Crop": {
        "cure": "No treatment needed. Maintain irrigation and sunlight.",
        "fertilizer": "Balanced NPK (10-10-10)"
    },
    "Mild Disease": {
        "cure": "Use organic neem spray and remove affected leaves.",
        "fertilizer": "Nitrogen-rich fertilizer (Urea low dose)"
    },
    "Moderate Disease": {
        "cure": "Apply fungicide spray (Bordeaux mixture). Improve soil drainage.",
        "fertilizer": "Phosphorus + Potassium rich fertilizer"
    },
    "Severe Disease": {
        "cure": "Apply chemical pesticide and isolate affected crops immediately.",
        "fertilizer": "Special recovery fertilizer (High Potassium + micronutrients)"
    }
}

# =========================
# FUNCTIONS
# =========================

def preprocess(image):
    return np.array(image.convert("RGB"))

def detect_crop_health(img):

    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    lower_green = np.array([25, 40, 40])
    upper_green = np.array([90, 255, 255])

    green_mask = cv2.inRange(hsv, lower_green, upper_green)
    diseased_mask = cv2.bitwise_not(green_mask)

    green = cv2.countNonZero(green_mask)
    total = img.shape[0] * img.shape[1]

    health = (green / total) * 100
    disease = 100 - health

    return health, disease, diseased_mask

def classify_disease(disease_percentage):

    if disease_percentage < 20:
        return "Healthy Crop"
    elif disease_percentage < 40:
        return "Mild Disease"
    elif disease_percentage < 70:
        return "Moderate Disease"
    else:
        return "Severe Disease"

def predict_future_risk(disease_percentage, weather_factor):

    # Simple AI risk model (you can replace with ML later)
    risk_score = (disease_percentage * 0.7) + (weather_factor * 0.3)

    if risk_score < 25:
        return "Low Risk (Crop Safe)"
    elif risk_score < 50:
        return "Medium Risk (Monitor Closely)"
    else:
        return "High Risk (Crop may be damaged)"

def weather_factor_simulation():
    # Fake weather intelligence (can connect API later)
    # 0 = good weather, 100 = bad weather
    return np.random.randint(20, 80)

# =========================
# MAIN APP
# =========================

if uploaded_file:

    image = Image.open(uploaded_file)
    img = preprocess(image)

    col1, col2 = st.columns(2)

    with col1:
        st.image(image, caption="Original Crop Image")

    health, disease, mask = detect_crop_health(img)

    highlighted = img.copy()
    highlighted[mask > 0] = [255, 0, 0]

    with col2:
        st.image(highlighted, caption="Disease Detection (Red Areas)")

    # =========================
    # CLASSIFICATION
    # =========================
    disease_type = classify_disease(disease)

    cure_info = disease_db[disease_type]["cure"]
    fertilizer_info = disease_db[disease_type]["fertilizer"]

    # =========================
    # DISPLAY RESULTS
    # =========================
    st.subheader("📊 Crop Health Report")

    st.metric("🌱 Health %", f"{health:.2f}")
    st.metric("🍂 Disease %", f"{disease:.2f}")

    st.success(f"🧠 Disease Type: {disease_type}")

    # =========================
    # CURE + FERTILIZER
    # =========================
    st.subheader("💊 Treatment & Fertilizer Recommendation")

    st.write("### 🧪 Cure Plan")
    st.info(cure_info)

    st.write("### 🌿 Recommended Fertilizer")
    st.warning(fertilizer_info)

    # =========================
    # FUTURE RISK PREDICTION
    # =========================
    st.subheader("🔮 Future Crop Risk Prediction")

    weather_factor = weather_factor_simulation()

    risk = predict_future_risk(disease, weather_factor)

    st.write(f"🌦 Weather Stress Factor: {weather_factor}/100")
    st.error(f"⚠️ Risk Prediction: {risk}")

    # =========================
    # CHART
    # =========================
    fig, ax = plt.subplots()
    ax.pie([health, disease], labels=["Healthy", "Diseased"], autopct="%1.1f%%")
    ax.set_title("Crop Condition Distribution")
    st.pyplot(fig)

else:
    st.info("👆 Upload a crop image to start AI analysis")