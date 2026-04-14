import statistics
from src.objects.Chord import Chord
from src.utils.io_handler import load_pickle
from src.constants import ARRANGEMENT_PICKLE, GENERATIONS, PROCESSED_DIR, MARKOV_PICKLE_SUFFIX, MUTATION_RATE, POPULATION_SIZE, NOTE_MAP
import numpy as np
import random
from src.objects.Arrangement import Arrangement
from src.objects.ChordProgression import ChordProgression
from src.objects.Bassline import BassLine
from src.widgets.CompositionKeySelection import CompositionKeySelection
from src.widgets.ChordsInput import ChordsInput
from src.utils.parser import parse_arrangements
keySelection = CompositionKeySelection()
key = keySelection.run()

if key is None:
    print("No key Selected")
    exit()


chordsInput = ChordsInput()
raw_input = chordsInput.run()
chords_list = [item.strip() for item in raw_input.split(',')]
spaced_chords = " ".join(chords_list)
chordList: Arrangement = parse_arrangements([spaced_chords])[0]

print(chordList)

# Please compare


def single_crossover(parent_a: Arrangement, parent_b: Arrangement) -> Arrangement:
    # Single-point crossover: take half from A, half from B
    point = random.randint(1, 7)
    a_chords = parent_a.get_progression().get_chords()
    b_chords = parent_b.get_progression().get_chords()
    child_chords: list[Chord] = a_chords[:point] + b_chords[point:]
    a_bass = parent_a.get_bassline().get_notes()
    b_bass = parent_b.get_bassline().get_notes()
    child_bass: list[int] = a_bass[:point] + b_bass[point:]
    return Arrangement(ChordProgression(child_chords), BassLine(child_bass))

# Uniform crossover


def uniform_crossover(parentA: Arrangement, parentB: Arrangement):
    # Child that we are returning later
    children = []
    for i in range(6):

        progression = []
        bassline = []

        counter = 0
        for a, b in zip(parentA.progression.chords, parentB.progression.chords):

            # "Coin flip" to decide crossover
            if a is not None:
                progression.append(b)
                bassline.append(parentB.bassline.notes[counter])
            elif b is not None:
                progression.append(a)
                bassline.append(parentA.bassline.notes[counter])
            elif random.random() < 0.5:
                progression.append(a)
                bassline.append(parentA.bassline.notes[counter])
            else:
                progression.append(b)
                bassline.append(parentB.bassline.notes[counter])

        child_arrangement = Arrangement(progression=ChordProgression(
            chords=progression), bassline=BassLine(notes=bassline))
        children.append(child_arrangement)

        counter += 1
    return children


def mutate(parent: Arrangement):
    # Where we are putting mutations in before return - Progression and bass notes
    mutated_chords = []
    mutated_notes = []

    for chord, note in zip(parent.progression.chords, parent.bassline.notes):
        mutation_range = random.randint(1, 4)
        # Chord stuff
        if random.random() < MUTATION_RATE:
            if chord is not None:
                # Ensuring it does not go past valid value
                mutated_chord = Chord(
                    notes=[(n + mutation_range) % 13 for n in chord.notes])
                mutated_chords.append(mutated_chord)
            else:
                mutated_chords.append(None)
        else:
            mutated_chords.append(chord)

        # Bass stuff
        if random.random() < MUTATION_RATE:
            if note is not None:
                # Ensuring it does not go past valid value
                mutated_notes.append((note + mutation_range) % 13)
            else:
                mutated_notes.append(None)
        else:
            mutated_notes.append(note)

    mutated_arrangement = Arrangement(progression=ChordProgression(
        chords=mutated_chords), bassline=BassLine(notes=mutated_notes))
    return mutated_arrangement


def tournament(participants):
    if len(participants) < 2:
        return [None, None]
    winners = sorted(participants, key=lambda x: x.fitness, reverse=True)
    return winners[0], winners[1]


population: Arrangement = load_pickle(PROCESSED_DIR/ARRANGEMENT_PICKLE)

# Append the new chords to the population
for item in population:
    item.progression.chords = chordList.progression.get_chords() + \
        item.progression.get_chords()
    item.bassline.notes = chordList.bassline.get_notes() + item.bassline.get_notes()


markov = load_pickle(PROCESSED_DIR / f"order2_{MARKOV_PICKLE_SUFFIX}")

for i in range(GENERATIONS):
    new_population = []
    rejects = []

    # We need to call the eval fitness function to calculate
    # the fitness functions for all the members
    for individual in population:
        individual.evaluate_fitness([markov])

    median_fitness = statistics.median(
        [population.fitness for population in population])
    highest_fitness = max([population.fitness for population in population])
    print(f"Median fitness {median_fitness}")
    print(f"Highest fitness {highest_fitness}")
    best = max(population, key=lambda p: p.fitness)
    print(best)

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

        children = uniform_crossover(parent1, parent2)
        # children = [mutate(child) if random.random() <
        #             0.95 else child for child in children]
        new_population.extend(children)

        competitors.remove(parent1)
        competitors.remove(parent2)
        rejects.extend(competitors)

    new_population.extend(rejects[:POPULATION_SIZE-len(new_population)])
    population = new_population
    print(f"Generation {i}")
