#!/usr/bin/env python3
import json
import pathlib
import sys

errs = 0
found = 0
for path in pathlib.Path(".").rglob("*.json"):
    if any(part.startswith(".") for part in path.parts):
        continue
    found += 1
    try:
        json.loads(path.read_text())
        print("ok", path)
    except Exception as exc:  # noqa: BLE001
        print("BAD", path, exc)
        errs += 1
if found == 0:
    print("no json files; structure present")
sys.exit(errs)
