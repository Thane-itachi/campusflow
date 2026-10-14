def search_tickets(tickets, title=""):
    """Search tickets by title, ignoring uppercase and lowercase."""
    if not isinstance(title, str):
        raise ValueError("Search title must be text.")

    search_text = title.strip().casefold()

    if not search_text:
        return list(tickets)

    return [
        ticket
        for ticket in tickets
        if search_text in ticket.get("title", "").casefold()
    ]


def filter_tickets(
    tickets,
    category=None,
    status=None,
    priority=None,
):
    """Filter tickets using category, status, and priority together."""
    filtered = []

    for ticket in tickets:
        if category is not None and ticket.get("category") != category:
            continue

        if status is not None and ticket.get("status") != status:
            continue

        if priority is not None and ticket.get("priority") != priority:
            continue

        filtered.append(ticket)

    return filtered
