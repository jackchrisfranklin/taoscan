import subprocess

# ----------------------------
# SAFE COPY (REMOVE METADATA + JUNK)
# ----------------------------

def sanitize_video(input_path, output_path):
    cmd = [
        "ffmpeg",
        "-i", input_path,
        "-map", "0",
        "-c", "copy",
        "-map_metadata", "-1",
        "-y",
        output_path
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    return {
        "success": result.returncode == 0,
        "error": result.stderr if result.returncode != 0 else None,
        "output": output_path
    }


# ----------------------------
# FULL RE-ENCODE CLEANING
# ----------------------------

def sanitize_reencode(input_path, output_path):
    cmd = [
        "ffmpeg",
        "-i", input_path,
        "-c:v", "libx264",
        "-c:a", "aac",
        "-movflags", "+faststart",
        "-y",
        output_path
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    return {
        "success": result.returncode == 0,
        "error": result.stderr if result.returncode != 0 else None,
        "output": output_path
    }


# ----------------------------
# FORENSIC EXTRACTION
# ----------------------------

def extract_suspicious_data(file_path, output_dir):
    cmd = ["binwalk", "-e", file_path]

    result = subprocess.run(cmd, capture_output=True, text=True)

    return {
        "success": True,
        "output": result.stdout,
        "error": result.stderr
    }