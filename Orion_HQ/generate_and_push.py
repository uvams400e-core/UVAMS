import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# 1. Create 1,050 Signal Data Points
n = 1050
times = [datetime.utcnow() - timedelta(minutes=i) for i in range(n)]
doppler = np.random.uniform(-5000, 15000, n)
snr = np.random.uniform(5, 50, n)
# Logic: Anomalous doppler/low SNR flagged as ghost
labels = ['ghost_signal' if d > 8500 or s < 12 else 'known_sat' for d, s in zip(doppler, snr)]

df = pd.DataFrame({
    'timestamp': [t.isoformat() for t in times],
    'center_freq': np.random.choice([2245.0, 2280.0], n),
    'doppler_shift': doppler,
    'snr': snr,
    'signal_type': labels
})

# 2. Save and Push to the Lake
df.to_csv('vertex_pilot_data.csv', index=False)
os.system("gsutil cp vertex_pilot_data.csv gs://uvams-pluto-data-lake/training/")
print("--- PILOT DATA UPLOADED TO UVAMS DATA LAKE ---")
