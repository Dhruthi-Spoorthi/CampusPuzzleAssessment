import os
import sys
import unittest


# Add the src folder to Python's module search path
SRC_DIR = os.path.dirname(os.path.abspath(__file__))

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)


from models import Class, Room
from greedy_solver import GreedySolver


class TestGreedySolver(unittest.TestCase):

    def test_class_too_large_for_every_room(self):
        classes = [
            Class("BIG101", 100, "P1")
        ]

        rooms = [
            Room("R101", 50),
            Room("R102", 40)
        ]

        solver = GreedySolver(
            classes,
            rooms,
            {}
        )

        schedule, unscheduled = solver.solve()

        self.assertEqual(len(schedule), 0)
        self.assertEqual(len(unscheduled), 1)
        self.assertEqual(
            unscheduled[0].class_id,
            "BIG101"
        )

    def test_same_professor_cannot_teach_two_classes_at_same_time(self):
        classes = [
            Class("CS101", 40, "P1"),
            Class("CS102", 30, "P1")
        ]

        rooms = [
            Room("R101", 50),
            Room("R102", 40)
        ]

        solver = GreedySolver(
            classes,
            rooms,
            {}
        )

        schedule, unscheduled = solver.solve()

        self.assertEqual(len(schedule), 2)

        first_entry = schedule[0]
        second_entry = schedule[1]

        self.assertNotEqual(
            first_entry.time_slot,
            second_entry.time_slot
        )

    def test_same_student_group_cannot_have_two_classes_at_same_time(self):
        classes = [
            Class("CS101", 40, "P1"),
            Class("MATH101", 35, "P2")
        ]

        rooms = [
            Room("R101", 50),
            Room("R102", 40)
        ]

        student_groups = {
            "GroupA": [
                "CS101",
                "MATH101"
            ]
        }

        solver = GreedySolver(
            classes,
            rooms,
            student_groups
        )

        schedule, unscheduled = solver.solve()

        self.assertEqual(len(schedule), 2)

        first_entry = schedule[0]
        second_entry = schedule[1]

        self.assertNotEqual(
            first_entry.time_slot,
            second_entry.time_slot
        )

    def test_no_rooms_available(self):
        classes = [
            Class("CS101", 40, "P1"),
            Class("MATH101", 35, "P2")
        ]

        rooms = []

        solver = GreedySolver(
            classes,
            rooms,
            {}
        )

        schedule, unscheduled = solver.solve()

        self.assertEqual(len(schedule), 0)
        self.assertEqual(len(unscheduled), 2)

    def test_no_class_is_scheduled_twice(self):
        classes = [
            Class("CS101", 40, "P1"),
            Class("MATH101", 35, "P2"),
            Class("HIST101", 20, "P3")
        ]

        rooms = [
            Room("R101", 50),
            Room("R102", 40)
        ]

        solver = GreedySolver(
            classes,
            rooms,
            {}
        )

        schedule, unscheduled = solver.solve()

        scheduled_ids = [
            entry.class_id
            for entry in schedule
        ]

        self.assertEqual(
            len(scheduled_ids),
            len(set(scheduled_ids))
        )


if __name__ == "__main__":
    unittest.main()