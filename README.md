# Campus Puzzle Assessment

## GitHub Repository

GitHub repository:

PASTE-YOUR-GITHUB-REPOSITORY-LINK-HERE

---

# 1. Project Overview

This project solves a campus class scheduling problem using multiple
algorithmic approaches.

The system assigns classes to available rooms and time slots while
respecting room capacity, room availability, professor availability,
and student group constraints.

The project implements four main algorithmic approaches:

1. Greedy Scheduling
2. Conflict Graph with Welsh-Powell Coloring
3. Dynamic Programming Room Optimization
4. Backtracking Search

The approaches are used to construct, improve, and validate a feasible
class timetable.

---

# 2. Scheduling Constraints

The scheduler considers the following constraints:

- A class must be assigned to a room with sufficient capacity.
- A room cannot contain two classes at the same time.
- A professor cannot teach two classes at the same time.
- Classes attended by the same student group cannot occur at the same
  time.
- Classes that cannot fit into any available room must be reported as
  unscheduled.
- The optimization stage aims to minimize wasted room capacity while
  maintaining feasibility.

---

# 3. Input Data

The scheduling constraints are stored in:

```text
data/constraints.json
```

The dataset contains:

- 6 classes
- 4 rooms
- 3 student groups
- 5 available time slots

## Classes

| Class | Students | Professor |
|---|---:|---|
| CS101 | 40 | P1 |
| MATH101 | 35 | P2 |
| CS102 | 30 | P1 |
| HIST101 | 20 | P3 |
| PROG101 | 45 | P4 |
| DB101 | 25 | P5 |

## Rooms

| Room | Capacity |
|---|---:|
| R101 | 50 |
| R102 | 40 |
| R103 | 30 |
| R104 | 20 |

## Student Groups

The input data contains three student groups:

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

Classes belonging to the same student group cannot be scheduled at the
same time.

---

# 4. Stage 1 - Greedy Scheduling

## Algorithm

The Greedy Solver sorts classes by student count in descending order.

Larger classes are considered first because they generally have fewer
available room choices than smaller classes.

For each class, the algorithm checks:

1. Time slots in order.
2. Rooms in their original order.
3. Room capacity.
4. Room conflicts.
5. Professor conflicts.
6. Student group conflicts.

The first feasible room and time-slot combination is selected.

## Why Greedy Was Chosen

A greedy approach provides a fast baseline solution.

It makes a locally feasible choice for each class rather than exploring
all possible complete schedules.

This makes it simple and efficient, but it does not guarantee the
globally optimal room allocation.

The Greedy Solver therefore provides a baseline against which the other
approaches can be compared.

---

# 5. Stage 2 - Conflict Graph

The Conflict Graph represents each class as a vertex.

An edge is created between two classes when they cannot occur at the same
time.

Two classes are considered to conflict when:

- They have the same professor, or
- They share a student group.

For example, if two classes belong to the same student group, an edge is
created between them because the students would otherwise be required
to attend two classes simultaneously.

The graph provides a mathematical representation of the time-slot
constraints.

---

# 6. Stage 3 - Welsh-Powell Graph Coloring

Welsh-Powell graph coloring is applied to the conflict graph.

The algorithm orders classes according to their degree in the graph and
then assigns colors so that connected classes receive different colors.

In this project:

```text
One color represents one time-slot group.
```

Therefore, two conflicting classes cannot receive the same color.

The colors are then converted into actual time slots, such as:

```text
09:00
10:00
11:00
12:00
13:00
```

This creates a conflict-aware assignment of classes to time slots.

---

# 7. Stage 4 - Dynamic Programming Room Optimization

After the graph-based method has assigned time slots, Dynamic Programming
is used to optimize room allocation.

The objective is to minimize the total wasted room capacity while
maintaining a feasible assignment.

For a class assigned to a room:

```text
Wasted capacity = Room capacity - Number of students
```

Only rooms with sufficient capacity are considered.

A room can only be assigned to one class within the same time slot.

## DP State

The Dynamic Programming state represents the current scheduling position
and the rooms that have already been used.

Conceptually, the state can be represented as:

```text
DP(index, used_rooms)
```

where:

- `index` represents the next class requiring a room.
- `used_rooms` represents the rooms already assigned in the current
  time slot.

The value stored by the state represents the minimum possible wasted
capacity for the remaining assignments.

