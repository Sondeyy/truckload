from dataclasses import dataclass


@dataclass
class Assignment:
    assignment_number: int
    target: str
    driving_time: int
    boxes: int
    box_weight: int
    bonus_time: int
    bonus_value: int
    reward: int
    penalty_time: int
    penalty_value: int
