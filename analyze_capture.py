import cv2
import numpy as np
import os
import glob
import pandas as pd
from datetime import datetime

# --- SETTINGS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAPTURE_DIR = os.path.join(BASE_DIR, "captures")
LOG_FILE = os.path.join(BASE_DIR, "mission_log.csv")

def run_analysis():
    print(f"--- UVAMS DEBUG: Checking {CAPTURE_DIR} ---")
    
    # 1. Get the latest file
    files = glob.glob(os.path.join(CAPTURE_DIR, "*.png"))
    if not files:
        print("ERROR: No files found in captures folder!")
        return
    
    latest_file = max(files, key=os.path.getctime)
    file_name = os.path.basename(latest_file)
    print(f"DEBUG: Analyzing {file_name}...")

    # 2. Compute Saliency
    img = cv2.imread(latest_file)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    saliency = cv2.saliency.StaticSaliencySpectralResidual_create()
    (success, saliency_map) = saliency.computeSaliency(gray)
    score = np.mean(saliency_map)
    print(f"DEBUG: Saliency Score calculated: {score:.4f}")

    # 3. Force Write to CSV
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_data = pd.DataFrame([[timestamp, file_name, round(score, 4)]], 
                            columns=['Timestamp', 'File', 'Saliency Score'])
    
    if not os.path.isfile(LOG_FILE):
        new_data.to_csv(LOG_FILE, index=False)
    else:
        new_data.to_csv(LOG_FILE, mode='a', header=False, index=False)
    
    print(f"SUCCESS: Data written to {LOG_FILE}")
    
    # 4. Print the Big Banner
    print("\n" + "!"*40)
    print("  UVAMS GLOBAL WORKSPACE BROADCAST  ")
    print(f"  Anomaly Detected in {file_name}")
    print("!"*40 + "\n")

if __name__ == "__main__":
    try:
        run_analysis()
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")

