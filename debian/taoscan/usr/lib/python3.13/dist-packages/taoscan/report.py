import json

def print_report(report, as_json=False):
    if as_json:
        print(json.dumps(report, indent=2))
    else:
        print("FILE:", report["file"])
        print("SIZE:", report["size"])
        print("\n--- FFPROBE ---")
        print(report["ffprobe"])
        print("\n--- BINWALK ---")
        print(report["binwalk"])
