from dataclasses import dataclass

from src.assignment import Assignment
from src.truck import Route


@dataclass
class Loading:
    """
    This class represents a configuration of routes and the assignments, which should be fulfilled with the routes.
    """
    routes: list[Route]
    assignments: list[Assignment]

    def is_valid(self) -> bool:
        """
        Check if the loading is valid.
        :return: true if the loading is valid, false otherwise.
        :rtype: bool
        """

        # TODO
        pass

    def evaluate_loading(self) -> int:
        """
        Evaluates the loading in aspect to money.

        :return: how much money this Loading will generate
        :rtype: int
        """
        money = 0
        for route in self.routes:
            for state in route.states[1:-1]:
                for assignment in self.assignments:
                    if assignment.target == state.current_position:
                        assignment.boxes_so_far += state.previously_loaded_boxes - state.loaded_boxes

                        if assignment.boxes_so_far == assignment.boxes_expected:
                            if state.time_on_the_road < assignment.bonus_time:
                                money += assignment.bonus_value
                            if state.time_on_the_road > assignment.penalty_time:
                                money -= assignment.penalty_value
                            money += assignment.reward
        return money
