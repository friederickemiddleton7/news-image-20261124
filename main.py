#!/usr/bin/env python3
"""Entrypoint for the news-image-20261124 entry.

The grader runs this in a fresh container with no network. It copies the
pre-rendered front page (entry.png, drawn by make_image.py at build time)
into the output directory. Standard library only, fully deterministic.
"""
import os
import shutil
import struct
import sys

REQUIRED_MIN_BYTES = 1024  # a real front page is never tiny

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"  # every genuine PNG file starts with these 8 bytes
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024


def png_dimensions(path):
    """Return (width, height) if path is a genuine PNG, else None.

    Reads the 8-byte PNG signature and the width/height fields of the mandatory
    IHDR chunk (always the first chunk, 13 data bytes). Standard library only.
    """
    try:
        with open(path, "rb") as fh:
            if fh.read(8) != PNG_SIGNATURE:
                return None
            chunk = fh.read(8)
            if len(chunk) < 8:
                return None
            length, ctype = struct.unpack(">I4s", chunk)
            if ctype != b"IHDR" or length != 13:
                return None
            data = fh.read(13)
            if len(data) < 13:
                return None
            width, height = struct.unpack(">II", data[:8])
            return width, height
    except OSError:
        return None


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")

    if not os.path.isfile(src):
        print("error: entry.png is missing next to main.py; run make_image.py first", file=sys.stderr)
        return 1

    dims = png_dimensions(src)
    if dims is None:
        print("error: entry.png is not a valid PNG file", file=sys.stderr)
        return 1
    width, height = dims
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        print(f"error: entry.png is {width}x{height}; expected exactly {EXPECTED_WIDTH}x{EXPECTED_HEIGHT}",
              file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    try:
        os.makedirs(out_dir, exist_ok=True)
    except OSError as exc:
        print(f"error: cannot create output directory {out_dir}: {exc}", file=sys.stderr)
        return 1

    dst = os.path.join(out_dir, "entry.png")
    try:
        shutil.copyfile(src, dst)
    except OSError as exc:
        print(f"error: cannot copy entry.png to {dst}: {exc}", file=sys.stderr)
        return 1

    size = os.path.getsize(dst)
    if size < REQUIRED_MIN_BYTES:
        print(f"error: copied entry.png is only {size} bytes; expected the full front page",
              file=sys.stderr)
        return 1

    print(f"ok: wrote entry.png ({size} bytes) to {dst}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
