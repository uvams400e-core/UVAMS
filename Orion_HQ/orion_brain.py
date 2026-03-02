# Orion_HQ/orion_brain.py
import os
import json
from google.cloud import aiplatform
from google.oauth2 import service_account
from Orion_HQ.security_monitor.shield import encrypt_packet

# --- CONFIGURATION ---
PROJECT_ID = "uvams400e-core"
LOCATION = "us-central1"
# This is a placeholder for your deployed Vertex AI Endpoint ID
# You can find this in your Google Cloud Console under Vertex AI > Endpoints
ENDPOINT_ID = "ORION_SIGNAL_TAGGER_v1" 
KEY_PATH = "Orion_HQ/keys/orion-key.json"

def analyze_signal(raw_telemetry):
    """
    AI Observer: Categorizes signals using Vertex AI without 
    ever deleting or modifying the raw data.
    """
    ai_label = "UNVERIFIED" # Default safety state
    confidence = 0.0

    try:
        # 1. Load Credentials securely from your local key
        if os.path.exists(KEY_PATH):
            credentials = service_account.Credentials.from_service_account_file(KEY_PATH)
            aiplatform.init(project=PROJECT_ID, location=LOCATION, credentials=credentials)
            
            # 2. Call the Vertex AI Endpoint
            # Note: We wrap this in a try/except so code doesn't crash if AI is offline
            endpoint = aiplatform.Endpoint(endpoint_name=ENDPOINT_ID)
            
            # Vertex expects a list of instances
            response = endpoint.predict(instances=[raw_telemetry])
            
            # 3. Extract Prediction (Assumes your model returns a 'label' and 'score')
            if response.predictions:
                prediction = response.predictions[0]
                # Adjust these keys based on your specific model's output schema
                ai_label = prediction.get("label", "UNKNOWN_SIGNAL")
                confidence = prediction.get("confidence", 0.0)
        else:
            print(f"⚠️ Security Alert: Key not found at {KEY_PATH}. Proceeding with UNVERIFIED tag.")

    except Exception as e:
        # Fail Gracefully: The mission continues even if the AI 'brain' is sleepy
        print(f"🤖 AI Brain Note: Vertex AI is unreachable or not yet configured. Tagging as UNVERIFIED. (Error: {e})")

    # 4. Create the Smart Packet (Raw Data + AI Metadata)
    smart_packet = {
        "raw_data": raw_telemetry,
        "ai_analysis": {
            "label": ai_label,
            "confidence": confidence,
            "engine": "VertexAI-Orion-v1",
            "safety_check": "Pass - No Data Removed"
        }
    }
    
    return smart_packet

def secure_mission_data(raw_data):
    """
    High-level wrapper to Tag, then Shield.
    """
    # Tag with AI
    smart_packet = analyze_signal(raw_data)
    
    # Encrypt the entire structure for the 'Shield' layer
    # This turns the JSON into an unreadable string for unauthorized users
    encrypted_blob = encrypt_packet(json.dumps(smart_packet))
    
    return encrypted_blob, smart_packet
