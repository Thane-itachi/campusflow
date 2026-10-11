"""JSON persistence — the only module that touches the tickets file.

Owner: Engineer A.

Contract:
- Missing or empty file -> [].
- Malformed JSON or invalid ticket data -> StorageError.
- Loading never modifies the file.
- Saving uses an atomic temporary-file replacement.
- Both functions accept an optional path for testability.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

DEFAULT_PATH = Path("data") / "tickets.json"
DEFAULT_STORAGE_PATH = DEFAULT_PATH


class StorageError(ValueError):
    """Raised when ticket storage cannot be read or validated."""


def load_tickets(path: Path | str = DEFAULT_PATH) -> list[dict]:
    """Load and validate tickets without modifying the stored file."""
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
            "The file was not modified."
        ) from exc

    if not isinstance(data, list):
        raise StorageError(f"{p} must contain a JSON list of tickets.")

    if not all(isinstance(ticket, dict) for ticket in data):
        raise StorageError("Every stored ticket must be a JSON object.")

    return data


def save_tickets(
    tickets: list[dict],
    path: Path | str = DEFAULT_PATH,
) -> None:
    """Atomically save tickets as formatted JSON."""
    p = Path(path)
    tmp = p.with_suffix(p.suffix + ".tmp")

    try:
        p.parent.mkdir(parents=True, exist_ok=True)
        tmp.write_text(
            json.dumps(tickets, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        os.replace(tmp, p)
    except (OSError, TypeError, ValueError) as exc:
        raise StorageError(f"Could not save tickets to {p}: {exc}") from exc
    finally:
        try:
            tmp.unlink(missing_ok=True)
        except OSError:
            pass
