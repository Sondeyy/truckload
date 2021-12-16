import sys
from dataclasses import dataclass
import random

from src.truck import Route


@dataclass
class Loading:
    """
    This class represents a configuration of routes and the assignments, which should be fulfilled with the routes.
    """
    routes: list[Route]
    reward: int = 0

    # def __len__(self):
    #     return 1

    @classmethod
    def get_random_loading(cls, trucks, assignments):
        routes = []

        for truck in trucks:
            picked_assignments = random.sample(assignments, random.randint(0, len(assignments)))
            picked_assignments = [pa for pa in picked_assignments if pa.boxes_expected < truck.maximum_boxes]
            picked_assignments = [pa for pa in picked_assignments if
                                  pa.boxes_expected * pa.box_weight < truck.maximum_payload]
            assignments = [a for a in assignments if a not in picked_assignments]

            routes.append(Route(truck, picked_assignments))

        return cls(
            routes=routes,
        )

    @staticmethod
    def crossover(loading1, loading2):
        """
        Crossover interchanges values of two loadings.

        :param loading1:
        :param loading2:
        :return:
        """
        # TODO combine and cross, but keep valid states

        return loading1, loading2

    @staticmethod
    def mutate(loading):
        """

        :param loading: loading to mutate
        :return: crossed loading
        """
        # TODO mutate, but keep valid state

        return loading

    def evaluate(self):
        """
        Evaluates the loading in aspect to money.

        :return: how much money this Loading will generate
        """
        money = 0

        for route in self.routes:
            for assignment in route.assignments:

                if route.truck.maximum_payload < assignment.box_weight * assignment.boxes_expected:
                    self.reward = -1
                    return (-1,)

                if route.truck.maximum_boxes < assignment.boxes_expected:
                    self.reward = -1
                    return (-1,)

                route.time_so_far += assignment.driving_time

                if route.time_so_far < assignment.bonus_time:
                    money += assignment.bonus_value
                elif route.time_so_far > assignment.penalty_time:
                    money -= assignment.penalty_value
                money += assignment.reward

                route.time_so_far += assignment.driving_time
        self.reward = money
        return (money,)
