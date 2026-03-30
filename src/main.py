from src.utils.io_handler import load_arrangements
from src.constants import PICKLE
import random
import numpy

GENERATIONS = 1000
POPULATION_SIZE = 95000

#Uniform crossover - FINISH LATER
#Give 6 children in return
def crossover(parentA, parentB):
    #Child that we are returning later
    child_genome = []

    for a,b in zip(parentA, parentB):
        #"Coin flip" to decide crossover
        #0 - Grab from A, 1 - Grab from B
        RAND_NUMBER = random.randint(0, 1)
        if(RAND_NUMBER == 0):
            child_genome.append(a)
        else:
            child_genome.append(b)
            
    return child_genome

#FINISH LATER
#Give 6 children in return
def mutate():
    data_set = load_arrangements(PICKLE)
    data_set_genome = []
    MUTATION_RATE = 0.05

    #Select a random point and alter it
    for i, a in zip(data_set):
        rand_number = random.random()
        if(MUTATION_RATE > rand_number):
            data_set_genome.append(a)
            data_set_genome[i] += 1
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
