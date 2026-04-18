st.set_page_config(
    page_title="AgroScan AI",
    page_icon="🌾",
    layout="wide"
)

st.markdown("""
<h1 style='text-align: center; color: green;'>🌾 AgroScan AI</h1>
<h4 style='text-align: center;'>Smart Crop Health Monitoring System</h4>
""", unsafe_allow_html=True)
st.info("📸 Upload a clear image of crop leaves to analyze health condition.")
import streamlit as st
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

st.set_page_config(page_title="Crop Monitoring System", layout="wide")

st.title("🌾 Drone-Based Crop Health Monitoring System")

uploaded_file = st.file_uploader("📤 Upload Crop Image", type=["jpg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    
    col1, col2 = st.columns(2)

    with col1:
        st.image(image, caption="Original Image")

    img = np.array(image.convert("RGB"))
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    # Green detection
    lower_green = np.array([25, 40, 40])
    upper_green = np.array([90, 255, 255])

    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Diseased = not green
    diseased_mask = cv2.bitwise_not(mask)

    # Highlight diseased area in RED
    highlighted = img.copy()
    highlighted[diseased_mask > 0] = [255, 0, 0]

    with col2:
        st.image(highlighted, caption="Diseased Area Highlighted")

    # Calculate percentage
    green_pixels = cv2.countNonZero(mask)
    total_pixels = img.size / 3
    health_percentage = (green_pixels / total_pixels) * 100
    disease_percentage = 100 - health_percentage

    st.subheader("📊 Analysis")

    st.write(f"🌱 Healthy: {health_percentage:.2f}%")
    st.write(f"🍂 Diseased: {disease_percentage:.2f}%")

    # Graph
    fig, ax = plt.subplots()
    ax.bar(["Healthy", "Diseased"], [health_percentage, disease_percentage])
    ax.set_ylabel("Percentage")
    ax.set_title("Crop Health Analysis")

    st.pyplot(fig)

    # Final result
    if health_percentage > 50:
        st.success("✅ Crop is Healthy")
    else:
        st.error("❌ Crop is Diseased")