"""Write the competition entry to /output/entry.txt.

One line of earned pride, 1 to 240 characters, as UTF-8 text with no
trailing newline.
"""

import os
import sys
import tempfile

ENTRY = "After forty years of night shifts, my father hung his own name above the workshop door and stood there a while, just looking at it."

OUTPUT_PATH = "/output/entry.txt"
MIN_LENGTH = 1
MAX_LENGTH = 240


def validate(text):
    if not isinstance(text, str):
        raise TypeError("entry must be a string")
    if len(text) < MIN_LENGTH or len(text) > MAX_LENGTH:
        raise ValueError(
            "entry must be %d-%d characters, got %d"
            % (MIN_LENGTH, MAX_LENGTH, len(text))
        )
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    return text


def write_entry(path, text):
    data = validate(text).encode("utf-8")
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(
        dir=directory or ".", prefix=".entry-", suffix=".tmp"
    )
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_path, path)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise
    return len(data)


def main():
    try:
        byte_count = write_entry(OUTPUT_PATH, ENTRY)
    except (OSError, ValueError, TypeError) as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 1
    print("wrote %s (%d characters, %d bytes)" % (OUTPUT_PATH, len(ENTRY), byte_count))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
