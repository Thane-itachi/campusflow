"""Tests for campusflow.tickets — Engineer A."""
import unittest

from campusflow.tickets import (
    ValidationError,
    assign_ticket,
    compute_priority,
    create_ticket,
    find_ticket,
    next_ticket_id,
    normalize_category,
    normalize_urgency,
    validate_affected_users,
    validate_title,
)


class PriorityEngineTests(unittest.TestCase):
    def test_rule_1_critical(self):
        self.assertEqual(compute_priority("high", 10), "critical")
        self.assertEqual(compute_priority("high", 50), "critical")

    def test_rule_2_high(self):
        self.assertEqual(compute_priority("high", 9), "high")
        self.assertEqual(compute_priority("low", 10), "high")
        self.assertEqual(compute_priority("medium", 15), "high")

    def test_rule_3_medium(self):
        self.assertEqual(compute_priority("medium", 1), "medium")
        self.assertEqual(compute_priority("low", 3), "medium")

    def test_rule_4_low(self):
        self.assertEqual(compute_priority("low", 1), "low")
        self.assertEqual(compute_priority("low", 2), "low")

    def test_boundaries(self):
        # Exactly at the cutoff, in the right direction.
        self.assertEqual(compute_priority("high", 10), "critical")
        self.assertEqual(compute_priority("high", 9), "high")
        self.assertEqual(compute_priority("low", 10), "high")
        self.assertEqual(compute_priority("low", 9), "medium")
        self.assertEqual(compute_priority("low", 3), "medium")
        self.assertEqual(compute_priority("low", 2), "low")


class ValidationTests(unittest.TestCase):
    def test_title_blank_rejected(self):
        for bad in ("", "   ", "\t\n"):
            with self.subTest(bad=bad), self.assertRaises(ValidationError):
                validate_title(bad)

    def test_title_stripped(self):
        self.assertEqual(validate_title("  Wi-Fi down  "), "Wi-Fi down")

    def test_affected_users_rejects_bad_input(self):
        for bad in (0, -1, -100, True, False, 1.5, "5", None):
            with self.subTest(bad=bad), self.assertRaises(ValidationError):
                validate_affected_users(bad)

    def test_affected_users_accepts_positive_int(self):
        self.assertEqual(validate_affected_users(1), 1)
        self.assertEqual(validate_affected_users(999), 999)

    def test_category_normalized(self):
        self.assertEqual(normalize_category("network"), "Network")
        self.assertEqual(normalize_category("HARDWARE"), "Hardware")
        self.assertEqual(normalize_category("  software  "), "Software")

    def test_category_rejects_unknown(self):
        with self.assertRaises(ValidationError):
            normalize_category("Printer")

    def test_urgency_normalized(self):
        self.assertEqual(normalize_urgency("HIGH"), "high")
        self.assertEqual(normalize_urgency("Medium"), "medium")

    def test_urgency_rejects_unknown(self):
        with self.assertRaises(ValidationError):
            normalize_urgency("urgent")


class CreateTicketTests(unittest.TestCase):
    def test_create_sets_defaults_and_priority(self):
        tickets = []
        t = create_ticket(tickets, title="Wi-Fi down", category="network",
                          urgency="HIGH", affected_users=15)
        self.assertEqual(t["id"], "T001")
        self.assertEqual(t["title"], "Wi-Fi down")
        self.assertEqual(t["category"], "Network")
        self.assertEqual(t["urgency"], "high")
        self.assertEqual(t["priority"], "critical")
        self.assertEqual(t["status"], "open")
        self.assertIsNone(t["assigned_to"])
        self.assertEqual(len(tickets), 1)

    def test_create_failure_leaves_list_untouched(self):
        tickets = []
        with self.assertRaises(ValidationError):
            create_ticket(tickets, title="   ", category="Network",
                          urgency="low", affected_users=1)
        self.assertEqual(tickets, [])

    def test_ids_increment_and_stay_unique_after_reload(self):
        tickets = []
        create_ticket(tickets, title="a", category="Network",
                      urgency="low", affected_users=1)
        create_ticket(tickets, title="b", category="Network",
                      urgency="low", affected_users=1)
        self.assertEqual([t["id"] for t in tickets], ["T001", "T002"])

        # Simulate a "reload": same data, ask for the next id.
        self.assertEqual(next_ticket_id(tickets), "T003")

        # T010 boundary — numeric, not lexicographic.
        padded = [{"id": f"T{i:03d}"} for i in range(1, 12)]
        self.assertEqual(next_ticket_id(padded), "T012")

    def test_next_ticket_id_ignores_garbage_ids(self):
        weird = [{"id": "T001"}, {"id": "nope"}, {"id": None}, {}]
        self.assertEqual(next_ticket_id(weird), "T002")


class FindAndAssignTests(unittest.TestCase):
    def _one(self):
        tickets = []
        create_ticket(tickets, title="wifi", category="Network",
                      urgency="high", affected_users=12)
        return tickets

    def test_find_ticket_case_insensitive(self):
        tickets = self._one()
        self.assertIs(find_ticket(tickets, "t001"), tickets[0])
        self.assertIs(find_ticket(tickets, "T001"), tickets[0])
        self.assertIsNone(find_ticket(tickets, "T999"))
        self.assertIsNone(find_ticket(tickets, ""))

    def test_assign_sets_staff_and_returns_same_object(self):
        tickets = self._one()
        t = assign_ticket(tickets, "T001", "  Sam  ")
        self.assertEqual(t["assigned_to"], "Sam")
        self.assertIs(t, tickets[0])

    def test_assign_rejects_unknown_id(self):
        tickets = self._one()
        with self.assertRaises(ValidationError):
            assign_ticket(tickets, "T999", "Sam")

    def test_assign_rejects_blank_staff(self):
        tickets = self._one()
        for bad in ("", "   ", None, 42):
            with self.subTest(bad=bad), self.assertRaises(ValidationError):
                assign_ticket(tickets, "T001", bad)
        # Nothing was mutated.
        self.assertIsNone(tickets[0]["assigned_to"])


if __name__ == "__main__":
    unittest.main()