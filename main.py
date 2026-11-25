"""The 3AM Fridge Text - writes one funny fridge text to /output/entry.txt.

The text is validated against the gate before writing, and the written
bytes are read back and verified (byte length and sha256 digest) so a
bad write fails loudly instead of shipping a broken entry. Standard
library only, deterministic: the file contains exactly TEXT, no
trailing newline.
"""
import hashlib
import os
import sys

TEXT = "I counted. That's your 4th 'just looking' tonight. We both know how this ends: you, me, and the cake pretending not to notice."

MIN_CHARS = 1
MAX_CHARS = 140


def validate_entry(text: str) -> None:
    """Check the text against the competition gate."""
    if not (MIN_CHARS <= len(text) <= MAX_CHARS) or not text.strip():
        raise SystemExit("gate failed: length")
    if text != text.strip() or "\n" in text or "\r" in text:
        raise SystemExit("gate failed: must be one line, no edge whitespace")


def verify_written_bytes(written: bytes) -> str:
    """Verify the exact bytes read back from entry.txt; return the digest."""
    intended = TEXT.encode("utf-8")
    if len(written) != len(intended):
        raise SystemExit("byte length mismatch on read-back")
    if written != intended:
        raise SystemExit("content mismatch on read-back")
    digest = hashlib.sha256(written).hexdigest()
    if digest != hashlib.sha256(intended).hexdigest():
        raise SystemExit("digest mismatch on read-back")
    return digest


def main() -> int:
    validate_entry(TEXT)
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
    verify_written_bytes(back)
    return 0


if __name__ == "__main__":
    sys.exit(main())
