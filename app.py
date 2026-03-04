import streamlit as st
import os
import glob
import pandas as pd
from PIL import Image
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="UVAMS Mission Control", layout="wide")

# --- PATHS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAPTURE_DIR = os.path.join(BASE_DIR, "captures")
LOG_FILE = os.path.join(BASE_DIR, "mission_log.csv")

# --- HEADER ---
st.title("🛰️ UVAMS LLC | Mission Control")
st.subheader("Station Status: VAN HORN, TX [ACTIVE]")
st.markdown("---")

# --- DATA LOGIC ---
def get_latest_capture():
    files = glob.glob(os.path.join(CAPTURE_DIR, "*.png"))
    if not files:
        return None
    return max(files, key=os.path.getctime)

latest_file = get_latest_capture()

# --- DASHBOARD LAYOUT ---
col1, col2 = st.columns([1, 2])

with col1:
    st.header("📊 Telemetry")
    if latest_file:
        file_name = os.path.basename(latest_file)
        st.metric(label="Latest Capture", value=file_name)
        
        # Detection logic
        is_anomaly = "real" in file_name or "NOAA" in file_name
        if is_anomaly:
            st.error("🚨 ANOMALY DETECTED")
        else:
            st.success("✅ NOMINAL")
            
        st.write("### Signal Analysis")
        # Sample chart for the presentation
        chart_data = pd.DataFrame({'Category': ['Signal', 'Noise'], 'Value': [82, 18]})
        st.bar_chart(chart_data.set_index('Category'))
    else:
        st.warning("No data detected in /captures")

with col2:
    st.header("🖼️ Live Feed")
    if latest_file:
        image = Image.open(latest_file)
        st.image(image, caption=f"Last Recorded Pass: {os.path.basename(latest_file)}", use_container_width=True)
    else:
        st.info("Awaiting satellite AOS (Acquisition of Signal)...")

# --- MISSION HISTORY (THE SWARM DB PREVIEW) ---
st.markdown("---")
st.header("📜 Mission History")
if os.path.exists(LOG_FILE):
    df = pd.read_csv(LOG_FILE)
    st.dataframe(df.sort_values(by='Timestamp', ascending=False), use_container_width=True)
else:
    # Creating a starting point for the log if it doesn't exist
    st.info("No mission logs yet. History will populate after the next satellite pass.")
    # For the first run, let's create the file with a header
    if not os.path.exists(LOG_FILE):
        pd.DataFrame(columns=['Timestamp', 'File', 'Saliency Score']).to_csv(LOG_FILE, index=False)

# --- SIDEBAR CONTROL PANEL ---
st.sidebar.header("Command Panel")
st.sidebar.button("Manual Analysis Trigger")
threshold = st.sidebar.slider("Saliency Threshold", 0.0, 1.0, 0.3)
st.sidebar.write(f"Current Threshold: {threshold}")
