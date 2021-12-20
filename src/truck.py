from dataclasses import dataclass

from assignment import Assignment


@dataclass
class Truck:
    """
    This class represents a single truck and its specifications.
    """
    truck_number: int
    maximum_boxes: int
    maximum_payload: int

    def __str__(self):
        return str(self.truck_number)


@dataclass
class Route:
    """
    This class represents the route one truck will drive. Routes consist of one or more single trips.
    """
    truck: Truck
    assignments: list[Assignment]

    time_so_far: int = 0

    def __str__(self):
        assignment_strs = " ".join(map(str, self.assignments))
        return f"Truck: {str(self.truck)}   Assignments: {assignment_strs}"
