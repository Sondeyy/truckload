import numpy as np


def calculate_population_fitness(w, p):
    # w: equation input
    # p: population (independant variable)
    # Calculating the fitness value of each Individuum in the current population.
    # axis=1 sums over each population
    fitness = np.sum(np.sin(w * p), axis=1)
    return fitness


def select_mating_pool(p, fitness, mates):
    # Wähle die besten Individuen der aktuellen Generation als Eltern für die nächste Generation

    newparents = np.empty((mates, p.shape[1]))

    for m in range(mates):
        # Wo ist Fitness maximal?
        max_fitness_index = np.argmax(fitness == np.max(fitness))
        newparents[m, :] = p[max_fitness_index, :]
        fitness[max_fitness_index] = -99999999999
    return newparents


def crossover(parents, print_results):
    offspring_size = parents.shape
    offspring = np.empty(offspring_size)

    for k in range(0, offspring_size[0], 2):
        # würfel crossover point aus\n"
        crossover_point = np.random.randint(1, offspring_size[1] - 2)
        if print_results:
            print('Eltern', k, ' und', k + 1, " - Crossover_point: ", crossover_point)

        # Index of the first parent to mate.
        parent1_index = k
        # Index of the second parent to mate.
        parent2_index = (k + 1)

        # The new offspring will have its first part of its genes taken from the first parent.
        offspring[k, 0:crossover_point] = parents[parent1_index, 0:crossover_point]
        # The new offspring will have its last part of its genes taken from the second parent.
        offspring[k, crossover_point:] = parents[parent2_index, crossover_point:]

        # The new offspring will have its first part of its genes taken from the first parent.
        offspring[k + 1, 0:crossover_point] = parents[parent2_index, 0:crossover_point]
        # The new offspring will have its last part of its genes taken from the second parent.
        offspring[k + 1, crossover_point:] = parents[parent1_index, crossover_point:]

    return offspring


def mutation(offspring_crossover, inc, print_results):
    # ort (index) o, an dem Mutation stattfinden wird
    # o = 0

    # Mutation changes a single gene in each offspring randomly.
    for idx in range(offspring_crossover.shape[0]):
        o = np.random.randint(0, offspring_crossover.shape[1])
        # The random value to be added to the gene.
        random_value = np.random.uniform(-1.0 * inc, inc)
        if print_results:
            print('Ort der Mutation: ', o, 'Mutationsgröße: ', random_value)

        offspring_crossover[idx, o] = offspring_crossover[idx, o] + random_value
    return offspring_crossover
