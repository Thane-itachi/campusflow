"""Ticket creation and validation for CampusFlow."""

VALID_PRIORITIES = {"low", "medium", "high", "critical"}


def create_ticket(tickets, title, description, priority="medium"):
    """Create a ticket and append it to the supplied ticket list."""

    if not isinstance(title, str) or not title.strip():
        raise ValueError("Ticket title cannot be empty.")

    if not isinstance(description, str) or not description.strip():
        raise ValueError("Ticket description cannot be empty.")

    if not isinstance(priority, str):
        raise ValueError("Priority must be a string.")

    priority = priority.strip().lower()

    if priority not in VALID_PRIORITIES:
        raise ValueError(f"Invalid priority: {priority}")

    # Generate the next sequential ticket ID.
    existing_numbers = []

    for ticket in tickets:
        ticket_id = ticket.get("id", "")

        if isinstance(ticket_id, str) and ticket_id.startswith("T"):
            try:
                existing_numbers.append(int(ticket_id[1:]))
            except ValueError:
                continue

    next_number = max(existing_numbers, default=0) + 1
    ticket_id = f"T{next_number:03d}"

    ticket = {
        "id": ticket_id,
        "title": title.strip(),
        "description": description.strip(),
        "priority": priority,
        "status": "open",
        "assigned_to": None,
    }

    tickets.append(ticket)
    return ticket
