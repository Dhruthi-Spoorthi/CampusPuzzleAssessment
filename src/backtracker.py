from models import ScheduleEntry


class BacktrackingSolver:

    def __init__(self, classes, rooms, student_groups):
        self.classes = classes
        self.rooms = rooms
        self.student_groups = student_groups
        self.schedule = []
        self.unscheduled = []

        self.time_slots = [
            "09:00",
            "10:00",
            "11:00",
            "12:00",
            "13:00"
        ]

        # Stores the best feasible partial schedule found.
        self.best_schedule = []

    def get_course(self, class_id):
        for course in self.classes:
            if course.class_id == class_id:
                return course

        return None

    def has_conflict(self, course, time_slot, room):
        for entry in self.schedule:

            # Room conflict
            if (
                    entry.time_slot == time_slot
                    and entry.room_id == room.room_id
            ):
                return True

            other_course = self.get_course(
                entry.class_id
            )

            # Professor conflict
            if (
                    other_course
                    and other_course.professor == course.professor
                    and entry.time_slot == time_slot
            ):
                return True

        # Student group conflict
        for group_courses in self.student_groups.values():

            if course.class_id not in group_courses:
                continue

            for entry in self.schedule:

                if entry.time_slot != time_slot:
                    continue

                if entry.class_id in group_courses:
                    return True

        return False

    def update_best_schedule(self):
        """
        Save the largest feasible partial schedule found so far.
        """

        if len(self.schedule) > len(self.best_schedule):
            self.best_schedule = list(self.schedule)

    def backtrack(self, index, courses):
        """
        Recursively search for a complete or best-effort schedule.
        """

        # Update the best partial solution whenever progress is made.
        self.update_best_schedule()

        # All classes have been processed.
        if index == len(courses):
            return True

        course = courses[index]

        # Try every possible time slot and room.
        for time_slot in self.time_slots:

            for room in self.rooms:

                # Capacity pruning
                if room.capacity < course.students:
                    continue

                # Conflict pruning
                if self.has_conflict(
                        course,
                        time_slot,
                        room
                ):
                    continue

                wasted_capacity = (
                        room.capacity - course.students
                )

                entry = ScheduleEntry(
                    course.class_id,
                    time_slot,
                    room.room_id,
                    wasted_capacity
                )

                self.schedule.append(entry)

                # Continue recursively.
                if self.backtrack(
                        index + 1,
                        courses
                ):
                    return True

                # Undo the assignment and try another choice.
                self.schedule.pop()

        # No valid assignment was found for this class.
        # Continue with the remaining classes so that a
        # best-effort solution can still be found.
        if self.backtrack(
                index + 1,
                courses
        ):
            return True

        return False

    def solve(self):
        """
        Generate a complete schedule when possible.

        If a complete schedule is impossible, return the
        largest feasible partial schedule found.
        """

        self.schedule = []
        self.unscheduled = []
        self.best_schedule = []

        courses = sorted(
            self.classes,
            key=lambda course: course.students,
            reverse=True
        )

        self.backtrack(
            0,
            courses
        )

        # Use the complete schedule if one was found.
        # Otherwise use the best partial schedule.
        self.schedule = list(self.best_schedule)

        scheduled_ids = {
            entry.class_id
            for entry in self.schedule
        }

        self.unscheduled = [
            course
            for course in courses
            if course.class_id not in scheduled_ids
        ]

        return self.schedule, self.unscheduled

    def validate_schedule(self):
        errors = []

        class_ids = {
            course.class_id
            for course in self.classes
        }

        room_map = {
            room.room_id: room
            for room in self.rooms
        }

        scheduled_ids = []

        for entry in self.schedule:

            if entry.class_id not in class_ids:
                errors.append(
                    f"Unknown class: {entry.class_id}"
                )
                continue

            if entry.room_id not in room_map:
                errors.append(
                    f"Unknown room: {entry.room_id}"
                )
                continue

            course = self.get_course(
                entry.class_id
            )

            room = room_map[
                entry.room_id
            ]

            if course.students > room.capacity:
                errors.append(
                    f"Class {course.class_id} "
                    f"exceeds room capacity"
                )

            scheduled_ids.append(
                entry.class_id
            )

        # Duplicate class check
        if len(scheduled_ids) != len(
                set(scheduled_ids)
        ):
            errors.append(
                "A class has been scheduled "
                "more than once."
            )

        # Pairwise conflict validation
        for i in range(len(self.schedule)):

            for j in range(
                    i + 1,
                    len(self.schedule)
            ):

                first = self.schedule[i]
                second = self.schedule[j]

                if first.time_slot != second.time_slot:
                    continue

                # Room conflict
                if first.room_id == second.room_id:
                    errors.append(
                        f"Room conflict: "
                        f"{first.room_id} "
                        f"at {first.time_slot}"
                    )

                first_course = self.get_course(
                    first.class_id
                )

                second_course = self.get_course(
                    second.class_id
                )

                if not first_course or not second_course:
                    continue

                # Professor conflict
                if (
                        first_course.professor
                        == second_course.professor
                ):
                    errors.append(
                        f"Professor conflict: "
                        f"{first_course.professor} "
                        f"at {first.time_slot}"
                    )

                # Student group conflict
                for group_courses in (
                        self.student_groups.values()
                ):

                    if (
                            first.class_id in group_courses
                            and second.class_id in group_courses
                    ):
                        errors.append(
                            f"Student group conflict: "
                            f"{first.class_id} and "
                            f"{second.class_id} "
                            f"at {first.time_slot}"
                        )

        return list(dict.fromkeys(errors))