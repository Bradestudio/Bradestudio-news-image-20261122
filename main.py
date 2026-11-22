#!/usr/bin/env python3
"""Entrypoint for the make.fun news-image-20261121 entry.

The picture itself is drawn by gen_image.py and shipped in this
repository as entry.png. This program only places that file where
the grader asks for it: MAKEFUN_OUTPUT_DIR, or the first argument,
or ./output. Stdlib only, no network, no clock -- every run writes
the exact same bytes.
"""
import os
import shutil
import sys
from pathlib import Path


def main():
    dest = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not dest and len(sys.argv) > 1:
        dest = sys.argv[1]
    if not dest:
        dest = "output"
    outdir = Path(dest)
    outdir.mkdir(parents=True, exist_ok=True)
    here = Path(__file__).resolve().parent
    source = here / "entry.png"
    if not source.is_file():
        raise SystemExit(f"entry.png is missing next to {__file__}")
    target = outdir / "entry.png"
    shutil.copyfile(source, target)
    if target.stat().st_size != source.stat().st_size:
        raise SystemExit("copied entry.png has the wrong size")
    print(f"wrote {target} ({target.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
