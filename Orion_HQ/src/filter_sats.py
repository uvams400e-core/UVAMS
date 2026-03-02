import os
from skyfield.api import load

def fetch_and_filter():
    # Mapping the URL to the local filename Skyfield uses
    sources = {
        'active': 'https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle',
        'weather': 'https://celestrak.org/NORAD/elements/gp.php?GROUP=weather&FORMAT=tle',
        'noaa': 'https://celestrak.org/NORAD/elements/gp.php?GROUP=noaa&FORMAT=tle' # THE MISSING PIECE
    }
    
    keywords = ["NOAA", "METOP", "GOES", "ARKTIKA"]
    combined_lines = []

    # Make sure data directory exists
    if not os.path.exists('data'):
        os.makedirs('data')

    for label, url in sources.items():
        print(f"[*] Fetching {label} group...")
        
        # We use 'filename' to force Skyfield to save it as something readable
        target_path = f"data/{label}.txt"
        load.tle_file(url, filename=target_path, reload=True)
        
        with open(target_path, 'r') as f:
            lines = f.readlines()
            for i in range(0, len(lines), 3):
                try:
                    name = lines[i].strip()
                    if any(key in name.upper() for key in keywords):
                        combined_lines.extend(lines[i:i+3])
                except IndexError:
                    break

    # Save the final lean target list
    with open("data/targets.txt", "w") as f:
        f.writelines(combined_lines)
    
    print(f"[*] Success: targets.txt now contains {len(combined_lines)//3} mission-critical satellites.")

if __name__ == "__main__":
    fetch_and_filter()
