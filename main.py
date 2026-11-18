"""Entry for news-image-20261118: copy the bundled front page to /output.

The image (entry.png, 1024x1024) was rendered programmatically from real
headlines of Wednesday 18 November 2026. This program only copies bytes:
no network, no randomness, identical output on every run.
"""
import os
import shutil
import sys


def main():
    # Paths resolve relative to this script, never the working directory,
    # so the program works wherever the grader runs it from.
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    return 0


if __name__ == "__main__":
    sys.exit(main())
