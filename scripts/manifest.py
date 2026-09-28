#!/usr/bin/env python3
"""Write logo/MANIFEST.sha256: the hash of every shipped brand file.

Surfaces pin these files by hash, so a changed file is a visible diff.

  python3 scripts/manifest.py          # write
  python3 scripts/manifest.py --check  # fail if stale
"""

import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "logo/MANIFEST.sha256"
DIRS = ["logo/svg", "logo/png", "logo/favicon", "logo/app-icon", "logo/sheet", "logo/construction", "tokens"]


def render() -> str:
    lines = []
    for d in DIRS:
        for f in sorted((ROOT / d).rglob("*")):
            if f.is_file() and f != OUT and "__pycache__" not in f.parts:
                lines.append(f"{hashlib.sha256(f.read_bytes()).hexdigest()}  {f.relative_to(ROOT)}")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    text = render()
    if "--check" in sys.argv:
        if OUT.read_text() != text:
            sys.exit("logo/MANIFEST.sha256 is stale: run python3 scripts/manifest.py")
    else:
        OUT.write_text(text)
