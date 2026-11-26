"""Entry point for the world-news front-page image.

Copies the bundled entry.png next to this script into /output/entry.png
and checks the copy is byte-for-byte identical by comparing SHA-256
hashes of the source and the output.
"""

import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
OUTPUT_DIR = "/output"
OUTPUT = os.path.join(OUTPUT_DIR, "entry.png")


def sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(SOURCE, "rb") as src:
        data = src.read()
    with open(OUTPUT, "wb") as dst:
        dst.write(data)
    if sha256(SOURCE) != sha256(OUTPUT):
        print("error: output does not match source", file=sys.stderr)
        return 1
    print(f"wrote {OUTPUT} ({len(data)} bytes)")
    print("success: output matches source byte-for-byte")
    return 0


if __name__ == "__main__":
    sys.exit(main())
