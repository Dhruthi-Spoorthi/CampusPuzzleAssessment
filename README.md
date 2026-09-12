# Campus Puzzle Assessment

## GitHub Repository

GitHub repository:

 https://github.com/Dhruthi-Spoorthi/CampusPuzzleAssessment

---

# 1. Project Overview

This project is a campus class scheduling system that uses different algorithms to create a valid timetable.

The system assigns classes to available rooms and time slots while making sure that the main scheduling rules are followed. These include room capacity, room availability, professor availability, and student group conflicts.

The project uses five main stages:

1. Greedy Scheduling
2. Conflict Graph
3. Welsh-Powell Coloring
4. Dynamic Programming Room Optimization
5. Backtracking

Each method has a different purpose. Together, they help create, improve, and check the final timetable.

---

# 2. Scheduling Constraints

The scheduler follows these rules:

* A room must have enough capacity for the class.
* A room cannot be used for two classes at the same time.
* A professor cannot teach two classes at the same time.
* Students in the same group cannot have two classes at the same time.
* Classes that cannot be placed in any suitable room are reported as unscheduled.
* The optimization stage tries to reduce unused room capacity while keeping the schedule valid.

---

# 3. Input Data

The scheduling data is stored in:

```text
data/constraints.json
```

The dataset contains:

* 6 classes
* 4 rooms
* 3 student groups
* 5 available time slots

## Classes

| Class   | Students | Professor |
| ------- | -------: | --------- |
| CS101   |       40 | P1        |
| MATH101 |       35 | P2        |
| CS102   |       30 | P1        |
| HIST101 |       20 | P3        |
| PROG101 |       45 | P4        |
| DB101   |       25 | P5        |

## Rooms

| Room | Capacity |
| ---- | -------: |
| R101 |       50 |
| R102 |       40 |
| R103 |       30 |
| R104 |       20 |

## Student Groups

There are three student groups:

```text
GroupA:
CS101
MATH101
PROG101

GroupB:
CS102
DB101

GroupC:
HIST101
MATH101
```

Classes belonging to the same student group cannot be scheduled at the same time.

---

# 4. Stage 1 - Greedy Scheduling

The Greedy Solver starts by sorting classes according to the number of students, from largest to smallest.

This is useful because larger classes usually have fewer room choices. Scheduling them first makes it less likely that a suitable room will already be taken by a smaller class.

For every class, the solver checks:

1. Available time slots
2. Rooms in their original order
3. Room capacity
4. Room conflicts
5. Professor conflicts
6. Student group conflicts

The first combination that satisfies all the conditions is selected.

## Why Greedy?

Greedy gives the project a simple and fast baseline solution. Instead of checking every possible timetable, it makes the best immediate choice for each class.

The main limitation is that a locally good choice is not always the best choice for the complete timetable. Therefore, the Greedy Solver is mainly used as a baseline for comparison with the other methods.

---

# 5. Stage 2 - Conflict Graph

The Conflict Graph represents each class as a vertex.

An edge is added between two classes when they cannot be held at the same time.

Two classes conflict when:

* They have the same professor, or
* They share a student group.

For example, if two classes belong to the same student group, they need an edge between them because the students cannot attend both classes at once.

This graph gives a clear way to represent the time-related constraints of the timetable.

---

# 6. Stage 3 - Welsh-Powell Graph Coloring

The Welsh-Powell algorithm is applied to the conflict graph.

It first orders classes based on their graph degree and then assigns colors so that connected classes receive different colors.

For this project:

```text
One color represents one time-slot group.
```

Therefore, two classes that conflict cannot have the same color.

The colors are then mapped to actual time slots:

```text
09:00
10:00
11:00
12:00
13:00
```

This produces a time-slot assignment that respects the conflicts represented in the graph.

---

# 7. Stage 4 - Dynamic Programming Room Optimization

Once the time slots have been decided, Dynamic Programming is used to improve the room assignments.

The goal is to reduce the amount of unused room capacity without breaking any scheduling rules.

The wasted capacity for a class is calculated as:

```text
Wasted capacity = Room capacity - Number of students
```

Only rooms large enough for the class are considered, and a room can only be assigned to one class within the same time slot.

## DP State

The Dynamic Programming state keeps track of the current class and the rooms already used in that time slot.

Conceptually:

```text
DP(index, used_rooms)
```

where:

