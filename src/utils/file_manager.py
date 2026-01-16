from __future__ import annotations

import os
from pathlib import Path
from typing import Union

PathLike = Union[str, os.PathLike]

def read_text(path: PathLike, encoding: str = "utf-8") -> str:
    # Reads a text file and returns its content.
    p = Path(path)
    return p.read_text(encoding=encoding)


def write_text(
    path: PathLike,
    content: str,
    encoding: str = "utf-8",
    ensure_parent: bool = True,
) -> None:
    # Writes content to file (path passed as parameter). If ensure_parent=True creates missing directories
    p = Path(path)
    if ensure_parent:
        p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding=encoding)


def safe_remove(path: PathLike) -> bool:
    # Attempts to delete a file. Returns True if removed, False if not exists or cannot be deleted
    # Useful on Windows where files are sometimes locked
    p = Path(path)
    try:
        p.unlink()
        return True
    except FileNotFoundError or OSError:
        return False


def ensure_dir(path: PathLike) -> str:
    # Creates a directory (if it doesn't exist) and returns the path as a string
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return str(p)


def obtain_import_module_str(file_path: str):
    return "data.input_code."+Path(file_path).stem
