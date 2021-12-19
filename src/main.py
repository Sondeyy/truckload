import random
from csv import reader

import numpy as np
from deap import base, creator, tools

from src.assignment import Assignment
from src.loading import Loading
from src.truck import Truck


def print_fitness(fits, description=""):
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

    # random.seed(42)

    creator.create("FitnessMin", base.Fitness, weights=(1.0,))
    creator.create("Individual", Loading, fitness=creator.FitnessMin)

    toolbox = base.Toolbox()
    toolbox.register("individual", creator.Individual.get_random_loading, trucks, assignments)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("mate", Loading.crossover)
    toolbox.register("mutate", Loading.mutate)
    toolbox.register("select", tools.selBest)
    toolbox.register("evaluate", creator.Individual.evaluate)

    pop = toolbox.population(n=50)

    hof = tools.HallOfFame(3)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)

    crossover_probability, mutation_probability, generations = 0.5, 0.2, 20

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
        offspring = toolbox.select(pop, 10)
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))

        # append random ones
        offspring.extend(toolbox.population(40))

        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < crossover_probability:
                continue
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < mutation_probability:
                continue
                toolbox.mutate(mutant)
                del mutant.fitness.values

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

    print("--- HALL OF FAME ---")
    print("\n\n".join(map(str, hof)))


if __name__ == '__main__':
    main()
