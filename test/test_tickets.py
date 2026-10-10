import unittest

from campusflow.tickets import create_ticket


class TestTicketCreation(unittest.TestCase):

    def setUp(self):
        self.tickets = []

    def test_create_ticket_with_defaults(self):
        ticket = create_ticket(
            self.tickets,
            "Broken projector",
            "Projector in Room 2 is not working."
        )

        self.assertEqual(ticket["id"], "T001")
        self.assertEqual(ticket["title"], "Broken projector")
        self.assertEqual(ticket["priority"], "medium")
        self.assertEqual(ticket["status"], "open")
        self.assertIsNone(ticket["assigned_to"])
        self.assertEqual(len(self.tickets), 1)

    def test_priority_is_normalized(self):
        ticket = create_ticket(
            self.tickets, "Network issue", "Wi-Fi is down.", " HIGH "
        )
        self.assertEqual(ticket["priority"], "high")

    def test_ticket_ids_increment(self):
        first = create_ticket(self.tickets, "First", "First issue")
        second = create_ticket(self.tickets, "Second", "Second issue")

        self.assertEqual(first["id"], "T001")
        self.assertEqual(second["id"], "T002")

    def test_blank_title_is_rejected(self):
        with self.assertRaises(ValueError):
            create_ticket(self.tickets, "  ", "Description")

    def test_blank_description_is_rejected(self):
        with self.assertRaises(ValueError):
            create_ticket(self.tickets, "Title", "  ")

    def test_invalid_priority_is_rejected(self):
        with self.assertRaises(ValueError):
            create_ticket(
                self.tickets, "Title", "Description", "urgent"
            )

    def test_non_string_priority_is_rejected(self):
        with self.assertRaises(ValueError):
            create_ticket(
                self.tickets, "Title", "Description", None
            )


if __name__ == "__main__":
    unittest.main()
