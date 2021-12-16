from dataclasses import dataclass
import random

import numpy as np

from src.assignment import Assignment
from src.truck import Route


@dataclass
class Loading:
    """
    This class represents a configuration of routes and the assignments, which should be fulfilled with the routes.
    """
    routes: list[Route]
    assignments: list[Assignment]

    @classmethod
    def get_random_loading(cls, trucks, assignments):
        routes = []

        for truck in trucks:
            picked_assignments = random.sample(assignments, random.randint(0, len(assignments)))
            assignments = [a for a in assignments if a not in picked_assignments]

            routes.append(Route(truck, picked_assignments))

        return cls(
            routes=routes,
            assignments=assignments
        )

    def is_valid(self) -> bool:
        """
        Check if the loading is valid.
        :return: true if the loading is valid, false otherwise.
        :rtype: bool
        """

        # TODO
        pass

    def evaluate(self) -> int:
        """
        Evaluates the loading in aspect to money.

        :return: how much money this Loading will generate
        :rtype: int
        """
        money = 0

        for route in self.routes:
            for assignment in route.assignments:

                route.time_so_far += assignment.driving_time

                if route.time_so_far < assignment.bonus_time:
                    money += assignment.bonus_value
                elif route.time_so_far > assignment.penalty_time:
                    money -= assignment.penalty_value
                money += assignment.reward

                route.time_so_far += assignment.driving_time

        return money
