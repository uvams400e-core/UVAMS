import os
import hashlib

def generate_secret_handshake(node_id):
    # Our secret key we agreed on
    mission_secret = "Marfa-Pi"
    
    # Simple 'Secret Math': ID + Secret Key
    # In the future, we can add time-based salts here
    raw_string = f"{node_id}-{mission_secret}"
    
    # Create a unique hash (The Digital Fingerprint)
    return hashlib.sha256(raw_string.encode()).hexdigest()[:10]

def verify_member(node_id, provided_token):
    expected = generate_secret_handshake(node_id)
    if provided_token == expected:
        print(f"Handshake Verified: Welcome to the family, {node_id}!")
        return True
    else:
        print(f"SECURITY ALERT: Node {node_id} failed the Marfa-Pi handshake!")
        return False

# Quick test for our eyes only
if __name__ == "__main__":
    test_id = "VH3"
    token = generate_secret_handshake(test_id)
    print(f"Secret Token for {test_id}: {token}")
