import sys
import os
import unittest

sys.path.insert(
    0,
    os.path.dirname(os.path.abspath(__file__))
)

from models import Class
from graph_engine import ConflictGraph


class TestConflictGraph(unittest.TestCase):

    def setUp(self):

        self.classes = [
            Class("CS101", 40, "P1"),
            Class("MATH101", 35, "P2"),
            Class("CS102", 30, "P1"),
            Class("HIST101", 20, "P3"),
            Class("PROG101", 45, "P4"),
            Class("DB101", 25, "P5")
        ]

        self.student_groups = {
            "GroupA": [
                "CS101",
                "MATH101",
                "PROG101"
            ],
            "GroupB": [
                "CS102",
                "DB101"
            ],
            "GroupC": [
                "HIST101",
                "MATH101"
            ]
        }

        self.graph = ConflictGraph(
            self.classes,
            self.student_groups
        )

        self.graph.build_graph()

    def test_professor_conflict(self):

        # CS101 and CS102 have the same professor P1
        self.assertIn(
            "CS102",
            self.graph.graph["CS101"]
        )

        self.assertIn(
            "CS101",
            self.graph.graph["CS102"]
        )

    def test_student_group_conflict(self):

        # CS101 and MATH101 share GroupA
        self.assertIn(
            "MATH101",
            self.graph.graph["CS101"]
        )

        # MATH101 and HIST101 share GroupC
        self.assertIn(
            "HIST101",
            self.graph.graph["MATH101"]
        )

    def test_no_false_conflict(self):

        # CS102 and HIST101 share neither
        # professor nor student group
        self.assertNotIn(
            "HIST101",
            self.graph.graph["CS102"]
        )

    def test_welsh_powell_coloring(self):

        colors = self.graph.welsh_powell()

        # Every class must receive a color
        self.assertEqual(
            len(colors),
            len(self.classes)
        )

        # Conflicting classes must have
        # different colors
        for class_id, neighbors in self.graph.graph.items():

            for neighbor in neighbors:

                self.assertNotEqual(
                    colors[class_id],
                    colors[neighbor]
                )

    def test_time_slot_assignment(self):

        time_slots = self.graph.assign_time_slots()

        # Every class should receive a time slot
        self.assertEqual(
            len(time_slots),
            len(self.classes)
        )

        for class_id, time_slot in time_slots.items():

            self.assertIsNotNone(time_slot)

            self.assertIn(
                time_slot,
                ConflictGraph.TIME_SLOTS
            )

    def test_conflict_report(self):

        report = self.graph.get_conflict_report()

        # There should be conflicts in our dataset
        self.assertGreater(
            len(report),
            0
        )

        # Check that known conflicts appear
        combined_report = " ".join(report)

        self.assertIn(
            "CS101",
            combined_report
        )

        self.assertIn(
            "MATH101",
            combined_report
        )


if __name__ == "__main__":
    unittest.main()