## Recurrence

For every feasible unused room, the algorithm considers the room's
wasted capacity and combines it with the best result for the remaining
classes.

Conceptually:

```text
DP(index, used_rooms)
=
min(
    wasted_capacity
    + DP(index + 1, updated_used_rooms)
)
```

The base case is reached when all classes for the current time slot have
been assigned:

```text
DP(number_of_classes, used_rooms) = 0
```

Previously calculated states can be reused instead of solving the same
subproblem repeatedly.

## Why Dynamic Programming Was Chosen

A straightforward exhaustive approach could repeatedly examine many
possible room allocation combinations.

Dynamic Programming reduces this repeated work by storing results for
already-solved states.

This makes the room-allocation problem more structured and allows the
algorithm to minimize total wasted capacity while respecting room
availability.

---

# 8. Stage 5 - Backtracking

The Backtracking Solver uses recursive search to explore possible class,
room, and time-slot assignments.

For each class, the algorithm:

1. Selects a time slot.
2. Selects a room.
3. Checks room capacity.
4. Checks room conflicts.
5. Checks professor conflicts.
6. Checks student group conflicts.
7. Recursively attempts to schedule the next class.

If an assignment causes a constraint violation, that branch is rejected.

If a later assignment makes the partial schedule impossible, the
algorithm backtracks by removing the previous assignment and trying
another possibility.

## Pruning

The solver prunes invalid branches as soon as a constraint is violated.

Examples include:

```text
Room too small
    ↓
Reject branch

Room already occupied
    ↓
Reject branch

Professor already teaching at that time
    ↓
Reject branch

Student group already has a class at that time
    ↓
Reject branch
```

This prevents the algorithm from continuing to explore branches that
cannot produce a valid schedule.

Backtracking provides a more exhaustive search than the Greedy approach.

---

# 9. Conflict Report

The graph engine produces a conflict report based on the relationships
between classes.

The report identifies conflicts caused by:

- Shared professors
- Shared student groups

This provides a transparent explanation of why certain classes cannot
be placed in the same time slot.

The conflict graph is therefore used not only for coloring but also for
explaining the scheduling constraints.

---

# 10. Algorithm Comparison

The project uses different algorithms because each approach has different
strengths.

| Algorithm | Main Purpose | Main Advantage |
|---|---|---|
| Greedy | Baseline scheduling | Fast and simple |
| Conflict Graph | Represent conflicts | Makes constraints explicit |
| Welsh-Powell | Assign time-slot groups | Conflict-aware coloring |
| Dynamic Programming | Optimize room allocation | Minimizes wasted capacity |
| Backtracking | Search for feasible schedules | Can explore alternative assignments |

The approaches complement each other rather than performing exactly the
same task.

The Greedy Solver provides a baseline.

The Conflict Graph and Welsh-Powell method focus on time-slot conflicts.

Dynamic Programming focuses on room allocation and wasted capacity.

Backtracking provides a more exhaustive search for feasible schedules.

---

# 11. Complexity Analysis

Let:

```text
C = number of classes
R = number of rooms
T = number of time slots
```

## Greedy Solver

The Greedy Solver considers each class, time slot, and room while also
checking the existing schedule for conflicts.

A simplified worst-case time complexity is:

```text
O(C² × T × R)
```

The schedule and unscheduled-class collections require approximately:

```text
O(C)
```

additional space.

---

## Conflict Graph

The graph compares pairs of classes to identify conflicts.

The worst-case time complexity is approximately:

```text
O(C²)
```

The conflict graph can contain an edge between many pairs of classes,
giving a worst-case space complexity of:

```text
O(C²)
```

---

## Welsh-Powell

Welsh-Powell sorts the vertices and examines graph relationships while
assigning colors.

For the implementation used in this project, the worst-case complexity
is approximately:

```text
O(C²)
```

The graph itself requires:

```text
O(C²)
```

space in the worst case.

---

## Dynamic Programming

For a time slot containing `C_s` classes and `R` rooms, the DP state can
include the current class index and a representation of the rooms already
used.

The number of possible room-use states can grow approximately with:

```text
2^R
```

Therefore, an approximate worst-case time complexity is:

```text
O(C_s × R × 2^R)
```

with approximately:

```text
O(C_s × 2^R)
```

DP state storage.

The important advantage is that repeated subproblems are stored and
reused rather than repeatedly recalculated.

