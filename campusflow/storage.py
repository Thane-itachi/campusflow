"""JSON persistence — the only module that touches the tickets file.

Owner: Engineer A.

Contract:
- load_tickets: missing file -> []. Malformed -> StorageError. Never writes.
- save_tickets: atomic write via tmp file + os.replace.
- Both functions accept an optional path for testability.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

DEFAULT_PATH = Path("data") / "tickets.json"


class StorageError(RuntimeError):
    """Raised for unrecoverable storage problems."""


def load_tickets(path: Path | str = DEFAULT_PATH) -> list[dict]:
    """Return tickets from disk. Missing file -> empty list.

    Malformed JSON or wrong top-level type -> StorageError, and the file
    is left untouched (we never write from here).
    """
    p = Path(path)
    if not p.exists():
        return []

    try:
        raw = p.read_text(encoding="utf-8")
    except OSError as exc:
        raise StorageError(f"Could not read {p}: {exc}") from exc

    if not raw.strip():
        return []

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise StorageError(
            f"{p} contains invalid JSON "
            f"({exc.msg} at line {exc.lineno}). "
            "Refusing to overwrite; fix or move the file."
        ) from exc

    if not isinstance(data, list):
        raise StorageError(f"{p} must contain a JSON list of tickets.")

    return data


def save_tickets(tickets: list[dict], path: Path | str = DEFAULT_PATH) -> None:
    """Atomically write tickets to disk as pretty JSON."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    try:
        tmp.write_text(json.dumps(tickets, indent=2), encoding="utf-8")
        os.replace(tmp, p)   # atomic on POSIX and Windows
    except OSError as exc:
        raise StorageError(f"Could not write {p}: {exc}") from exc