import os
import sys
import unittest


# Add the src folder to Python's module search path
SRC_DIR = os.path.dirname(os.path.abspath(__file__))

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)


from models import Class, Room
from optimizer import Optimizer


class TestOptimizer(unittest.TestCase):

    def test_optimizer_schedules_all_feasible_classes(self):
        classes = [
            Class("CS101", 40, "P1"),
            Class("MATH101", 35, "P2")
        ]

        rooms = [
            Room("R101", 50),
            Room("R102", 40)
        ]

        time_slots = {
            "CS101": "09:00",
            "MATH101": "09:00"
        }

        optimizer = Optimizer(
            classes,
            rooms,
            time_slots
        )

        schedule = optimizer.optimize()

        self.assertEqual(
            len(schedule),
            2
        )

    def test_optimizer_respects_room_capacity(self):
        classes = [
            Class("CS101", 40, "P1")
        ]

        rooms = [
            Room("R101", 30),
            Room("R102", 50)
        ]

        time_slots = {
            "CS101": "09:00"
        }

        optimizer = Optimizer(
            classes,
            rooms,
            time_slots
        )

        schedule = optimizer.optimize()

        self.assertEqual(
            len(schedule),
            1
        )

        self.assertEqual(
            schedule[0].room_id,
            "R102"
        )

    def test_optimizer_minimizes_wasted_capacity(self):
        classes = [
            Class("CS101", 40, "P1"),
            Class("HIST101", 20, "P2")
        ]

        rooms = [
            Room("R101", 50),
            Room("R102", 40),
            Room("R103", 30),
            Room("R104", 20)
        ]

        time_slots = {
            "CS101": "09:00",
            "HIST101": "09:00"
        }

        optimizer = Optimizer(
            classes,
            rooms,
            time_slots
        )

        schedule = optimizer.optimize()

        total_waste = (
            optimizer.calculate_total_wasted_capacity(
                schedule
            )
        )

        self.assertEqual(
            total_waste,
            0
        )

    def test_room_cannot_be_used_twice_in_same_time_slot(self):
        classes = [
            Class("CS101", 40, "P1"),
            Class("MATH101", 35, "P2")
        ]

        rooms = [
            Room("R101", 50),
            Room("R102", 40)
        ]

        time_slots = {
            "CS101": "09:00",
            "MATH101": "09:00"
        }

        optimizer = Optimizer(
            classes,
            rooms,
            time_slots
        )

        schedule = optimizer.optimize()

        room_ids = [
            entry.room_id
            for entry in schedule
        ]

        self.assertEqual(
            len(room_ids),
            len(set(room_ids))
        )

    def test_optimizer_handles_different_time_slots(self):
        classes = [
            Class("CS101", 40, "P1"),
            Class("MATH101", 35, "P2")
        ]

        rooms = [
            Room("R101", 50),
            Room("R102", 40)
        ]

        time_slots = {
            "CS101": "09:00",
            "MATH101": "10:00"
        }

        optimizer = Optimizer(
            classes,
            rooms,
            time_slots
        )

        schedule = optimizer.optimize()

        self.assertEqual(
            len(schedule),
            2
        )

        schedule_slots = {
            entry.class_id: entry.time_slot
            for entry in schedule
        }

        self.assertEqual(
            schedule_slots["CS101"],
            "09:00"
        )

        self.assertEqual(
            schedule_slots["MATH101"],
            "10:00"
        )

    def test_optimizer_handles_impossible_assignment(self):
        classes = [
            Class("BIG101", 100, "P1")
        ]

        rooms = [
            Room("R101", 50),
            Room("R102", 40)
        ]

        time_slots = {
            "BIG101": "09:00"
        }

        optimizer = Optimizer(
            classes,
            rooms,
            time_slots
        )

        schedule = optimizer.optimize()

        self.assertEqual(
            len(schedule),
            0
        )

    def test_wasted_capacity_is_calculated_correctly(self):
        classes = [
            Class("CS101", 40, "P1")
        ]

        rooms = [
            Room("R101", 50)
        ]

        time_slots = {
            "CS101": "09:00"
        }

        optimizer = Optimizer(
            classes,
            rooms,
            time_slots
        )

        schedule = optimizer.optimize()

        self.assertEqual(
            schedule[0].wasted_capacity,
            10
        )

        self.assertEqual(
            optimizer.calculate_total_wasted_capacity(
                schedule
            ),
            10
        )


if __name__ == "__main__":
    unittest.main()