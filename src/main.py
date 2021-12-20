import random
from csv import reader

import numpy as np
from deap import base, creator, tools

from src.assignment import Assignment
from src.loading import Loading
from src.truck import Truck


def print_fitness(fits, description="") -> None:
    """
    Print common statistical values of a fitness list.

    :param fits: fitness list
    :param description: additional description, e.g 'after'
    """
    length = len(fits)
    mean = sum(fits) / length
    sum2 = sum(x * x for x in fits)
    std = abs(sum2 / length - mean ** 2) ** 0.5

    print(description)
    print("  Min %s" % min(fits))
    print("  Max %s" % max(fits))
    print("  Avg %s" % mean)
    print("  Std %s" % std)

    print("")


def read_from_csv(truck_file: str, assignment_file: str) -> (list[Truck], list[Assignment]):
    """
    reads given csv files and returns trucks and assignment objects

    if no penalty or bonus is given, the vales are set to 0

    :param truck_file: path of truck file
    :param assignment_file: path of assignment file
    :return: trucks and assignments in lists as a tuple
    """
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

    return trucks, assignments


def main():
    truck_file = "../data/Evo11/Evo11_LKW.csv"
    assignment_file = "../data/Evo11/Evo11_Auftraege.csv"

    trucks, assignments = read_from_csv(truck_file, assignment_file)

    # random.seed(42)

    # create custom types
    creator.create("Fitness", base.Fitness, weights=(1.0,))
    creator.create("Individual", Loading, fitness=creator.Fitness)

    # register functions in toolbox
    toolbox = base.Toolbox()
    toolbox.register("individual", creator.Individual.get_random_loading, trucks, assignments)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("mate", Loading.crossover)
    toolbox.register("mutate", Loading.mutate)
    toolbox.register("select", tools.selBest)
    toolbox.register("evaluate", creator.Individual.evaluate)

    # create first population
    pop = toolbox.population(n=100)

    # register hall of fame
    # the 3 best individuals of all generations will be gathered here
    hof = tools.HallOfFame(3)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)

    # probabilities
    # crossover between 0.8 and 0.95
    # mutation between 0.001 and 0.05
    # see Xin-She Yang, ... Tiew On Ting, in Bio-Inspired Computation in Telecommunications, 2015
    crossover_probability, mutation_probability, generations = 0.8, 0.001, 50

    # Evaluate the entire population
    fitnesses = map(toolbox.evaluate, pop)
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    fits = [ind.fitness.values[0] for ind in pop]

    print_fitness(fits, "before")

    hof.update(pop)

    for generation in range(generations):
        # print(f"{generation=}  Fitness={max([ind.fitness.values[0] for ind in pop])}")

        # Select the next generation individuals
        offspring = toolbox.select(pop, 80)
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))

        # append random ones
        offspring.extend(toolbox.population(20))

        # Apply crossover and mutation on the offspring
        changed = []

        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < crossover_probability:
                changed.append(toolbox.clone(child1))
                changed.append(toolbox.clone(child2))
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < mutation_probability:
                changed.append(toolbox.clone(mutant))
                toolbox.mutate(mutant)
                del mutant.fitness.values

        offspring.extend(changed)

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        hof.update(offspring)

        # The population is entirely replaced by the offspring
        pop[:] = offspring

    # Gather all the fitnesses in one list and print the stats
    fits = [ind.fitness.values[0] for ind in pop]

    print_fitness(fits, "after")

    # print hall of fame
    print("--- HALL OF FAME ---")
    print("\n\n".join(map(str, hof)))


if __name__ == '__main__':
    main()
