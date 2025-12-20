from __future__ import annotations

import os
from pathlib import Path
from typing import Union

PathLike = Union[str, os.PathLike]

def read_text(path: PathLike, encoding: str = "utf-8") -> str:
    # Legge un file di testo e ritorna il contenuto.
    p = Path(path)
    return p.read_text(encoding=encoding)


def write_text(
    path: PathLike,
    content: str,
    encoding: str = "utf-8",
    ensure_parent: bool = True,
) -> None:
    # Scrive contenuto su file (path passato come parametro). Se ensure_parent=True crea le cartelle mancanti
    p = Path(path)
    if ensure_parent:
        p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding=encoding)


def safe_remove(path: PathLike) -> bool:
    # Prova a cancellare un file. Ritorna True se rimosso, False se non esiste o non cancellabile
    # Utile su Windows dove a volte i file restano lockati
    p = Path(path)
    try:
        p.unlink()
        return True
    except FileNotFoundError or OSError:
        return False


def ensure_dir(path: PathLike) -> str:
    # Crea una directory (se non esiste) e ritorna il path come stringa
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return str(p)


def obtain_import_module_str(file_path: str):
    return "data.input_code."+Path(file_path).stem
