import os
import sys
import unittest

sys.path.insert(
    0,
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

from models import Class, Room, ScheduleEntry
from backtracker import BacktrackingSolver


class TestBacktrackingSolver(unittest.TestCase):

    def setUp(self):

        self.classes = [
            Class("CS101", 40, "P1"),
            Class("MATH101", 35, "P2"),
            Class("CS102", 30, "P1"),
            Class("HIST101", 20, "P3"),
            Class("PROG101", 45, "P4"),
            Class("DB101", 25, "P5")
        ]

        self.rooms = [
            Room("R101", 50),
            Room("R102", 40),
            Room("R103", 30),
            Room("R104", 20)
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

        self.solver = BacktrackingSolver(
            self.classes,
            self.rooms,
            self.student_groups
        )

    def test_backtracking_schedules_all_classes(self):

        schedule, unscheduled = self.solver.solve()

        self.assertEqual(
            len(schedule),
            6
        )

        self.assertEqual(
            len(unscheduled),
            0
        )

    def test_no_class_is_scheduled_twice(self):

        schedule, _ = self.solver.solve()

        class_ids = [
            entry.class_id
            for entry in schedule
        ]

        self.assertEqual(
            len(class_ids),
            len(set(class_ids))
        )

    def test_room_capacity_is_respected(self):

        schedule, _ = self.solver.solve()

        class_map = {
            course.class_id: course
            for course in self.classes
        }

        room_map = {
            room.room_id: room
            for room in self.rooms
        }

        for entry in schedule:

            course = class_map[entry.class_id]
            room = room_map[entry.room_id]

            self.assertLessEqual(
                course.students,
                room.capacity
            )

    def test_no_room_conflicts(self):

        schedule, _ = self.solver.solve()

        for i in range(len(schedule)):

            for j in range(i + 1, len(schedule)):

                first = schedule[i]
                second = schedule[j]

                if first.time_slot == second.time_slot:

                    self.assertNotEqual(
                        first.room_id,
                        second.room_id
                    )

    def test_no_professor_conflicts(self):

        schedule, _ = self.solver.solve()

        class_map = {
            course.class_id: course
            for course in self.classes
        }

        for i in range(len(schedule)):

            for j in range(i + 1, len(schedule)):

                first = schedule[i]
                second = schedule[j]

                if first.time_slot != second.time_slot:
                    continue

                first_course = class_map[first.class_id]
                second_course = class_map[second.class_id]

                self.assertNotEqual(
                    first_course.professor,
                    second_course.professor
                )

    def test_student_group_conflicts_are_avoided(self):

        schedule, _ = self.solver.solve()

        for group_courses in self.student_groups.values():

            for i in range(len(schedule)):

                for j in range(i + 1, len(schedule)):

                    first = schedule[i]
                    second = schedule[j]

                    if first.class_id not in group_courses:
                        continue

                    if second.class_id not in group_courses:
                        continue

                    if first.time_slot == second.time_slot:

                        self.fail(
                            f"Student group conflict: "
                            f"{first.class_id} and "
                            f"{second.class_id} at "
                            f"{first.time_slot}"
                        )

    def test_impossible_class_is_unscheduled(self):

        impossible_classes = [
            Class("BIG101", 100, "P10")
        ]

        solver = BacktrackingSolver(
            impossible_classes,
            self.rooms,
            {}
        )

        schedule, unscheduled = solver.solve()

        self.assertEqual(
            len(schedule),
            0
        )

        self.assertEqual(
            len(unscheduled),
            1
        )

        self.assertEqual(
            unscheduled[0].class_id,
            "BIG101"
        )


if __name__ == "__main__":
    unittest.main()