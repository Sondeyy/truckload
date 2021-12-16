import random
from dataclasses import dataclass

from src.assignment import Assignment


@dataclass
class Truck:
    """
    This class represents a single truck and its specifications.
    """
    truck_number: int
    maximum_boxes: int
    maximum_payload: int


@dataclass
class Route:
    """
    This class represents the route one truck will drive. Routes consist of one or more single trips.
    """
    truck: Truck
    assignments: list[Assignment]

    time_so_far: int = 0
