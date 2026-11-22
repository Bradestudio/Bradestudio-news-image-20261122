#!/usr/bin/env python3
"""Ship the pre-rendered front page as this entry's output.

The picture itself lives in ``entry.png`` next to this file (drawn by
``gen_image.py`` with Pillow only). This script just copies that file to
the place the make.fun harness expects it:

* ``$MAKEFUN_OUTPUT_DIR/entry.png`` when the variable is set, else
* the directory given as the first command-line argument, else
* ``./output/entry.png``.

Standard library only. No network, no clock, no randomness — the same
input always produces the same bytes.
"""

import os
import shutil
import sys


def pick_output_dir(argv):
    """Decide where the finished image goes, in priority order."""
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        return env_dir
    if len(argv) > 1:
        return argv[1]
    return os.path.join(os.getcwd(), "output")


def main(argv):
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    if not os.path.isfile(source):
        raise SystemExit("entry.png is missing next to main.py — "
                         "run gen_image.py first")
    dest_dir = pick_output_dir(argv)
    os.makedirs(dest_dir, exist_ok=True)
    dest = os.path.join(dest_dir, "entry.png")
    shutil.copyfile(source, dest)
    size = os.path.getsize(dest)
    print("copied entry.png to %s (%d bytes)" % (dest, size))


if __name__ == "__main__":
    main(sys.argv)
