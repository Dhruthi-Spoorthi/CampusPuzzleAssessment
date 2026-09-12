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

        # Keep track of the best schedule we find.
        self.best_schedule = []

    def get_course(self, class_id):
        for course in self.classes:
            if course.class_id == class_id:
                return course

        return None

    def has_conflict(self, course, time_slot, room):
        for entry in self.schedule:

            # Check if the room is already being used.
            if (
                    entry.time_slot == time_slot
                    and entry.room_id == room.room_id
            ):
                return True

            other_course = self.get_course(entry.class_id)

            # Two classes cannot have the same professor
            # at the same time.
            if (
                    other_course
                    and other_course.professor == course.professor
                    and entry.time_slot == time_slot
            ):
                return True

        # Check whether students in the same group
        # would have two classes at the same time.
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
        if len(self.schedule) > len(self.best_schedule):
            self.best_schedule = list(self.schedule)

    def backtrack(self, index, courses):
        # Save the current schedule if it is better
        # than the one we already have.
        self.update_best_schedule()

        # We have gone through all the classes.
        if index == len(courses):
            return True

        course = courses[index]

        # Try each time slot and room for this class.
        for time_slot in self.time_slots:

            for room in self.rooms:

                # The room must be large enough for the class.
                if room.capacity < course.students:
                    continue

                # Skip this choice if it causes a conflict.
                if self.has_conflict(course, time_slot, room):
                    continue

                wasted_capacity = room.capacity - course.students

                entry = ScheduleEntry(
                    course.class_id,
                    time_slot,
                    room.room_id,
                    wasted_capacity
                )

                self.schedule.append(entry)

                # Try scheduling the next class.
                if self.backtrack(index + 1, courses):
                    return True

                # This choice did not work, so remove it
                # and try another room or time slot.
                self.schedule.pop()

        # If this class cannot be scheduled, move on to
        # the next one and keep the best schedule found.
        if self.backtrack(index + 1, courses):
            return True

        return False

    def solve(self):
        self.schedule = []
        self.unscheduled = []
        self.best_schedule = []

        # Schedule larger classes first so that it is
        # easier to find suitable rooms for them.
        courses = sorted(
            self.classes,
            key=lambda course: course.students,
            reverse=True
        )

        self.backtrack(0, courses)

        # Use the best schedule found by the search.
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

            # Check that the class exists.
            if entry.class_id not in class_ids:
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

            course = self.get_course(entry.class_id)
            room = room_map[entry.room_id]

            # Make sure the class fits in the room.
            if course.students > room.capacity:
                errors.append(
                    f"Class {course.class_id} "
                    f"exceeds room capacity"
                )

            scheduled_ids.append(entry.class_id)

        # A class should only appear once in the schedule.
        if len(scheduled_ids) != len(set(scheduled_ids)):
            errors.append(
                "A class has been scheduled more than once."
            )

        # Compare every pair of classes that are
        # scheduled at the same time.
        for i in range(len(self.schedule)):

            for j in range(i + 1, len(self.schedule)):

                first = self.schedule[i]
                second = self.schedule[j]

                if first.time_slot != second.time_slot:
                    continue

                # Two classes cannot use the same room
                # at the same time.
                if first.room_id == second.room_id:
                    errors.append(
                        f"Room conflict: "
                        f"{first.room_id} "
                        f"at {first.time_slot}"
                    )

                first_course = self.get_course(first.class_id)
                second_course = self.get_course(second.class_id)

                if not first_course or not second_course:
                    continue

                # Two classes cannot use the same professor
                # at the same time.
                if first_course.professor == second_course.professor:
                    errors.append(
                        f"Professor conflict: "
                        f"{first_course.professor} "
                        f"at {first.time_slot}"
                    )

                # Check if both classes belong to the same
                # student group.
                for group_courses in self.student_groups.values():

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

        # Remove duplicate error messages.
        return list(dict.fromkeys(errors))