import json
import os

from models import Class, Room
from greedy_solver import GreedySolver
from graph_engine import ConflictGraph
from optimizer import Optimizer
from backtracker import BacktrackingSolver


def load_data():

    data_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "data",
        "constraints.json"
    )

    with open(data_path, "r") as file:
        data = json.load(file)

    classes = [
        Class(
            item["id"],
            item["students"],
            item["professor"]
        )
        for item in data["classes"]
    ]

    rooms = [
        Room(
            item["id"],
            item["capacity"]
        )
        for item in data["rooms"]
    ]

    student_groups = data["student_groups"]

    return classes, rooms, student_groups


def get_unscheduled_reason(course, rooms):
    """
    Provide a simple explanation for why a class
    could not be scheduled.
    """

    if not rooms:
        return "no rooms are available"

    largest_capacity = max(
        room.capacity
        for room in rooms
    )

    if course.students > largest_capacity:
        return (
            "no available room has sufficient capacity"
        )

    return (
        "no feasible room and time-slot combination "
        "was available"
    )


def print_unscheduled_classes(
        unscheduled,
        rooms
):
    """
    Print unscheduled classes together with
    an explanation.
    """

    if not unscheduled:
        print("None")
        return

    for course in unscheduled:
        reason = get_unscheduled_reason(
            course,
            rooms
        )

        print(
            f"{course.class_id} - "
            f"Reason: {reason}"
        )


def main():

    classes, rooms, student_groups = load_data()

    # ==========================================
    # STAGE 1 - GREEDY BASELINE
    # ==========================================

    print("=== GREEDY BASELINE ===")

    greedy_solver = GreedySolver(
        classes,
        rooms,
        student_groups
    )

    greedy_schedule, greedy_unscheduled = (
        greedy_solver.solve()
    )

    print("\nGreedy schedule:")

    for entry in greedy_schedule:
        print(entry)

    print("\nGreedy unscheduled classes:")

    print_unscheduled_classes(
        greedy_unscheduled,
        rooms
    )

    print("\nGreedy validation:")

    greedy_errors = (
        greedy_solver.validate_schedule()
    )

    if not greedy_errors:
        print("Schedule is valid.")
    else:
        for error in greedy_errors:
            print(error)

    # ==========================================
    # STAGE 2 - CONFLICT GRAPH
    # ==========================================

    print("\n=== CONFLICT GRAPH ===")

    graph = ConflictGraph(
        classes,
        student_groups
    )

    graph.build_graph()

    print("\nClass conflicts:")

    for class_id, neighbors in graph.graph.items():

        if neighbors:
            print(
                f"{class_id}: "
                f"{', '.join(sorted(neighbors))}"
            )
        else:
            print(
                f"{class_id}: No conflicts"
            )

    # ==========================================
    # STAGE 3 - WELSH-POWELL COLORING
    # ==========================================

    print("\n=== WELSH-POWELL COLORING ===")

    colors = graph.welsh_powell()

    for class_id, color in colors.items():
        print(
            f"{class_id} -> Color {color}"
        )

    # ==========================================
    # STAGE 4 - GRAPH-BASED TIME SLOTS
    # ==========================================

    print("\n=== GRAPH-BASED TIME SLOTS ===")

    time_slots = graph.assign_time_slots()

    for class_id in sorted(time_slots):
        print(
            f"{class_id} -> "
            f"{time_slots[class_id]}"
        )

    # ==========================================
    # STAGE 5 - CONFLICT REPORT
    # ==========================================

    print("\n=== CONFLICT REPORT ===")

    conflict_report = graph.get_conflict_report()

    if not conflict_report:
        print("No conflicts found.")
    else:
        for conflict in conflict_report:
            print(conflict)

    # ==========================================
    # STAGE 6 - DYNAMIC PROGRAMMING
    # ==========================================

    print("\n=== DYNAMIC PROGRAMMING OPTIMIZATION ===")

    optimizer = Optimizer(
        classes,
        rooms,
        time_slots
    )

    dp_schedule = optimizer.optimize()

    print("\nDP schedule:")

    for entry in dp_schedule:
        print(entry)

    dp_total_wasted_capacity = (
        optimizer.calculate_total_wasted_capacity(
            dp_schedule
        )
    )

    print("\nDP total wasted capacity:")

    print(dp_total_wasted_capacity)

    greedy_total_wasted_capacity = sum(
        entry.wasted_capacity
        for entry in greedy_schedule
    )

    capacity_improvement = (
            greedy_total_wasted_capacity
            - dp_total_wasted_capacity
    )

    print("\nCapacity improvement:")

    print(capacity_improvement)

    print("\nDP unscheduled classes:")

    dp_scheduled_ids = {
        entry.class_id
        for entry in dp_schedule
    }

    dp_unscheduled = [
        course
        for course in classes
        if course.class_id not in dp_scheduled_ids
    ]

    print_unscheduled_classes(
        dp_unscheduled,
        rooms
    )

    # ==========================================
    # STAGE 7 - BACKTRACKING SOLVER
    # ==========================================

    print("\n=== BACKTRACKING SOLVER ===")

    backtracking_solver = BacktrackingSolver(
        classes,
        rooms,
        student_groups
    )

    backtracking_schedule, backtracking_unscheduled = (
        backtracking_solver.solve()
    )

    print("\nBacktracking schedule:")

    for entry in backtracking_schedule:
        print(entry)

    print("\nBacktracking unscheduled classes:")

    print_unscheduled_classes(
        backtracking_unscheduled,
        rooms
    )

    print("\nBacktracking validation:")

    backtracking_errors = (
        backtracking_solver.validate_schedule()
    )

    if not backtracking_errors:
        print("Schedule is valid.")
    else:
        for error in backtracking_errors:
            print(error)

    # ==========================================
    # FINAL SUMMARY
    # ==========================================

    print("\n=== FINAL SCHEDULE SUMMARY ===")

    print(
        f"Total classes: {len(classes)}"
    )

    print(
        f"Greedy scheduled: "
        f"{len(greedy_schedule)}"
    )

    print(
        f"Greedy unscheduled: "
        f"{len(greedy_unscheduled)}"
    )

    print(
        f"DP scheduled: "
        f"{len(dp_schedule)}"
    )

    print(
        f"DP unscheduled: "
        f"{len(dp_unscheduled)}"
    )

    print(
        f"Backtracking scheduled: "
        f"{len(backtracking_schedule)}"
    )

    print(
        f"Backtracking unscheduled: "
        f"{len(backtracking_unscheduled)}"
    )


if __name__ == "__main__":
    main()