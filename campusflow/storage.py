"""JSON persistence for CampusFlow tickets."""

import json
from pathlib import Path


DEFAULT_STORAGE_PATH = Path("data/tickets.json")


def load_tickets(path=DEFAULT_STORAGE_PATH):
    """Load tickets from JSON, returning an empty list if no file exists."""

    path = Path(path)

    if not path.exists():
        return []

    try:
        with path.open("r", encoding="utf-8") as file:
            tickets = json.load(file)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Ticket storage contains invalid JSON: {path}") from exc

    if not isinstance(tickets, list):
        raise ValueError("Ticket storage must contain a JSON list.")

    if not all(isinstance(ticket, dict) for ticket in tickets):
        raise ValueError("Every stored ticket must be a JSON object.")

    return tickets


def save_tickets(tickets, path=DEFAULT_STORAGE_PATH):
    """Persist the supplied ticket list to JSON."""

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    temporary_path = path.with_suffix(path.suffix + ".tmp")

    try:
        with temporary_path.open("w", encoding="utf-8") as file:
            json.dump(tickets, file, indent=2, ensure_ascii=False)
            file.write("\n")

        temporary_path.replace(path)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()
