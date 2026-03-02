import sqlite3
import os
from pathlib import Path  # Added missing import

# 1. Consistent path for all Marfa Pi family members
# BASE_DIR finds the Orion_HQ folder relative to this file
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. Logic to handle /app/data/a/ vs local data/a/
# If UVAMS_DB_PATH is not set in environment, it defaults to your project folder
DEFAULT_PATH = str(BASE_DIR / "data" / "a" / "mission_vault.db")
DB_PATH = os.getenv("UVAMS_DB_PATH", DEFAULT_PATH)

# 3. Ensure the directory exists (Self-Healing logic)
# This creates data/a/ if it doesn't exist on your Mac or the Pi
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def get_db_connection():
    """Establishes connection to the local SQLite vault."""
    return sqlite3.connect(DB_PATH)

def init_vault():
    """Initializes the database and ensures all tables exist (The Healing Logic)."""
    conn = get_db_connection()
    c = conn.cursor()
    
    # 1. Create table for satellite hits with all mission-critical columns
    c.execute('''CREATE TABLE IF NOT EXISTS satellite_hits 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, 
                  node_id TEXT, 
                  snr REAL, 
                  power REAL, 
                  sat_name TEXT, 
                  frequency REAL, 
                  alt REAL, 
                  az REAL, 
                  type TEXT, 
                  ingested INTEGER DEFAULT 0)''')
    
    # 2. Create table for peer health (The "Family" Heartbeat)
    c.execute('''CREATE TABLE IF NOT EXISTS astro_health 
                 (peer_id TEXT PRIMARY KEY, 
                  last_seen DATETIME, 
                  status TEXT)''')
    
    conn.commit()
    conn.close()
    print(f"✅ Vault Initialized at: {DB_PATH}")

def save_hit(node_id, snr, power, sat_name, freq, alt, az, hit_type="SIM"):
    """Persists a new satellite detection and heals the DB if missing."""
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("""INSERT INTO satellite_hits 
                     (node_id, snr, power, sat_name, frequency, alt, az, type) 
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", 
                  (node_id, snr, power, sat_name, freq, alt, az, hit_type))
        conn.commit()
        conn.close()
    except sqlite3.OperationalError as e:
        if "no such table" in str(e):
            print(f"⚠️ {node_id} detected missing table! Auto-healing now...")
            init_vault() # Re-create the tables
            save_hit(node_id, snr, power, sat_name, freq, alt, az, hit_type) # Try again
        else:
            print(f"❌ DB Error: {e}")
            raise e