* `index` is the next class that needs a room.
* `used_rooms` contains the rooms already assigned.

The state stores the minimum possible wasted capacity for the remaining assignments.

The recurrence can be represented as:

```text
DP(index, used_rooms)
=
min(
    wasted_capacity
    + DP(index + 1, updated_used_rooms)
)
```

When all classes in the current time slot have been assigned:

```text
DP(number_of_classes, used_rooms) = 0
```

Previously solved states are stored and reused, which avoids repeating the same calculations.

## Why Dynamic Programming?

A simple exhaustive approach could check the same room combinations many times. Dynamic Programming avoids some of this repeated work by remembering results from earlier states.

This makes the room-allocation problem more organized and allows the program to focus on minimizing wasted capacity.

---

# 8. Stage 5 - Backtracking

The Backtracking Solver uses recursive search to try different class, room, and time-slot combinations.

For each class, it:

1. Selects a time slot.
2. Selects a room.
3. Checks room capacity.
4. Checks room conflicts.
5. Checks professor conflicts.
6. Checks student group conflicts.
7. Moves on to the next class.

If an assignment breaks a rule, that option is rejected.

If the solver reaches a later point where the timetable can no longer be completed, it goes back to the previous decision and tries another option.

## Pruning

Invalid branches are rejected as early as possible.

For example:

```text
Room too small
    ↓
Reject branch

Room already occupied
    ↓
Reject branch

Professor already teaching
    ↓
Reject branch

Student group already has a class
    ↓
Reject branch
```

This prevents the solver from wasting time exploring schedules that cannot become valid.

Compared with Greedy Scheduling, Backtracking provides a more exhaustive search for possible schedules.

---

# 9. Conflict Report

The graph engine also produces a conflict report.

It identifies conflicts caused by:

* Shared professors
* Shared student groups

This makes it easier to understand why certain classes cannot be placed in the same time slot.

The conflict graph is therefore useful not only for coloring but also for explaining the scheduling constraints.

---

# 10. Algorithm Comparison

Each algorithm has a different role in the project.

| Algorithm           | Main Purpose            | Main Advantage                  |
| ------------------- | ----------------------- | ------------------------------- |
| Greedy              | Baseline scheduling     | Fast and simple                 |
| Conflict Graph      | Represent conflicts     | Makes conflicts clear           |
| Welsh-Powell        | Assign time-slot groups | Respects graph conflicts        |
| Dynamic Programming | Optimize rooms          | Reduces wasted capacity         |
| Backtracking        | Search for schedules    | Can try alternative assignments |

The algorithms complement each other rather than doing exactly the same job.

Greedy provides the starting point, the Conflict Graph and Welsh-Powell handle time conflicts, Dynamic Programming improves room usage, and Backtracking provides a more thorough search.

---

# 11. Complexity Analysis

Let:

```text
C = number of classes
R = number of rooms
T = number of time slots
```

## Greedy Solver

The Greedy Solver checks classes, time slots, rooms, and existing schedule conflicts.

A simplified worst-case complexity is:

```text
O(C² × T × R)
```

The additional space used for the schedule and unscheduled classes is approximately:

```text
O(C)
```

## Conflict Graph

The graph compares pairs of classes to find conflicts.

Worst-case time complexity:

```text
O(C²)
```

Worst-case space complexity:

```text
O(C²)
```

because many pairs of classes may have conflicts.

## Welsh-Powell

Welsh-Powell sorts the classes and examines their graph relationships while assigning colors.

For this implementation, the approximate worst-case complexity is:

```text
O(C²)
```

The graph requires approximately:

```text
O(C²)
```

space in the worst case.

## Dynamic Programming

For a time slot containing `C_s` classes and `R` rooms, the possible room-use states can grow with:

```text
2^R
```

The approximate worst-case time complexity is:

```text
O(C_s × R × 2^R)
```

with approximately:

```text
O(C_s × 2^R)
```

space for the DP states.

The main benefit is that previously calculated states are reused.

## Backtracking

Backtracking has exponential worst-case complexity because it can explore many possible assignments.

A simplified upper bound is:

```text
O((T × R)^C)
```

since each class can potentially be assigned to different time-slot and room combinations.

The recursive call stack uses approximately:

```text
O(C)
```

space, excluding the schedule and input structures.

In practice, pruning removes many invalid branches and reduces the amount of searching required.

---

# 12. Testing

The project includes unit tests for the main scheduling components.

