# Orion_HQ/security_monitor/shield.py
from cryptography.fernet import Fernet
import os

# Use the 'orion-key.json' we just agreed on
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEY_PATH = os.path.join(BASE_DIR, "keys", "orion-key.json")

def load_key():
    return open(KEY_PATH, "rb").read()

def encrypt_packet(data_string):
    """Turns cleartext JSON into encrypted bytes (matches orion_brain)."""
    f = Fernet(load_key())
    return f.encrypt(data_string.encode())

def decrypt_packet(encrypted_bytes):
    """Turns encrypted bytes back into JSON."""
    f = Fernet(load_key())
    return f.decrypt(encrypted_bytes).decode()
