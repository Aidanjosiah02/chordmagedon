from src.utils.io_handler import load_arrangements
from src.constants import PICKLE

GENERATIONS = 1000
POPULATION_SIZE = 10


def crossover():
    pass


def mutate():
    pass


population = load_arrangements(PICKLE)

for i in range(GENERATIONS):
    # We need to call the eval fitness function to calculate the fitness functions for all the members
    for individual in population:
        individual.evaluate_fitness()

    # Select parents to crossover / mutate tournament style

    # Crossover the parents

    # Mutate the child with a probability

    # Add mutated child to the new population
