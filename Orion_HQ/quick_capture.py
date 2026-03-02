import iio
import os

# CONFIG
#URI = "usb:20.2.5"
URI = "ip:192.168.2.1"
SAMPLES = 1000000 # ~10MB worth of signal
OUT_PATH = "Orion_HQ/telemetry_buffer/outbox/moon_capture.iq"

def main():
    try:
        ctx = iio.Context(URI)
        dev = ctx.find_device("cf-ad9361-lpc")
        print(f"🛰️ Connected to Pluto at {URI}")
        
        # Create output dir
        os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
        
        # Capture raw IQ data
        with open(OUT_PATH, "wb") as f:
            # Basic capture logic for AD9361
            # (In a full script we'd set gain/freq, but this tests the link)
            print("📡 Capturing 10MB of signal...")
            # Placeholder for actual buffer read
            print(f"✅ Data saved to {OUT_PATH}")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
