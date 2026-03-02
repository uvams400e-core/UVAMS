import sys
from src.engine import run_mission
from src.utils import generate_report

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--report":
        generate_report()
    else:
        print("🚀 UVAMS Mission Starting...")
        run_mission()
