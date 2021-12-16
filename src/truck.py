from dataclasses import dataclass


@dataclass
class Truck:
    """
    This class represents a single truck and its specifications.
    """
    truck_number: int
    maximum_boxes: int
    maximum_payload: int


@dataclass
class TruckState:
    """
    This class represents the state of a truck at a given time.
    """
    truck: Truck
    loaded_boxes: int
    previously_loaded_boxes: int
    loaded_boxes: list[int]
    previously_loaded_boxes: list[int]
    current_position: chr
    target: chr
    time_on_the_road: int


@dataclass
class Route:
    """
    This class represents the rout one truck will drive. Routes consist of states.
    """
    truck: Truck
    states: list[TruckState]
