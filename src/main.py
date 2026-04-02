from pathlib import Path
from src.utils.io_handler import load_pickle
from src.constants import ARRANGEMENT_PICKLE, GENERATIONS, PROCESSED_DIR, MARKOV_PICKLE_SUFFIX, MUTATION_RATE, POPULATION_SIZE
import numpy as np
import random

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
        mutation_range = random.randInt(1,4)
        if random.random() < MUTATION_RATE:
            #Ensure that the data value does not go beyond 13
            data_set_genome.append((gene+mutation_range)%13)
        else:
            data_set_genome.append(gene)
    return data_set_genome


def tournament(participants):
    if len(participants) < 2:
        return [None, None]

    total_fitness = sum([participant.fitness for participant in participants])

    if total_fitness <= 0:
        return [None, None]

    fitnesses = [participant.fitness/total_fitness for participant in participants]

    return np.random.choice(participants, size=2, replace=False, p=fitnesses)


population = load_pickle(PROCESSED_DIR/ARRANGEMENT_PICKLE)
markov = load_pickle(PROCESSED_DIR / f"order2_{MARKOV_PICKLE_SUFFIX}")

for i in range(GENERATIONS):
    new_population = []
    rejects = []

    # We need to call the eval fitness function to calculate
    # the fitness functions for all the members
    for individual in population:
        individual.evaluate_fitness([markov])


    total_fitness = sum([population.fitness for population in population])
    print(f"Total fitness {total_fitness}")

    # Select parents to crossover / mutate tournament style
    # trying groups of 8 at first

    random.shuffle(population)
    for j in range(0, len(population), 8):
        competitors = population[j:j+8]
        parent1, parent2 = tournament(competitors)

        if parent1 is None or parent2 is None:
            continue

        new_population.append(parent1)
        new_population.append(parent2)

        # children = crossover(parent1, parent2)
        # new_population.extend(children)

        competitors.remove(parent1)
        competitors.remove(parent2)
        rejects.extend(competitors)

    new_population.extend(rejects[:POPULATION_SIZE-len(new_population)])
    population = new_population
    print(f"Generation {i}")