The tests cover:

* Greedy scheduling
* Room capacity
* Professor conflicts
* Student group conflicts
* Conflict graph construction
* Welsh-Powell coloring
* Graph-based time-slot assignment
* Dynamic Programming optimization
* Room allocation
* Wasted capacity
* Impossible room assignments
* Backtracking
* Duplicate scheduling prevention

The complete test suite contains:

```text
25 tests
```

The latest result is:

```text
Ran 25 tests
OK
Process finished with exit code 0
```

All 25 tests pass successfully.

---

# 13. Results

The current dataset contains:

```text
Total classes: 6
```

The scheduling system successfully schedules all six classes with the current input.

The program reports the number of scheduled and unscheduled classes for the Greedy, Dynamic Programming, and Backtracking stages.

The Dynamic Programming stage also reports the total wasted room capacity.

The program compares:

```text
Greedy total wasted capacity
DP total wasted capacity
Capacity improvement
```

This gives a simple way to compare the room allocation produced by the different approaches.

---

# 14. Validation

The generated schedules are checked against the main constraints.

The validation process checks:

* Room capacity violations
* Room conflicts
* Professor conflicts
* Duplicate class assignments
* Student group conflicts

A schedule is considered valid when no validation errors are found.

The current dataset produces a valid schedule.

---

# 15. Unscheduled Classes

The system also handles situations where a class cannot be scheduled.

For example, if a class has more students than the capacity of every available room, there is no valid room for it.

In that situation, the class is added to the unscheduled collection and reported by the program.

The system therefore separates classes into:

```text
Scheduled
```

and:

```text
Unscheduled
```

When a class cannot be scheduled, the program also reports the reason.

---

# 16. Project Structure

```text
CampusPuzzleAssessment/
│
├── data/
│   └── constraints.json
│
├── src/
│   ├── models.py
│   ├── greedy_solver.py
│   ├── graph_engine.py
│   ├── optimizer.py
│   ├── backtracker.py
│   ├── main.py
│   │
│   ├── test_greedy_solver.py
│   ├── test_graph_engine.py
│   ├── test_optimizer.py
│   └── test_backtracking_solver.py
│
└── README.md
```

---

# 17. Manual Fix Log

A few issues were found and corrected during development.

| Issue                                                     | Resolution                                                                                         |
| --------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| Backtracking test imported the wrong module               | Updated the test to use `BacktrackingSolver` from `backtracker.py`                                 |
| Greedy initially selected the smallest fitting room       | Changed it to check rooms in their original order and select the first feasible room               |
| Optimizer was initially a simple room-by-room improvement | Reworked it into the Dynamic Programming room-optimization component                               |
| Optimizer was not connected to the main program           | Added the optimizer to `main.py`                                                                   |
| Optimizer needed more validation                          | Added tests for capacity, room uniqueness, time slots, impossible assignments, and wasted capacity |
| Regression testing was required                           | Ran the full test suite and confirmed all 25 tests pass                                            |

These fixes helped keep the different parts of the project connected and working together.

---

# 18. Design Justification

Each algorithm was selected because it solves a different part of the scheduling problem.

## Greedy

Greedy provides a quick and straightforward baseline. Sorting classes by student count gives larger classes priority because they usually have fewer suitable rooms.

## Conflict Graph

The graph gives a clear representation of which classes cannot share a time slot.

## Welsh-Powell

Welsh-Powell provides a practical way to color the graph and group classes into compatible time slots.

## Dynamic Programming

Dynamic Programming is used after the time slots are decided. At this point, the main problem is choosing rooms efficiently.

The goal is to reduce wasted room capacity while still respecting room availability.

## Backtracking

Backtracking gives the system a more thorough search strategy. It can undo previous choices and try different assignments when an earlier decision leads to a problem.

---

# 19. Conclusion

This project shows how different algorithmic techniques can be combined to solve a campus scheduling problem with several constraints.

The Greedy algorithm provides a fast baseline.

The Conflict Graph represents relationships between classes that cannot happen at the same time.

Welsh-Powell coloring uses those relationships to create conflict-aware time-slot assignments.

Dynamic Programming improves room allocation by trying to reduce wasted capacity.

Backtracking provides a recursive way to explore alternative assignments.

The project is organized into separate modules for the different algorithms and includes automated tests for the major components.

For the provided dataset, all six classes are successfully scheduled, and all 25 tests pass.
