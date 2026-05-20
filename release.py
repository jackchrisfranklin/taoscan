import subprocess
import sys
import re
from pathlib import Path
from datetime import datetime
import glob
import os

PROJECT_ROOT = Path(__file__).resolve().parent
PARENT = PROJECT_ROOT.parent
CHANGELOG = PROJECT_ROOT / "debian" / "changelog"


def run(cmd):
    print(f"\n>>> {' '.join(cmd)}\n")
    subprocess.run(cmd, cwd=PROJECT_ROOT, check=True)


def get_current_version():
    text = CHANGELOG.read_text()
    match = re.search(r"\((\d+\.\d+\.\d+)\)", text)
    if not match:
        raise ValueError("No version found in changelog")
    return match.group(1)


def bump_version(v):
    a, b, c = map(int, v.split("."))
    return f"{a}.{b}.{c + 1}"


def write_changelog(version, msg):
    date = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S +0000")

    entry = f"""taoscan ({version}) unstable; urgency=medium

  * {msg}

 -- Taoscan Dev <dev@local>  {date}

"""

    CHANGELOG.write_text(entry + CHANGELOG.read_text())


def git_commit_and_push(version):
    run(["git", "add", "."])
    run(["git", "commit", "-m", f"Release v{version}"])
    run(["git", "push"])


def clean():
    run(["dh_clean"])


def build():
    run(["debuild", "-us", "-uc"])


def find_deb():
    debs = glob.glob(str(PARENT / "taoscan_*.deb"))
    if not debs:
        raise FileNotFoundError("No .deb found")
    return max(debs, key=os.path.getctime)


def git_tag(version):
    run(["git", "tag", f"v{version}"])
    run(["git", "push", "origin", f"v{version}"])


def github_release(version, msg, deb):
    run([
        "gh", "release", "create", f"v{version}",
        deb,
        "--title", f"taoscan v{version}",
        "--notes", msg
    ])


def main():
    print("TAOSCAN RELEASE TOOL")

    current = get_current_version()
    new_version = bump_version(current)

    print(f"Current: {current}")
    print(f"New: {new_version}")

    msg = input("Release message: ").strip()
    if not msg:
        print("No message provided")
        sys.exit(1)

    write_changelog(new_version, msg)

    # 1. commit + push source first
    git_commit_and_push(new_version)

    # 2. build package
    clean()
    build()

    # 3. find deb
    deb = find_deb()
    print(f"Found package: {deb}")

    # 4. tag + release
    git_tag(new_version)
    github_release(new_version, msg, deb)

    print("Release complete")


if __name__ == "__main__":
    main()