---

## Backtracking

Backtracking has exponential worst-case complexity because it may explore
many possible assignments.

A simplified upper bound is:

```text
O((T × R)^C)
```

because each class may potentially be assigned to one of several
time-slot and room combinations.

The recursive call stack requires approximately:

```text
O(C)
```

space, excluding the stored schedule and input structures.

Pruning invalid branches reduces the practical search space.

---

# 12. Testing

The project contains unit tests for the main scheduling components.

The tests cover:

- Greedy scheduling
- Room capacity
- Professor conflicts
- Student group conflicts
- Conflict graph construction
- Welsh-Powell coloring
- Graph-based time-slot assignment
- Dynamic Programming optimization
- Room allocation
- Wasted capacity
- Impossible room assignments
- Backtracking
- Duplicate scheduling prevention

The complete test suite currently contains:

```text
25 tests
```

The latest test result is:

```text
Ran 25 tests

OK

Process finished with exit code 0
```

All tests pass successfully.

---

# 13. Results

The current input dataset contains:

```text
Total classes: 6
```

The scheduling system successfully schedules all six classes with the
current dataset.

The final program reports the number of scheduled and unscheduled classes
for the Greedy, Dynamic Programming, and Backtracking stages.

The Dynamic Programming stage also reports total wasted room capacity.

The program compares:

```text
Greedy total wasted capacity
DP total wasted capacity
Capacity improvement
```

This provides a quantitative comparison of the room-allocation results.

---

# 14. Validation

The generated schedules are checked against the main constraints.

The validation process checks for:

- Room capacity violations
- Room conflicts
- Professor conflicts
- Duplicate class assignments
- Student group conflicts during scheduling

A schedule is considered valid when no validation errors are reported.

The current dataset produces a valid schedule.

---

# 15. Unscheduled Classes

The system supports cases where a class cannot be scheduled.

For example, if a class has more students than the capacity of every
available room, it cannot be assigned a room.

Such a class is placed in the unscheduled collection and reported by the
program.

The system can therefore distinguish between:

```text
Scheduled
```

and:

```text
Unscheduled
```

classes.

The final program also reports the reason for an unscheduled class when
such a case occurs.

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

The following issues were identified and corrected during development.

| Issue | Resolution |
|---|---|
| Backtracking test imported the wrong module name | Updated the test to import `BacktrackingSolver` from `backtracker.py` |
| Greedy room selection was originally selecting the smallest fitting room | Changed the baseline to check rooms in their original order and select the first feasible room |
| Optimizer was initially implemented as a simple room-by-room improvement | Reworked the optimizer as the Dynamic Programming room-optimization component |
| Optimizer was not connected to the main program | Added the optimizer to `main.py` |
| Optimizer required additional validation | Added tests for room capacity, room uniqueness, time slots, impossible assignments, and wasted capacity |
| Project required regression testing | Ran the complete test suite and confirmed that all 25 tests pass |

---

# 18. Design Justification

Each algorithm was selected for a specific role.

## Greedy

Greedy provides a simple and efficient baseline.

Sorting by student count prioritizes classes with fewer room options.

## Conflict Graph

The graph explicitly represents relationships between classes that cannot
share a time slot.

## Welsh-Powell

Welsh-Powell provides a practical graph-coloring method for grouping
non-conflicting classes into time slots.

## Dynamic Programming

Dynamic Programming is used after time slots have been fixed because the
remaining problem is primarily room allocation.

The objective is to minimize wasted capacity without violating room
availability.

## Backtracking

Backtracking provides a more exhaustive search strategy.

It is useful when a simple greedy decision may lead to an undesirable
partial schedule.

---

# 19. Conclusion

This project demonstrates how multiple algorithmic techniques can be
combined to solve a constrained campus scheduling problem.

The Greedy algorithm provides a fast baseline solution.

The Conflict Graph models relationships between classes.

Welsh-Powell coloring converts those conflicts into conflict-aware
time-slot assignments.

Dynamic Programming optimizes room allocation by minimizing wasted room
capacity after time slots have been fixed.

Backtracking provides a recursive search strategy capable of exploring
alternative assignments.

The final project is modular and includes automated tests for the major
algorithmic components.

The current implementation successfully schedules all six classes in the
provided dataset, and the complete test suite passes with 25 successful
tests.