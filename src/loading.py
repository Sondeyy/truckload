import random
from dataclasses import dataclass

from truck import Route


@dataclass
class Loading:
    """
    This class represents a configuration of routes and the assignments, which should be fulfilled with the routes.
    """
    routes: list[Route]
    reward: int = 0

    def __str__(self):
        string = ""
        for route in self.routes:
            string += f"{str(route)}\n"
        string += f" --> Reward: {str(self.reward)} €"
        return string

    def __getitem__(self, item):
        for route in self.routes:
            if route.truck.truck_number == item:
                return route

    @classmethod
    def get_random_loading(cls, trucks, assignments):
        """
        returns a random loading

        :param trucks: available trucks
        :param assignments: assignments to do
        :return: random loading
        """
        routes = []

        for truck in trucks:
            # pick a random number of random assignments for each truck and remove those that can't be done
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

        each one stays valid!

        :param loading1: individual 1
        :param loading2: individual 2
        :return: crossed loadings
        """
        for loading, other_loading in zip((loading1, loading2), (loading2, loading1)):
            for route in loading.routes:
                if route.assignments:
                    continue

                # if one route/truck has no assignments at all:
                # look in the other loading which values are possible
                # switch possible values from their original location to the empty root

                possible_assignments = [a for a in other_loading[route.truck.truck_number].assignments]
                possible_assignments_numbers = [a.number for a in possible_assignments]

                if not possible_assignments:
                    continue

                # remove assignments elsewhere
                for r in loading.routes:
                    r.assignments = [a for a in r.assignments if not a.number in possible_assignments_numbers]

                # add assignments here
                route.assignments.extend(possible_assignments)

        return loading1, loading2

    @staticmethod
    def mutate(loading):
        """
        changes a single loading randomly

        1. the loadings per route get shuffled
        2. try to switch one random assignment of each route with another random assignment from another route

        :param loading: loading to mutate
        :return: mutated loading
        """

        for route in loading.routes:

            # shuffle assignments to change bonus/penalty chances
            random.shuffle(route.assignments)

            # if possible, switch one assignment to another truck
            if not len(route.assignments):
                continue

            assignment = route.assignments[0]

            random_route = random.choice(loading.routes)
            random_truck = random_route.truck

            if assignment.boxes_expected < random_truck.maximum_boxes and \
                    assignment.boxes_expected * assignment.box_weight < random_truck.maximum_payload:
                # assignment gets taken by another truck
                random_route.assignments.append(assignment)
                # original truck doesn't have to do it anymore
                route.assignments = route.assignments[1:]

        return loading

    def is_valid(self):
        """
        only checks if one assignment appears twice
        :return:
        """
        all_assignments = []
        for route in self.routes:
            for assignment in route.assignments:
                if assignment.number in all_assignments:
                    print(assignment.number)
                    return False
                all_assignments.append(assignment.number)
        return True

    def evaluate(self):
        """
        Evaluates the loading in aspect to money.

        :return: how much money this Loading will generate
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

        self.reward = money

        return (money,)
