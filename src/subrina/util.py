from io import TextIOWrapper, StringIO
from pathlib import Path
from os.path import isfile


def try_int(value: str) -> int | None:
    """Tries to convert a string to an int, returns None if it fails"""
    try:
        return int(value)
    except ValueError:
        return None


def get_stream_from_argument(file: str | Path | TextIOWrapper, encoding="utf-8"):
    if isinstance(file, TextIOWrapper):
        return file
    elif isinstance(file, str):
        if isfile(file):
            return open(file, "r", encoding=encoding)
        else:
            return StringIO(file)
    elif isinstance(file, Path):
        return open(file, "r", encoding=encoding)

    return None
