#!/usr/bin/env python3
"""World news of Thursday 26 November 2026, summed up in one image.

The entry image is drawn in advance by draw.py and shipped in this
repository as entry.png (a 1024x1024 newspaper front page). This program
copies it to the grader's output path. Standard library only, no network,
and the same bytes every run.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def main():
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(OUT_DIR, "entry.png")
    os.makedirs(OUT_DIR, exist_ok=True)
    shutil.copyfile(src, dst)
    # The two runs must write the same bytes: confirm the copy is exact.
    with open(src, "rb") as f:
        expected = f.read()
    with open(dst, "rb") as f:
        written = f.read()
    if written != expected:
        raise SystemExit("entry.png copy differs from the shipped image")


if __name__ == "__main__":
    main()
