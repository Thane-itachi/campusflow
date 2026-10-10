"""Reporting functions for CampusFlow."""

from collections import Counter


VALID_STATUSES = {"open", "in_progress", "resolved"}
VALID_PRIORITIES = {"low", "medium", "high", "critical"}


def generate_report(tickets):
    """Generate a summary of ticket counts by status and priority."""
    status_counts = Counter()
    priority_counts = Counter()

    for ticket in tickets:
        status = ticket.get("status", "open")
        priority = str(ticket.get("priority", "medium")).lower()

        if status not in VALID_STATUSES:
            raise ValueError(f"Unknown ticket status: {status}")

        if priority not in VALID_PRIORITIES:
            raise ValueError(f"Unknown ticket priority: {priority}")

        status_counts[status] += 1
        priority_counts[priority] += 1

    return {
        "total_tickets": len(tickets),
        "by_status": {
            status: status_counts[status]
            for status in ("open", "in_progress", "resolved")
        },
        "by_priority": {
            priority: priority_counts[priority]
            for priority in ("critical", "high", "medium", "low")
        },
    }


def print_report(tickets, file=None):
    """Print a readable ticket report."""
    report = generate_report(tickets)
    print("=== CampusFlow Ticket Report ===", file=file)
    print(f"Total tickets: {report['total_tickets']}", file=file)

    print("\nBy status:", file=file)
    for status, count in report["by_status"].items():
        print(f"  {status}: {count}", file=file)

    print("\nBy priority:", file=file)
    for priority, count in report["by_priority"].items():
        print(f"  {priority}: {count}", file=file)

    return report
