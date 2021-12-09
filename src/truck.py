from dataclasses import dataclass


@dataclass
class Truck:
    truck_number: int
    maximum_boxes: int
    maximum_payload: int
