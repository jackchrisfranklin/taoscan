import argparse
import json
from taoscan.scanner import scan_file
from taoscan.sanitizer import sanitize_video, sanitize_reencode, extract_suspicious_data

def main():
    parser = argparse.ArgumentParser(description="taoscan - forensic video scanner")

    parser.add_argument("file", help="Path to video file")

    # scan features
    parser.add_argument("--score", action="store_true")
    parser.add_argument("--entropy", action="store_true")
    parser.add_argument("--structure", action="store_true")
    parser.add_argument("--eof", action="store_true")

    # sanitizer features
    parser.add_argument("--sanitize", action="store_true")
    parser.add_argument("--rebuild", action="store_true")
    parser.add_argument("--extract", action="store_true")
    parser.add_argument("--out", help="Output file path")

    parser.add_argument("--interpret", action="store_true")

    args = parser.parse_args()

    # --- scan phase ---
    report = scan_file(
        args.file,
        enable_score=args.score,
        enable_entropy=args.entropy,
        enable_structure=args.structure,
        enable_eof=args.eof
    )

    print(json.dumps(report, indent=2))

    # --- sanitize / forensic actions ---
    if args.sanitize:
        out = args.out or f"{args.file}"
        result = sanitize_video(args.file, out)
        print("\n[SANITIZE]", json.dumps(result, indent=2))

    if args.rebuild:
        out = args.out or f"rebuild_{args.file}"
        result = sanitize_reencode(args.file, out)
        print("\n[REBUILD]", json.dumps(result, indent=2))

    if args.extract:
        result = extract_suspicious_data(args.file, ".")
        print("\n[EXTRACT]", json.dumps(result, indent=2))
    
    if args.interpret:
        from taoscan.utils.rules import interpret

        result = interpret(report)
        print("\nINTERPRETATION")
        print("--------------")
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
