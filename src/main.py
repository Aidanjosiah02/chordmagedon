import statistics
import copy
from src.objects.Chord import Chord
from src.utils.io_handler import load_pickle
from src.constants import ARRANGEMENT_PICKLE, GENERATIONS, PROCESSED_DIR, MARKOV_PICKLE_SUFFIX, MUTATION_RATE, POPULATION_SIZE, NOTE_MAP, OCTAVE_NOTE_COUNT, NOTE_MAP, ALLOWED_PAIRS_OF_QUALITY_AND_SEVENTH_TYPE
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
transposition_factor = -NOTE_MAP.get(key, 0)

if key is None:
    print("No key Selected")
    exit()


chordsInput = ChordsInput()
raw_input = chordsInput.run()
chords_list = [item.strip() for item in raw_input.split(',')]
spaced_chords = " ".join(chords_list)
chordList: Arrangement = parse_arrangements([spaced_chords])[0]


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


def mutate(parent: Arrangement, mutation_rate: float = MUTATION_RATE):
    mutated_chords = []
    mutated_notes = []

    for chord, note in zip(parent.progression.chords, parent.bassline.notes):

        step = random.choice([-2, -1, 1, 2])

        if chord is not None and random.random() < mutation_rate:

            new_root = (chord.root + step) % OCTAVE_NOTE_COUNT

            new_quality, new_seventh = random.choice(
                ALLOWED_PAIRS_OF_QUALITY_AND_SEVENTH_TYPE)

            mutated_chords.append(
                Chord(
                    root=new_root,
                    quality=new_quality,
                    seventhType=new_seventh,
                    remainders=set()
                )
            )
        else:
            mutated_chords.append(chord)

        if note is not None and random.random() < mutation_rate:

            bass_step = random.choice([-1, 1, 2])

            mutated_notes.append((note + bass_step) % OCTAVE_NOTE_COUNT)
        else:
            mutated_notes.append(note)

    return Arrangement(
        progression=ChordProgression(chords=mutated_chords),
        bassline=BassLine(notes=mutated_notes)
    )


def tournament(participants):
    if len(participants) < 2:
        return [None, None]
    winners = sorted(participants, key=lambda x: x.fitness, reverse=True)
    return winners[0], winners[1]


population: list[Arrangement] = load_pickle(PROCESSED_DIR/ARRANGEMENT_PICKLE)

# Append the new chords to the population
for item in population:
    item.progression.chords = chordList.progression.get_chords() + \
        item.progression.get_chords()
    item.bassline.notes = chordList.bassline.get_notes() + item.bassline.get_notes()
    item.transpose(transposition_factor)


markov = load_pickle(PROCESSED_DIR / f"order2_{MARKOV_PICKLE_SUFFIX}")

for i in range(GENERATIONS):
    for individual in population:
        individual.evaluate_fitness([markov])

    current_fitnesses = [p.fitness for p in population]
    median_fitness = statistics.median(current_fitnesses)
    highest_fitness = max(current_fitnesses)

    print(f"Generation {i}")
    print(f"Median fitness {median_fitness}")
    print(f"Highest fitness {highest_fitness}")

    best_overall = max(population, key=lambda p: p.fitness)
    new_population = [copy.deepcopy(best_overall)]

    random.shuffle(population)
    rejects = []

    for j in range(0, len(population), 8):
        if len(new_population) >= POPULATION_SIZE:
            break
        competitors = population[j:j+8]
        parent1, parent2 = tournament(competitors)

        if parent1 is None or parent2 is None:
            continue

        children = uniform_crossover(parent1, parent2)
        for child in children:
            if len(new_population) < POPULATION_SIZE:
                new_population.append(mutate(child))

        losers = [c for c in competitors if c not in (parent1, parent2)]
        rejects.extend(losers)

    if len(new_population) < POPULATION_SIZE:
        fill_count = POPULATION_SIZE - len(new_population)
        new_population.extend(rejects[:fill_count])

    population = new_population
