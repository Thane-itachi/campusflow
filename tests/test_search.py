import unittest

from campusflow.search import search_tickets, filter_tickets


def make_ticket(
    ticket_id="T001",
    title="Campus Wi-Fi is down",
    category="Network",
    status="open",
    priority="critical",
):
    """Create a sample ticket for testing."""
    return {
        "id": ticket_id,
        "title": title,
        "category": category,
        "status": status,
        "priority": priority,
    }


class TestTicketSearch(unittest.TestCase):

    def setUp(self):
        """Prepare sample tickets for each test."""
        self.tickets = [
            make_ticket(
                "T001",
                "Campus Wi-Fi is down",
                "Network",
                "open",
                "critical",
            ),
            make_ticket(
                "T002",
                "Printer problem",
                "Hardware",
                "open",
                "medium",
            ),
            make_ticket(
                "T003",
                "Wi-Fi login issue",
                "Network",
                "resolved",
                "high",
            ),
            make_ticket(
                "T004",
                "Software installation failure",
                "Software",
                "in_progress",
                "medium",
            ),
        ]

    def test_search_is_case_insensitive(self):
        result = search_tickets(self.tickets, "CAMPUS WI-FI")

        self.assertEqual(
            [ticket["id"] for ticket in result],
            ["T001"],
        )

    def test_search_finds_partial_title(self):
        result = search_tickets(self.tickets, "Printer")

        self.assertEqual(
            [ticket["id"] for ticket in result],
            ["T002"],
        )

    def test_search_returns_multiple_matches(self):
        result = search_tickets(self.tickets, "Wi-Fi")

        self.assertEqual(
            [ticket["id"] for ticket in result],
            ["T001", "T003"],
        )

    def test_search_returns_empty_list_when_no_match(self):
        result = search_tickets(self.tickets, "Electricity")

        self.assertEqual(result, [])

    def test_empty_search_returns_all_tickets(self):
        result = search_tickets(self.tickets, "")

        self.assertEqual(result, self.tickets)

    def test_search_rejects_non_string_input(self):
        with self.assertRaises(ValueError):
            search_tickets(self.tickets, 123)

    def test_filter_by_category(self):
        result = filter_tickets(
            self.tickets,
            category="Network",
        )

        self.assertEqual(
            [ticket["id"] for ticket in result],
            ["T001", "T003"],
        )

    def test_filter_by_status(self):
        result = filter_tickets(
            self.tickets,
            status="open",
        )

        self.assertEqual(
            [ticket["id"] for ticket in result],
            ["T001", "T002"],
        )

    def test_filter_by_priority(self):
        result = filter_tickets(
            self.tickets,
            priority="medium",
        )

        self.assertEqual(
            [ticket["id"] for ticket in result],
            ["T002", "T004"],
        )

    def test_combined_filters_use_and_logic(self):
        result = filter_tickets(
            self.tickets,
            category="Network",
            status="open",
            priority="critical",
        )

        self.assertEqual(
            [ticket["id"] for ticket in result],
            ["T001"],
        )

    def test_combined_filters_return_empty_list_when_no_match(self):
        result = filter_tickets(
            self.tickets,
            category="Hardware",
            status="resolved",
            priority="critical",
        )

        self.assertEqual(result, [])

    def test_filter_without_options_returns_all_tickets(self):
        result = filter_tickets(self.tickets)

        self.assertEqual(result, self.tickets)


if __name__ == "__main__":
    unittest.main()
    