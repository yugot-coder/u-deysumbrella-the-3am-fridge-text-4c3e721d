"""The 3AM Fridge Text - writes one funny fridge text to /output/entry.txt."""
import hashlib
import os
import sys

TEXT = "I counted. That's your 4th 'just looking' tonight. We both know how this ends: you, me, and the cake pretending not to notice."


def main() -> int:
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    try:
        os.makedirs(out_dir, exist_ok=True)
        path = os.path.join(out_dir, "entry.txt")
    except OSError:
        path = "/output/entry.txt"
    data = TEXT.encode("utf-8")
    with open(path, "wb") as fh:
        fh.write(data)
    with open(path, "rb") as fh:
        back = fh.read()
    if hashlib.sha256(back).hexdigest() != hashlib.sha256(data).hexdigest():
        raise SystemExit("digest mismatch on read-back")
    if not (1 <= len(TEXT) <= 140) or not TEXT.strip():
        raise SystemExit("gate failed: length")
    return 0


if __name__ == "__main__":
    sys.exit(main())
