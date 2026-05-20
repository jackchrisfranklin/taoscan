import os
from taoscan.tools import run_ffprobe, run_binwalk
from taoscan.utils.rules import (
    analyze,
    score_file,
    detect_entropy,
    detect_eof_anomaly,
    analyze_structure
)

def scan_file(path, enable_score=False, enable_entropy=False, enable_structure=False, enable_eof=False):

    if not os.path.isfile(path):
        return {"error": "File not found"}

    size = os.path.getsize(path)

    ffprobe_data = run_ffprobe(path)
    binwalk_data = run_binwalk(path)

    flags = analyze(ffprobe_data, binwalk_data, size)

    report = {
        "file": path,
        "size": size,
        "ffprobe": ffprobe_data,
        "binwalk": binwalk_data,
        "flags": flags
    }

    if enable_entropy:
        report["entropy"] = detect_entropy(path)

    if enable_structure:
        report["structure"] = analyze_structure(ffprobe_data)

    if enable_eof:
        report["eof_anomaly"] = detect_eof_anomaly(path)

    if enable_score:
        report["risk_score"] = score_file(flags)

    return report