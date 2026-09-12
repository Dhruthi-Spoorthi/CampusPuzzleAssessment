from models import ScheduleEntry


TIME_SLOTS = [
    "09:00",
    "10:00",
    "11:00",
    "12:00",
    "13:00"
]


class GreedySolver:

    def __init__(self, classes, rooms, student_groups):
        self.classes = classes
        self.rooms = rooms
        self.student_groups = student_groups

        self.schedule = []
        self.unscheduled = []

    def sort_classes(self):
        """
        Sort classes from largest to smallest.
        """

        return sorted(
            self.classes,
            key=lambda course: course.students,
            reverse=True
        )

    def room_can_fit(self, course, room):
        """
        Check if the room is large enough for the class.
        """

        return room.capacity >= course.students

    def has_conflict(self, course, time_slot, room):
        """
        Check for room, professor, and student group conflicts.
        """

        for entry in self.schedule:

            # A room cannot be used by two classes at once.
            if (
                    entry.time_slot == time_slot
                    and entry.room_id == room.room_id
            ):
                return True

            scheduled_course = next(
                (
                    c for c in self.classes
                    if c.class_id == entry.class_id
                ),
                None
            )

            # A professor cannot teach two classes at once.
            if (
                    scheduled_course
                    and scheduled_course.professor == course.professor
                    and entry.time_slot == time_slot
            ):
                return True

        # Check for student group conflicts.
        for group_courses in self.student_groups.values():

            if course.class_id not in group_courses:
                continue

            for entry in self.schedule:

                if entry.time_slot != time_slot:
                    continue

                if entry.class_id in group_courses:
                    return True

        return False

    def solve(self):
        self.schedule = []
        self.unscheduled = []

        sorted_classes = self.sort_classes()

        for course in sorted_classes:

            placed = False

            # Try each time slot and room in order.
            for time_slot in TIME_SLOTS:

                for room in self.rooms:

                    # Skip rooms that are too small.
                    if not self.room_can_fit(course, room):
                        continue

                    # Skip this choice if there is a conflict.
                    if self.has_conflict(
                            course,
                            time_slot,
                            room
                    ):
                        continue

                    wasted_capacity = room.capacity - course.students

                    entry = ScheduleEntry(
                        course.class_id,
                        time_slot,
                        room.room_id,
                        wasted_capacity
                    )

                    self.schedule.append(entry)

                    placed = True
                    break

                if placed:
                    break

            # No suitable room and time slot was found.
            if not placed:
                self.unscheduled.append(course)

        return self.schedule, self.unscheduled

    def validate_schedule(self):
        errors = []

        class_map = {
            course.class_id: course
            for course in self.classes
        }

        room_map = {
            room.room_id: room
            for room in self.rooms
        }

        for entry in self.schedule:

            # Check that the class exists.
            if entry.class_id not in class_map:
                errors.append(
                    f"Unknown class: {entry.class_id}"
                )
                continue

            # Check that the room exists.
            if entry.room_id not in room_map:
                errors.append(
                    f"Unknown room: {entry.room_id}"
                )
                continue

            course = class_map[entry.class_id]
            room = room_map[entry.room_id]

            # Make sure the class fits in the room.
            if course.students > room.capacity:
                errors.append(
                    f"Class {course.class_id} "
                    f"exceeds room capacity"
                )

            # Check for professor conflicts.
            for other in self.schedule:

                if other is entry:
                    continue

                if (
                        other.time_slot == entry.time_slot
                        and other.class_id != entry.class_id
                ):

                    other_course = class_map.get(
                        other.class_id
                    )

                    if (
                            other_course
                            and other_course.professor
                            == course.professor
                    ):
                        errors.append(
                            f"Professor conflict: "
                            f"{course.professor} "
                            f"at {entry.time_slot}"
                        )

            # Check for room conflicts.
            for other in self.schedule:

                if other is entry:
                    continue

                if (
                        other.time_slot == entry.time_slot
                        and other.room_id == entry.room_id
                        and other.class_id != entry.class_id
                ):
                    errors.append(
                        f"Room conflict: "
                        f"{entry.room_id} "
                        f"at {entry.time_slot}"
                    )

        # Remove duplicate error messages.
        return list(dict.fromkeys(errors))