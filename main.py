#!/usr/bin/env python3
"""Run the round-2 front page and write it to the harness output dir.

This entrypoint draws the picture itself (via ``gen_image.render``) and
writes ``entry.png`` where the make.fun harness expects it:

* ``$MAKEFUN_OUTPUT_DIR/entry.png`` when the variable is set, else
* the directory passed as the first command-line argument, else
* ``./output/entry.png``.

Standard library plus Pillow (the same library ``gen_image`` uses).
No network, no clock, no randomness: the same run always writes the
same bytes.
"""

import os
import sys


def _here():
    """Directory holding this file, so the import works from anywhere."""
    return os.path.dirname(os.path.abspath(__file__))


def pick_dir(argv):
    """Choose the output directory, in priority order."""
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        return env_dir
    if len(argv) > 1:
        return argv[1]
    return os.path.join(os.getcwd(), "output")


def main(argv):
    """Draw the front page into the chosen output directory."""
    sys.path.insert(0, _here())
    import gen_image

    out_dir = pick_dir(argv)
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    gen_image.render(target)
    print("wrote", target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
