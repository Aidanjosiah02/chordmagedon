from pathlib import Path

from src.utils.io_handler import load_pickle
from src.constants import ARRANGEMENT_PICKLE, GENERATIONS
import numpy as np
import random

GENERATIONS = 1000
POPULATION_SIZE = 95000
MUTATION_RATE = 0.05

#Uniform crossover
def crossover(parentA, parentB):
    #Child that we are returning later
    #Array we are storing our 6 children in? Idk ask Marvellous
    children = []
    for i in range (6):
        
        child_genome = []

        for a,b in zip(parentA, parentB):
            #"Coin flip" to decide crossover
            if random.random() < 0.5:
                child_genome.append(a)
            else:
                child_genome.append(b)
    children.append(child_genome)
    return children

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
    fitnesses = [participant.fitness for participant in participants]
    return np.random.choice(participants, size=2, replace=False, p=fitnesses)


population = load_pickle(Path(ARRANGEMENT_PICKLE))

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
