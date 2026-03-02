import adi
import numpy as np
from datetime import datetime

# --- CONFIGURATION (VE) ---
SDR_URI = "ip:192.168.2.1"
TARGET_FREQ = 2245e6   # Standard S-Band Telemetry
SAMPLE_RATE = 2.5e6

def capture_stabilization_data():
    print(f"[{datetime.utcnow()}] Initiating Precision Doppler Lock...")
    
    try:
        # INITIALIZE (ASTRA)
        sdr = adi.Pluto(SDR_URI)
        sdr.sample_rate = int(SAMPLE_RATE)
        sdr.rx_lo = int(TARGET_FREQ)
        sdr.rx_buffer_size = 1024 * 10
        
        # Capture 5 frames for frequency averaging
        frames = [sdr.rx() for _ in range(5)]
        avg_signal = np.mean(frames, axis=0)
        
        # Find the Peak Truth
        fft_res = np.fft.fftshift(np.fft.fft(avg_signal))
        peak_idx = np.argmax(np.abs(fft_res))
        freq_bins = np.fft.fftshift(np.fft.fftfreq(len(avg_signal), 1/SAMPLE_RATE))
        
        actual_freq = TARGET_FREQ + freq_bins[peak_idx]
        doppler_shift = actual_freq - TARGET_FREQ
        
        print(f"TRUTH FOUND: {actual_freq/1e6:.4f} MHz")
        print(f"DOPPLER: {doppler_shift:.2f} Hz")
        
        # Log for TraCSS upload preparation
        with open("mission_logs/vh_truth_log.csv", "a") as f:
            f.write(f"{datetime.utcnow()},{actual_freq},{doppler_shift}\n")
            
    except Exception as e:
        print(f"System Alert: Stabilizer Offline. Error: {e}")
