from src.utils.io_handler import load_arrangements
from src.constants import PICKLE
import random
import numpy

GENERATIONS = 1000
POPULATION_SIZE = 95000
MUTATION_RATE = 0.05

#Uniform crossover
def crossover(parentA, parentB):
    #Child that we are returning later
    child_genome = []

    for a,b in zip(parentA, parentB):
        #"Coin flip" to decide crossover
        if random.random() < 0.5:
            child_genome.append(a)
        else:
            child_genome.append(b)
            
    return child_genome

def mutate(genome):
    data_set_genome = []

    #Select a random point and alter it
    for gene in genome:
        if random.random() < MUTATION_RATE:
            data_set_genome.append(gene+1)
        else:
            data_set_genome.append(gene)
    return data_set_genome


def tournament(participants):
    pass


population = load_arrangements(PICKLE)

for i in range(GENERATIONS):
    # We need to call the eval fitness function to calculate
    # the fitness functions for all the members
    for individual in population:
        individual.evaluate_fitness()

    # Select parents to crossover / mutate tournament style

    # Crossover the parents

    # Mutate the child with a probability

    # Add mutated child to the new population
