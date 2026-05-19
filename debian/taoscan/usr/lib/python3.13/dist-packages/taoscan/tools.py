import subprocess
import json

def run_ffprobe(file):
    cmd = [
        "ffprobe",
        "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        "-show_streams",
        file
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    try:
        return json.loads(result.stdout)
    except:
        return {
            "error": "ffprobe_failed",
            "raw": result.stdout,
            "stderr": result.stderr
        }


def run_binwalk(file):
    result = subprocess.run(["binwalk", file], capture_output=True, text=True)

    return {
        "output": result.stdout,
        "stderr": result.stderr,
        "returncode": result.returncode
    }