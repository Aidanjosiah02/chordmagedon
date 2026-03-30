from src.utils.io_handler import load_arrangements
from src.constants import PICKLE
import numpy
import random

GENERATIONS = 1000
POPULATION_SIZE = 95000


def crossover():
    pass


def mutate():
    pass


def tournament(participants):
    fitnesses = [participant.fitness for participant in participants]
    return np.random.choice(participants, size=2, replace=False, p=fitnesses)


population = load_arrangements(PICKLE)

for i in range(GENERATIONS):
    new_population = []
    rejects = []
    # We need to call the eval fitness function to calculate
    # the fitness functions for all the members
    for individual in population:
        individual.evaluate_fitness()

    # Select parents to crossover / mutate tournament style
    # trying groups of 8 at first
    while len(population) > 8:
        competitors = random.sample(population) 
        parent1, parent2 = tournament(competitors)
        new_population.append(parent1)
        new_population.append(parent2)
        # remove the competitors from the population
        [population.remove(item) for item in competitors]
        competitors.remove(parent1)
        competitors.remove(parent2)
        rejects.extend(competitors)
        print('hi')

    population = new_population
