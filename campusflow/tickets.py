"""Ticket creation, validation, ID generation, and the priority engine.

Owner: Engineer A.

Contract (see docs/design-decisions.md):
- Every invalid input raises ValidationError.
- Functions never print, never call input(), never touch the filesystem.
- create_ticket appends in place and returns the new ticket dict.
- On validation failure, the tickets list is left untouched.
"""
from __future__ import annotations

VALID_CATEGORIES = ("Network", "Hardware", "Software", "Other")
VALID_URGENCIES = ("low", "medium", "high")
VALID_STATUSES = ("open", "in_progress", "resolved")

_CATEGORY_LOOKUP = {c.lower(): c for c in VALID_CATEGORIES}
_URGENCY_LOOKUP = {u.lower(): u for u in VALID_URGENCIES}


class ValidationError(ValueError):
    """Raised when user-supplied ticket data fails validation."""


# ---------------------------------------------------------------- validation

def normalize_category(raw: str) -> str:
    """Return the canonical category name, case-insensitively."""
    if not isinstance(raw, str):
        raise ValidationError("Category must be text.")
    key = raw.strip().lower()
    if key not in _CATEGORY_LOOKUP:
        raise ValidationError(
            f"Unknown category {raw!r}. "
            f"Choose from {', '.join(VALID_CATEGORIES)}."
        )
    return _CATEGORY_LOOKUP[key]


def normalize_urgency(raw: str) -> str:
    """Return the canonical urgency, case-insensitively."""
    if not isinstance(raw, str):
        raise ValidationError("Urgency must be text.")
    key = raw.strip().lower()
    if key not in _URGENCY_LOOKUP:
        raise ValidationError(
            f"Unknown urgency {raw!r}. "
            f"Choose from {', '.join(VALID_URGENCIES)}."
        )
    return _URGENCY_LOOKUP[key]


def validate_title(raw: str) -> str:
    """Reject blank / whitespace-only titles; return stripped title."""
    if not isinstance(raw, str) or not raw.strip():
        raise ValidationError("Title must not be blank.")
    return raw.strip()


def validate_affected_users(raw) -> int:
    """Accept only positive ints. Reject bool, float, str, 0, negatives."""
    if isinstance(raw, bool) or not isinstance(raw, int):
        raise ValidationError("Affected users must be a positive integer.")
    if raw <= 0:
        raise ValidationError("Affected users must be a positive integer.")
    return raw


# ----------------------------------------------------------- priority engine

def compute_priority(urgency: str, affected_users: int) -> str:
    """Pure priority engine. First matching rule wins.

    1. high AND >=10 users   -> critical
    2. high OR  >=10 users   -> high
    3. medium OR >=3 users   -> medium
    4. otherwise             -> low
    """
    if urgency == "high" and affected_users >= 10:
        return "critical"
    if urgency == "high" or affected_users >= 10:
        return "high"
    if urgency == "medium" or affected_users >= 3:
        return "medium"
    return "low"


# ---------------------------------------------------------------- ID / lookup

def next_ticket_id(tickets: list[dict]) -> str:
    """Return the next T### id based on the current max, safe across reloads."""
    highest = 0
    for t in tickets:
        tid = t.get("id", "")
        if isinstance(tid, str) and tid.startswith("T") and tid[1:].isdigit():
            highest = max(highest, int(tid[1:]))
    return f"T{highest + 1:03d}"


def find_ticket(tickets: list[dict], ticket_id: str) -> dict | None:
    """Case-insensitive lookup by id. Returns the dict (same object) or None."""
    tid = (ticket_id or "").strip().upper()
    for t in tickets:
        if t["id"] == tid:
            return t
    return None


# -------------------------------------------------------------- create/assign

def create_ticket(tickets: list[dict], *, title: str, category: str,
                  urgency: str, affected_users) -> dict:
    """Validate inputs, compute priority, append to tickets, return the ticket.

    On any ValidationError the tickets list is unchanged.
    """
    clean_title = validate_title(title)
    clean_category = normalize_category(category)
    clean_urgency = normalize_urgency(urgency)
    clean_users = validate_affected_users(affected_users)

    ticket = {
        "id": next_ticket_id(tickets),
        "title": clean_title,
        "category": clean_category,
        "urgency": clean_urgency,
        "affected_users": clean_users,
        "priority": compute_priority(clean_urgency, clean_users),
        "status": "open",
        "assigned_to": None,
    }
    tickets.append(ticket)
    return ticket


def assign_ticket(tickets: list[dict], ticket_id: str, staff_name: str) -> dict:
    """Assign a ticket to a non-empty staff name. Returns the same dict object."""
    ticket = find_ticket(tickets, ticket_id)
    if ticket is None:
        raise ValidationError(f"No ticket with id {ticket_id!r}.")
    if not isinstance(staff_name, str) or not staff_name.strip():
        raise ValidationError("Staff name must not be blank.")
    ticket["assigned_to"] = staff_name.strip()
    return ticket