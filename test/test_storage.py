import json
import tempfile
import unittest
from pathlib import Path

from campusflow.storage import load_tickets, save_tickets


class TestTicketStorage(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.path = Path(self.temp_dir.name) / "data" / "tickets.json"

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_missing_file_returns_empty_list(self):
        self.assertEqual(load_tickets(self.path), [])

    def test_save_and_load_tickets(self):
        tickets = [
            {
                "id": "T001",
                "title": "Broken projector",
                "description": "Room 2 projector is not working.",
                "priority": "high",
                "status": "open",
                "assigned_to": None,
            }
        ]

        save_tickets(tickets, self.path)
        self.assertEqual(load_tickets(self.path), tickets)

    def test_invalid_json_is_rejected(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text("{invalid json", encoding="utf-8")

        with self.assertRaises(ValueError):
            load_tickets(self.path)

    def test_non_list_json_is_rejected(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text('{"id": "T001"}', encoding="utf-8")

        with self.assertRaises(ValueError):
            load_tickets(self.path)

    def test_non_object_ticket_is_rejected(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps([{"id": "T001"}, "invalid ticket"]),
            encoding="utf-8",
        )

        with self.assertRaises(ValueError):
            load_tickets(self.path)


if __name__ == "__main__":
    unittest.main()
