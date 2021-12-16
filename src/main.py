import random
from csv import reader
import numpy as np
from deap import base, creator, tools, algorithms

from src.loading import Loading
from src.assignment import Assignment
from src.truck import Truck, Route


def main():
    truck_file = "../data/Evo11/Evo11_LKW.csv"
    assignment_file = "../data/Evo11/Evo11_Auftraege.csv"

    trucks = []
    with open(truck_file) as f:
        rows = reader(f, delimiter=";")
        next(rows)
        for truck in rows:
            trucks.append(Truck(
                truck_number=int(truck[0]),
                maximum_boxes=int(truck[1]),
                maximum_payload=int(truck[2])
            ))

    assignments = []
    with open(assignment_file) as f:
        rows = reader(f, delimiter=";")
        next(rows)
        for assignment in rows:
            assignments.append(Assignment(
                number=int(assignment[0]),
                target=str(assignment[1]).strip(),
                driving_time=int(assignment[2]),
                boxes_expected=int(assignment[3]),
                box_weight=int(assignment[4]) if len(assignment[4]) > 0 and not assignment[4].isspace() else 0,
                bonus_time=int(assignment[5]) if len(assignment[5]) > 0 and not assignment[5].isspace() else 0,
                bonus_value=int(assignment[6]),
                reward=int(assignment[7]),
                penalty_time=int(assignment[8]) if len(assignment[8]) > 0 and not assignment[8].isspace() else 0,
                penalty_value=int(assignment[9]) if len(assignment[9]) > 0 and not assignment[9].isspace() else 0,
            ))

    # creator.create("FitnessMin", base.Fitness)
    # creator.create("Individual", Loading, fitness=creator.FitnessMin)
    #
    # IND_SIZE = 10
    #
    # toolbox = base.Toolbox()
    # toolbox.register("attribute", random.random)
    # toolbox.register("individual", tools.initRepeat, creator.Individual,
    #                  toolbox.attribute, n=IND_SIZE)
    # toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    #
    # toolbox.register("mate", tools.cxTwoPoint)
    # toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.1)
    # toolbox.register("select", tools.selTournament, tournsize=3)
    # toolbox.register("evaluate", toolbox.individual.evaluate)
    #
    # pop = toolbox.population(n=50)
    # CXPB, MUTPB, NGEN = 0.5, 0.2, 40
    #
    # # Evaluate the entire population
    # fitnesses = map(toolbox.evaluate, pop)
    # for ind, fit in zip(pop, fitnesses):
    #     ind.fitness.values = fit
    #
    # for g in range(NGEN):
    #     # Select the next generation individuals
    #     offspring = toolbox.select(pop, len(pop))
    #     # Clone the selected individuals
    #     offspring = list(map(toolbox.clone, offspring))
    #
    #     # Apply crossover and mutation on the offspring
    #     for child1, child2 in zip(offspring[::2], offspring[1::2]):
    #         if random.random() < CXPB:
    #             toolbox.mate(child1, child2)
    #             del child1.fitness.values
    #             del child2.fitness.values
    #
    #     for mutant in offspring:
    #         if random.random() < MUTPB:
    #             toolbox.mutate(mutant)
    #             del mutant.fitness.values
    #
    #     # Evaluate the individuals with an invalid fitness
    #     invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
    #     fitnesses = map(toolbox.evaluate, invalid_ind)
    #     for ind, fit in zip(invalid_ind, fitnesses):
    #         ind.fitness.values = fit
    #
    #     # The population is entirely replaced by the offspring
    #     pop[:] = offspring
    #
    #     print(pop)

    loading = Loading.get_random_loading(trucks, assignments)

    print(loading.evaluate())


if __name__ == '__main__':
    main()
