import unittest

from campusflow.reports import generate_ticket_report


def make_ticket(
    ticket_id,
    priority="medium",
    status="open",
    assigned_to=None,
    category="Network",
):
    """Create a sample ticket for testing."""
    return {
        "id": ticket_id,
        "title": "Test ticket",
        "priority": priority,
        "status": status,
        "assigned_to": assigned_to,
        "category": category,
    }


class TestTicketReport(unittest.TestCase):

    def test_counts_total_tickets(self):
        tickets = [
            make_ticket("T001"),
            make_ticket("T002"),
            make_ticket("T003"),
        ]

        report = generate_ticket_report(tickets)

        self.assertEqual(report["total"], 3)

    def test_counts_statuses(self):
        tickets = [
            make_ticket("T001", status="open"),
            make_ticket("T002", status="open"),
            make_ticket("T003", status="in_progress"),
            make_ticket("T004", status="resolved"),
        ]

        report = generate_ticket_report(tickets)

        self.assertEqual(report["open"], 2)
        self.assertEqual(report["in_progress"], 1)
        self.assertEqual(report["resolved"], 1)

    def test_counts_priorities(self):
        tickets = [
            make_ticket("T001", priority="critical"),
            make_ticket("T002", priority="critical"),
            make_ticket("T003", priority="high"),
            make_ticket("T004", priority="low"),
        ]

        report = generate_ticket_report(tickets)

        self.assertEqual(
            report["by_priority"],
            {"critical": 2, "high": 1, "low": 1},
        )

    def test_counts_categories(self):
        tickets = [
            make_ticket("T001", category="Network"),
            make_ticket("T002", category="Network"),
            make_ticket("T003", category="Hardware"),
        ]

        report = generate_ticket_report(tickets)

        self.assertEqual(
            report["by_category"],
            {"Network": 2, "Hardware": 1},
        )

    def test_counts_assignees(self):
        tickets = [
            make_ticket("T001", assigned_to="John"),
            make_ticket("T002", assigned_to="John"),
            make_ticket("T003", assigned_to="Mary"),
            make_ticket("T004", assigned_to=None),
        ]

        report = generate_ticket_report(tickets)

        self.assertEqual(
            report["by_assignee"],
            {"John": 2, "Mary": 1, "Unassigned": 1},
        )

    def test_counts_unresolved_tickets(self):
        tickets = [
            make_ticket("T001", status="open"),
            make_ticket("T002", status="in_progress"),
            make_ticket("T003", status="resolved"),
        ]

        report = generate_ticket_report(tickets)

        self.assertEqual(report["unresolved"], 2)

    def test_calculates_resolution_percentage(self):
        tickets = [
            make_ticket("T001", status="resolved"),
            make_ticket("T002", status="resolved"),
            make_ticket("T003", status="open"),
            make_ticket("T004", status="in_progress"),
        ]

        report = generate_ticket_report(tickets)

        self.assertEqual(report["resolution_percentage"], 50.0)

    def test_empty_list_returns_zero_percentage(self):
        report = generate_ticket_report([])

        self.assertEqual(report["total"], 0)
        self.assertEqual(report["unresolved"], 0)
        self.assertEqual(report["resolution_percentage"], 0.0)
        self.assertEqual(report["by_category"], {})

    def test_does_not_modify_tickets(self):
        tickets = [
            make_ticket("T001", priority="critical", assigned_to="John"),
            make_ticket("T002", priority="low"),
        ]

        original_tickets = [ticket.copy() for ticket in tickets]

        generate_ticket_report(tickets)

        self.assertEqual(tickets, original_tickets)


if __name__ == "__main__":
    unittest.main()
    