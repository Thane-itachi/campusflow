"""Tests for campusflow.storage — Engineer A."""
import json
import tempfile
import unittest
from pathlib import Path

from campusflow import storage
from campusflow.tickets import create_ticket, next_ticket_id


class StorageTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "tickets.json"

    def tearDown(self):
        self.tmp.cleanup()

    # ----------------------------------------------------------- load
    def test_missing_file_returns_empty_list(self):
        self.assertEqual(storage.load_tickets(self.path), [])

    def test_empty_file_returns_empty_list(self):
        self.path.write_text("", encoding="utf-8")
        self.assertEqual(storage.load_tickets(self.path), [])

    def test_malformed_json_raises_storage_error(self):
        self.path.write_text("{ not json", encoding="utf-8")
        with self.assertRaises(storage.StorageError):
            storage.load_tickets(self.path)

    def test_malformed_json_is_not_overwritten(self):
        original = "{ not json"
        self.path.write_text(original, encoding="utf-8")
        with self.assertRaises(storage.StorageError):
            storage.load_tickets(self.path)
        self.assertEqual(self.path.read_text(encoding="utf-8"), original)

    def test_wrong_top_level_type_raises(self):
        self.path.write_text(json.dumps({"a": 1}), encoding="utf-8")
        with self.assertRaises(storage.StorageError):
            storage.load_tickets(self.path)

    # ----------------------------------------------------------- save
    def test_save_creates_parent_dirs(self):
        nested = Path(self.tmp.name) / "deep" / "nested" / "tickets.json"
        storage.save_tickets([], nested)
        self.assertTrue(nested.exists())

    # ----------------------------------------------------------- round-trip
    def test_round_trip_preserves_tickets(self):
        tickets = []
        create_ticket(tickets, title="wifi", category="Network",
                      urgency="high", affected_users=20)
        create_ticket(tickets, title="laptop", category="Hardware",
                      urgency="medium", affected_users=2)

        storage.save_tickets(tickets, self.path)
        reloaded = storage.load_tickets(self.path)

        self.assertEqual(reloaded, tickets)
        # IDs keep counting after reload.
        self.assertEqual(next_ticket_id(reloaded), "T003")

    def test_round_trip_empty(self):
        storage.save_tickets([], self.path)
        self.assertEqual(storage.load_tickets(self.path), [])

    def test_save_is_atomic_no_tmp_file_left_behind(self):
        tickets = []
        create_ticket(tickets, title="x", category="Other",
                      urgency="low", affected_users=1)
        storage.save_tickets(tickets, self.path)
        # Nothing left over.
        leftovers = list(self.path.parent.glob("*.tmp"))
        self.assertEqual(leftovers, [])


if __name__ == "__main__":
    unittest.main()