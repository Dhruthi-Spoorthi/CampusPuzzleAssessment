class Class:
    def __init__(self, class_id, students, professor):
        self.class_id = class_id
        self.students = students
        self.professor = professor

    def __repr__(self):
        return f"Class({self.class_id}, {self.students} students, {self.professor})"


class Room:
    def __init__(self, room_id, capacity):
        self.room_id = room_id
        self.capacity = capacity

    def __repr__(self):
        return f"Room({self.room_id}, capacity={self.capacity})"


class ScheduleEntry:
    def __init__(self, class_id, time_slot, room_id, wasted_capacity):
        self.class_id = class_id
        self.time_slot = time_slot
        self.room_id = room_id
        self.wasted_capacity = wasted_capacity

    def __repr__(self):
        return (
            f"ScheduleEntry("
            f"{self.class_id}, "
            f"{self.time_slot}, "
            f"{self.room_id}, "
            f"wasted={self.wasted_capacity})"
        )