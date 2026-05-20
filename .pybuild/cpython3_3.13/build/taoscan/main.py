import sys
from scanner import scan_file
import json

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <file>")
        return

    path = sys.argv[1]
    report = scan_file(path)

    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()