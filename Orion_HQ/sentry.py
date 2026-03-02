import adi
import numpy as np
import time
from datetime import datetime

# --- CONFIGURATION (VE) ---
# When you get to VH, you can adjust these ranges
SDR_URI = "ip:192.168.2.1"
START_FREQ = 2200e6  # 2.2 GHz (S-Band Start)
END_FREQ = 2300e6    # 2.3 GHz (S-Band End)
STEP_SIZE = 2.5e6    # Frequency hop per step
THRESHOLD = 40.0     # Signal power threshold in dB

def auto_sweep_mission():
    print(f"[{datetime.utcnow()}] Initiating VH Sentry Sweep...")
    
    try:
        # INITIALIZE HARDWARE (ASTRA)
        sdr = adi.Pluto(SDR_URI)
        sdr.sample_rate = int(STEP_SIZE)
        sdr.rx_buffer_size = 1024
        
        current_f = START_FREQ
        
        while current_f <= END_FREQ:
            sdr.rx_lo = int(current_f)
            samples = sdr.rx()
            
            # Calculate average power of the capture
            power = 10 * np.log10(np.mean(np.abs(samples)**2))
            
            # If power exceeds the desert silence, log it as an Ace
            if power > THRESHOLD:
                print(f"ALERT: Signal Found at {current_f/1e6:.2f} MHz | Power: {power:.2f} dB")
                
                # Internal Log entry
                with open("mission_logs/vh_sentry_log.csv", "a") as f:
                    f.write(f"{datetime.utcnow()},{current_f},{power}\n")
            
            current_f += STEP_SIZE
            time.sleep(0.05) # Fast hop
            
        print("--- Sweep Cycle Complete ---")
        
    except Exception as e:
        print(f"System Alert: Hardware not detected. Error: {e}")
