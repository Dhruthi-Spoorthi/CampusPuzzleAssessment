class ConflictGraph:

    TIME_SLOTS = [
        "09:00",
        "10:00",
        "11:00",
        "12:00",
        "13:00"
    ]

    def __init__(self, classes, student_groups):
        self.classes = classes
        self.student_groups = student_groups

        self.graph = {
            course.class_id: set()
            for course in classes
        }

        self.colors = {}
        self.time_slots = {}

    def build_graph(self):

        for i in range(len(self.classes)):

            course_a = self.classes[i]

            for j in range(i + 1, len(self.classes)):

                course_b = self.classes[j]

                if course_a.professor == course_b.professor:
                    self.graph[course_a.class_id].add(
                        course_b.class_id
                    )
                    self.graph[course_b.class_id].add(
                        course_a.class_id
                    )

        for group_courses in self.student_groups.values():

            for i in range(len(group_courses)):

                class_a = group_courses[i]

                for j in range(i + 1, len(group_courses)):

                    class_b = group_courses[j]

                    if (
                            class_a in self.graph
                            and class_b in self.graph
                    ):
                        self.graph[class_a].add(class_b)
                        self.graph[class_b].add(class_a)

        return self.graph

    def welsh_powell(self):

        if not any(self.graph.values()):
            self.build_graph()

        ordered_classes = sorted(
            self.graph,
            key=lambda class_id: len(self.graph[class_id]),
            reverse=True
        )

        self.colors = {}

        for class_id in ordered_classes:

            used_colors = {
                self.colors[neighbor]
                for neighbor in self.graph[class_id]
                if neighbor in self.colors
            }

            color = 0

            while color in used_colors:
                color += 1

            self.colors[class_id] = color

        return self.colors

    def assign_time_slots(self):

        if not self.colors:
            self.welsh_powell()

        self.time_slots = {}

        for class_id, color in self.colors.items():

            if color < len(self.TIME_SLOTS):
                self.time_slots[class_id] = self.TIME_SLOTS[color]
            else:
                self.time_slots[class_id] = None

        return self.time_slots

    def get_conflicts(self):
        conflicts = []

        for class_id in self.graph:

            for other_id in self.graph[class_id]:


                if class_id < other_id:
                    conflicts.append(
                        (class_id, other_id)
                    )

        return sorted(conflicts)

    def get_conflict_report(self):

        report = []

        for class_a, class_b in self.get_conflicts():
            report.append(
                f"{class_a} conflicts with {class_b}"
            )

        if not report:
            report.append("No conflicts found.")

        return report