import numpy as np
import yaml
import time
import os
import random
import adi
import math
from skyfield.api import Topos, load
from src.vault import init_vault, save_hit

def run_mission():
    # 1. DOCKER IDENTITY & CONFIG
    node_id = os.getenv('NODE_ID', 'VAN_HORN_UNKNOWN')
    pluto_ip = os.getenv('PLUTO_IP', 'ip:192.168.2.1')
    
    # Initialize the local database (The Vault)
    init_vault()
    
    try:
        with open("config/uvams_config.yaml", 'r') as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"[!] {node_id} Error: config/uvams_config.yaml not found.")
        return

    STATION_LOCATION = Topos(config['station']['lat'], config['station']['lon'])
    ts = load.timescale()
    tle_path = 'data/targets.txt'
    last_tle_reload = time.time()
    
    # 2. SDR INITIALIZATION (With Simulation Fallback)
    sdr = None
    try:
        print(f"📡 {node_id} attempting connection to {pluto_ip}...")
        sdr = adi.Pluto(pluto_ip)
        # Apply SDR settings from config
        sdr.rx_lo = int(config['sdr'].get('center_freq_hz', 137100000))
        sdr.sample_rate = int(config['sdr'].get('sample_rate', 2000000))
        print(f"✅ {node_id} SDR Active at {sdr.rx_lo/1e6} MHz")
    except Exception as e:
        print(f"⚠️ {node_id} Hardware Offline: {e}. Entering SIMULATION MODE.")

    # 3. MISSION LOOP
    print(f"[*] {node_id} Mission Loop Started.")
    
    while True:
        try:
            # DYNAMIC RELOAD: Check if 6 hours have passed
            if (time.time() - last_tle_reload) > 21600:
                print(f"[*] {node_id}: Reloading TLE library...")
                last_tle_reload = time.time()

            if sdr:
                # --- REAL HARDWARE CAPTURE ---
                samples = sdr.rx()
                p_total = np.mean(np.abs(samples)**2)
                p_noise = np.median(np.abs(samples)**2)
                snr = 10 * np.log10(p_total / p_noise) if p_noise > 0 else 0
                
                # Check thresholds from config
                if p_total > config['sdr'].get('threshold', 15000):
                    # Placeholder for match_name logic from your TLE library
                    match_name = "Unknown RFI" 
                    
                    save_hit(
                        node_id=node_id,
                        snr=round(float(snr), 2),
                        power=round(float(p_total), 2),
                        sat_name=match_name,
                        freq=sdr.rx_lo / 1e6,
                        alt=0.0, # Replace with actual skyfield calculation
                        az=0.0,  # Replace with actual skyfield calculation
                        hit_type="REAL"
                    )
                    print(f"[*] {node_id} | REAL HIT | SNR: {snr:.2f}dB")
            
            else:
# --- SIMULATION CAPTURE (Synchronized across all nodes) ---
                
                t = time.time()
                
                # 1. Master Clock Math: 1 degree of Azimuth movement per second
                mock_az = round(t % 360, 1)
                
                # 2. Master Clock Math: Altitude follows a 10-minute pass arc (0 to 90 degrees)
                # This ensures all nodes see the satellite "rise" and "set" together
                mock_alt = round(max(0, 90 * math.sin((t % 600) * (math.pi / 600))), 1)
                
                # 3. Intelligent Signal: SNR is better when the satellite is higher in the sky
                base_snr = 12.0
                alt_bonus = (mock_alt / 90) * 12 # Up to +12dB at the Zenith (90 degrees)
                mock_snr = round(base_snr + alt_bonus + random.uniform(-0.5, 0.5), 2)
                
                mock_power = round(random.uniform(14000, 18000), 2)

                save_hit(
                    node_id=node_id,
                    snr=mock_snr,
                    power=mock_power,
                    sat_name="UVAMS-ALPHA-SIM", # Updated name for your Git check-in
                    freq=137.1,
                    alt=mock_alt,
                    az=mock_az,
                    hit_type="SIM"
                )
                print(f"📡 {node_id} [SYNC] Pulse: {mock_snr}dB | Alt: {mock_alt}° | Az: {mock_az}°")

            # Control loop speed from config
            time.sleep(config['processing'].get('sleep_interval_sec', 5.0))

        except KeyboardInterrupt:
            print(f"\n[!] {node_id} Mission Terminated by Operator.")
            break
        except Exception as e:
            print(f"❌ {node_id} Loop Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    run_mission()
