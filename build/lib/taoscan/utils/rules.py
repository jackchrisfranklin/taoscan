import math

# ----------------------------
# BASIC ANALYSIS
# ----------------------------

def analyze(ffprobe_data, binwalk_data, size):
    flags = []

    if not isinstance(ffprobe_data, dict):
        flags.append("FFPROBE_INVALID")
    elif "error" in ffprobe_data:
        flags.append("FFPROBE_ERROR")
    elif "streams" not in ffprobe_data:
        flags.append("FFPROBE_NO_STREAMS")

    output = binwalk_data.get("output", "") if isinstance(binwalk_data, dict) else str(binwalk_data)

    if binwalk_data.get("returncode", 0) != 0:
        flags.append("BINWALK_ERROR")

    lower = output.lower()

    if "zip archive data" in lower:
        flags.append("ARCHIVE_SIGNATURE")

    if "elf" in lower:
        flags.append("EMBEDDED_BINARY_SIGNATURE")

    if size > 100 * 1024 * 1024:
        flags.append("VERY_LARGE_FILE")

    return flags


# ----------------------------
# SCORING
# ----------------------------

def score_file(flags):
    weights = {
        "FFPROBE_INVALID": 30,
        "FFPROBE_ERROR": 20,
        "FFPROBE_NO_STREAMS": 25,
        "BINWALK_ERROR": 10,
        "ARCHIVE_SIGNATURE": 35,
        "EMBEDDED_BINARY_SIGNATURE": 70,
        "VERY_LARGE_FILE": 5,
        "ENTROPY_HIGH": 20,
        "EOF_ANOMALY": 50
    }

    return min(100, sum(weights.get(f, 0) for f in flags))


# ----------------------------
# ENTROPY
# ----------------------------

def detect_entropy(path):
    with open(path, "rb") as f:
        data = f.read()

    if not data:
        return {"entropy": 0.0, "high": False}

    freq = [0] * 256

    for b in data:
        freq[b] += 1

    entropy = 0.0
    size = len(data)

    for f in freq:
        if f:
            p = f / size
            entropy -= p * math.log2(p)

    return {
        "entropy": round(entropy, 4),
        "high": entropy > 7.5
    }


# ----------------------------
# EOF DETECTION
# ----------------------------

def detect_eof_anomaly(path):
    with open(path, "rb") as f:
        data = f.read()

    if len(data) < 2048:
        return {"anomaly": False}

    tail = data[-2048:]

    if b"PK" in tail:
        return {"anomaly": True, "reason": "ZIP signature in tail"}

    if b"ELF" in tail:
        return {"anomaly": True, "reason": "ELF signature in tail"}

    if len(tail.strip(b"\x00")) > 300:
        return {"anomaly": True, "reason": "Non-zero trailing data"}

    return {"anomaly": False}


# ----------------------------
# STRUCTURE
# ----------------------------

def analyze_structure(ffprobe_data):
    if not isinstance(ffprobe_data, dict):
        return {"error": "invalid ffprobe data"}

    streams = ffprobe_data.get("streams", [])

    return {
        "stream_count": len(streams),
        "has_video": any(s.get("codec_type") == "video" for s in streams),
        "has_audio": any(s.get("codec_type") == "audio" for s in streams)
    }

# ----------------------------
# INTERPRET
# ----------------------------

def interpret(report):
    flags = report.get("flags", [])
    entropy = report.get("entropy", {})
    eof = report.get("eof_anomaly", {})
    score = report.get("risk_score", 0)

    messages = []

    if score <= 10:
        messages.append("This appears to be a normal media file with no strong indicators of tampering.")
    elif score <= 40:
        messages.append("Some unusual patterns were detected, but there is no strong indication of malicious content.")
    else:
        messages.append("Multiple suspicious indicators were detected. Further inspection is recommended.")

    if entropy.get("high"):
        messages.append("High entropy detected. This is typically normal for compressed video and audio files.")

    if eof.get("anomaly"):
        messages.append(f"Trailing data detected: {eof.get('reason')}. This can occur due to encoding or muxing artifacts.")

    if "VERY_LARGE_FILE" in flags:
        messages.append("Large file size detected. This is expected for high-definition video content.")

    return {
        "summary": messages,
        "risk_level": (
            "LOW" if score <= 10 else
            "MEDIUM" if score <= 40 else
            "HIGH"
        )
    }