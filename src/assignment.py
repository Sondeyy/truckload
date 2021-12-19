from dataclasses import dataclass


@dataclass
class Assignment:
    """
    This class represents an assignment.
    """
    number: int
    target: str
    driving_time: int
    boxes_expected: int
    box_weight: int
    bonus_time: int
    bonus_value: int
    reward: int
    penalty_time: int
    penalty_value: int

    def __str__(self):
        return str(self.number)
