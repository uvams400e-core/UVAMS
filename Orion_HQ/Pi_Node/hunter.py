# Pi_Node/hunter.py
import os
import time
from math import log10

def get_snr(signal_chunk):
    # Extremely light math: Compare signal peak to noise floor
    # No heavy libraries like NumPy needed if we optimize for power
    p_signal = max(signal_chunk)**2
    p_noise = sum(signal_chunk[-10:]) / 10 # Sample end of buffer for noise
    return 10 * log10(p_signal / p_noise) if p_noise > 0 else 0

def start_passive_hunt():
    threshold = 12 # 12dB - only keep 'loud' signals
    while True:
        raw_bits = capture_from_sdr() # Low-level capture
        
        snr = get_snr(raw_bits)
        
        if snr > threshold:
            # ONLY encrypt and save if it's worth the SD card write-cycle
            save_to_outbox(raw_bits, snr) 
        
        # Long sleep to keep the Pi cool
        time.sleep(5)
