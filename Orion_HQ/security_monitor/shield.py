# Save as security_monitor/shield.py
from cryptography.fernet import Fernet
import os

KEY_PATH = "security_monitor/mission.key"

def load_key():
    return open(KEY_PATH, "rb").read()

def encrypt_yield(data_string):
    """Turns cleartext JSON into encrypted bytes."""
    f = Fernet(load_key())
    return f.encrypt(data_string.encode())

def decrypt_yield(encrypted_bytes):
    """Turns encrypted bytes back into JSON (for the Cloud Lake/Laptop)."""
    f = Fernet(load_key())
    return f.decrypt(encrypted_bytes).decode()
