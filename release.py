import subprocess
import sys
import re
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent
CHANGELOG = PROJECT_ROOT / "debian" / "changelog"


def run(cmd):
    print(f"\n>>> {' '.join(cmd)}\n")
    subprocess.run(cmd, cwd=PROJECT_ROOT, check=True)


def get_current_version():
    text = CHANGELOG.read_text()

    match = re.search(r"\((\d+\.\d+\.\d+)\)", text)
    if not match:
        raise ValueError("Could not detect version in changelog")

    return match.group(1)


def bump_version(version):
    major, minor, patch = map(int, version.split("."))
    return f"{major}.{minor}.{patch + 1}"


def write_changelog(new_version, message):
    date = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S +0000")

    entry = f"""taoscan ({new_version}) unstable; urgency=medium

  * {message}

 -- Taoscan Dev <dev@local>  {date}

"""

    old = CHANGELOG.read_text()
    CHANGELOG.write_text(entry + old)


def clean():
    run(["dh_clean"])


def build():
    run(["debuild", "-us", "-uc"])


def main():
    print("TAOSCAN RELEASE TOOL")

    current = get_current_version()
    new_version = bump_version(current)

    print(f"Current version: {current}")
    print(f"New version: {new_version}")

    message = input("Changelog message: ").strip()

    if not message:
        print("No message provided, aborting.")
        sys.exit(1)

    print("\nUpdating changelog...")
    write_changelog(new_version, message)

    print("Cleaning...")
    clean()

    print("Building...")
    build()

    print("\nDone. .deb should be in parent directory.")


if __name__ == "__main__":
    main()