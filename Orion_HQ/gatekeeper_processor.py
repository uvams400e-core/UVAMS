# Orion_HQ/gatekeeper_processor.py
def process_harvested_data(mule_payload):
    for packet in mule_payload:
        # 1. Decrypt what the Pi caught
        raw_signal = decrypt_packet(packet)
        
        # 2. Check the SNR (already calculated by the Pi)
        if raw_signal['snr'] > 15:
            # 3. ONLY NOW do we use the internet/Vertex AI
            # This happens on your laptop, not in the field!
            tag = call_vertex_ai(raw_signal)
            raw_signal['ai_tag'] = tag
        
        # 4. Final Push to GCP
        upload_to_gcp(raw_signal)
