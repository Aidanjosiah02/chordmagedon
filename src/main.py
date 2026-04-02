from src.utils.io_handler import load_arrangements
from src.constants import PICKLE
import random
<<<<<<< Updated upstream
import numpy
=======
import mido
#CODY TODO: LOOK INTO MIDO FOR MIDI OUTPUT - WOULD BE COOL
>>>>>>> Stashed changes

GENERATIONS = 1000
POPULATION_SIZE = 95000
MUTATION_RATE = 0.05

#Uniform crossover
def crossover(parentA, parentB):
    #Child that we are returning later
    child_genome = []

<<<<<<< Updated upstream
    for a,b in zip(parentA, parentB):
        #"Coin flip" to decide crossover
        if random.random() < 0.5:
            child_genome.append(a)
        else:
            child_genome.append(b)
            
    return child_genome
=======
        for a,b in zip(parentA, parentB):
            #"Coin flip" to decide crossover
            if random.random() < 0.5:
                child_genome.append(a)
            else:
                child_genome.append(b)
        children.append(child_genome)
    return children
>>>>>>> Stashed changes

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

def export_midi():
    #create file
    file = mido.MidiFile('song.mid', type=1)
    chord_track = MidiTrack()
    bass_track = MidiTrack()

    file.tracks.append(chord_track)
    file.tracks.append(bass_track)

    #specs of output - Default as of now
    ticks_per_beat = 480
    velocity = 64

    #data - Put in when finished
    chordprog = []

    bassline = []
    
    #put data inside of the file - for msg in MidiFile? Look back later
    chord_track.append(Message('note_on', note=64, velocity=64, time=32))

    bass_track.append(Message('note_on', note=64, velocity=64, time=32))

    #save file
    mid.save('song.mid')
    print("Song finished!")


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
