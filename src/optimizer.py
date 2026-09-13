from models import ScheduleEntry


class Optimizer:

    def __init__(self, classes, rooms, time_slots):
        self.classes = classes
        self.rooms = rooms
        self.time_slots = time_slots

        self.class_map = {
            course.class_id: course
            for course in classes
        }

        self.optimized_schedule = []

    def calculate_total_wasted_capacity(self, schedule=None):

        if schedule is None:
            schedule = self.optimized_schedule

        total = 0

        for entry in schedule:
            total += entry.wasted_capacity

        return total

    def get_classes_for_time_slot(self, time_slot):

        result = []

        for class_id, assigned_slot in self.time_slots.items():
            if assigned_slot == time_slot:
                course = self.class_map.get(class_id)

                if course is not None:
                    result.append(course)

        return result

    def dynamic_programming(self, courses):

        memo = {}

        def dp(index, used_rooms):

            if index == len(courses):
                return 0, []

            state = (index, used_rooms)

            if state in memo:
                return memo[state]

            course = courses[index]

            best_waste = float("inf")
            best_assignment = None

            for room in self.rooms:

                if room.room_id in used_rooms:
                    continue

                if room.capacity < course.students:
                    continue

                wasted_capacity = (
                        room.capacity - course.students
                )

                new_used_rooms = tuple(
                    sorted(
                        used_rooms + (room.room_id,)
                    )
                )

                remaining_waste, remaining_assignment = dp(
                    index + 1,
                    new_used_rooms
                )

                if remaining_assignment is None:
                    continue

                total_waste = (
                        wasted_capacity + remaining_waste
                )

                if total_waste < best_waste:
                    best_waste = total_waste

                    best_assignment = [
                                          room.room_id
                                      ] + remaining_assignment

            if best_assignment is None:
                result = (float("inf"), None)
            else:
                result = (
                    best_waste,
                    best_assignment
                )

            memo[state] = result

            return result

        return dp(0, tuple())

    def optimize(self):

        self.optimized_schedule = []

        unique_time_slots = []

        for slot in self.time_slots.values():
            if slot not in unique_time_slots:
                unique_time_slots.append(slot)

        for time_slot in unique_time_slots:

            courses = self.get_classes_for_time_slot(
                time_slot
            )

            if not courses:
                continue

            courses = sorted(
                courses,
                key=lambda course: course.students,
                reverse=True
            )

            minimum_waste, room_assignment = (
                self.dynamic_programming(courses)
            )

            if room_assignment is None:
                continue

            for course, room_id in zip(
                    courses,
                    room_assignment
            ):

                room = next(
                    (
                        r for r in self.rooms
                        if r.room_id == room_id
                    ),
                    None
                )

                if room is None:
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

                self.optimized_schedule.append(entry)

        return self.optimized_schedule