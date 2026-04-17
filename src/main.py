import statistics
import copy
import numpy as np
import random

from src.objects.Chord import Chord
from src.utils.io_handler import load_pickle
from src.constants import (
    ARRANGEMENT_PICKLE, GENERATIONS, PROCESSED_DIR, MARKOV_PICKLE_SUFFIX, ELITE_RATIO, 
    MUTATION_RATE, POPULATION_SIZE, NOTE_MAP, OCTAVE_NOTE_COUNT, ALLOWED_PAIRS_OF_QUALITY_AND_SEVENTH_TYPE, 
)
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

transposition_factor = -NOTE_MAP.get(key, 0)

chordsInput = ChordsInput()
raw_input = chordsInput.run()
chords_list = [item.strip() for item in raw_input.split(',')]
spaced_chords = " ".join(chords_list)

chordList: Arrangement = parse_arrangements([spaced_chords])[0]

def mutate(parent: Arrangement, mutation_rate: float = MUTATION_RATE):
    mutated_chords = []
    mutated_notes = []

    for chord, note in zip(parent.progression.chords, parent.bassline.notes):

        if chord is not None and random.random() < mutation_rate:
            new_root = (chord.root + random.choice([-1, 1])) % OCTAVE_NOTE_COUNT

            if random.random() < 0.2:
                new_quality, new_seventh = random.choice(ALLOWED_PAIRS_OF_QUALITY_AND_SEVENTH_TYPE)
            else:
                new_quality, new_seventh = chord.quality, chord.seventhType

            mutated_chords.append(
                Chord(root=new_root, quality=new_quality, seventhType=new_seventh, remainders=set())
            )
        else:
            mutated_chords.append(chord)

        if note is not None and random.random() < mutation_rate:
            mutated_notes.append((note + random.choice([-1, 1])) % OCTAVE_NOTE_COUNT)
        else:
            mutated_notes.append(note)

    return Arrangement(
        progression=ChordProgression(chords=mutated_chords),
        bassline=BassLine(notes=mutated_notes)
    )

def uniform_crossover(parentA: Arrangement, parentB: Arrangement):
    children = []
    for _ in range(2):
        progression = []
        bassline = []
        for i, (a, b) in enumerate(zip(parentA.progression.chords, parentB.progression.chords)):
            if random.random() < 0.5:
                progression.append(a)
                bassline.append(parentA.bassline.notes[i])
            else:
                progression.append(b)
                bassline.append(parentB.bassline.notes[i])

        children.append(
            Arrangement(
                progression=ChordProgression(chords=progression),
                bassline=BassLine(notes=bassline)
            )
        )
    return children


def tournament_selection(population, k=5):
    competitors = random.sample(population, k)
    return max(competitors, key=lambda p: p.fitness)


population: list[Arrangement] = load_pickle(PROCESSED_DIR / ARRANGEMENT_PICKLE)

unique_signatures = set()
unique_population = []

for item in population:
    sig = tuple((c.root, c.quality, c.seventhType) for c in item.progression.chords)
    if sig not in unique_signatures:
        unique_signatures.add(sig)
        unique_population.append(item)

population = unique_population

for item in population:
    item.progression.chords = chordList.progression.get_chords() + item.progression.get_chords()
    item.bassline.notes = chordList.bassline.get_notes() + item.bassline.get_notes()
    item.transpose(transposition_factor)

markov = load_pickle(PROCESSED_DIR / f"order2_{MARKOV_PICKLE_SUFFIX}")


for generation in range(GENERATIONS):

    for individual in population:
        individual.evaluate_fitness([markov], chordList.progression.get_chords())

    fitnesses = [p.fitness for p in population]

    median_fitness = statistics.median(fitnesses)
    best = max(population, key=lambda p: p.fitness)

    print(f"\nGeneration {generation}")
    print(f"Median fitness: {median_fitness:.4f}")
    print(f"Best fitness:   {best.fitness:.4f}")

    elite_count = max(1, int(ELITE_RATIO * POPULATION_SIZE))
    elites = sorted(population, key=lambda p: p.fitness, reverse=True)[:elite_count]

    new_population = [copy.deepcopy(e) for e in elites]

    while len(new_population) < POPULATION_SIZE:

        parent1 = tournament_selection(population)
        parent2 = tournament_selection(population)

        children = uniform_crossover(parent1, parent2)

        for child in children:
            if len(new_population) >= POPULATION_SIZE:
                break

            adaptive_mutation = MUTATION_RATE
            if child.fitness < median_fitness:
                adaptive_mutation *= 1.2

            mutated_child = mutate(child, mutation_rate=adaptive_mutation)

            new_population.append(mutated_child)

    population = new_population

best = max(population, key=lambda p: p.fitness)

print("\n=== FINAL RESULT ===")
print(f"Best fitness: {best.fitness}")

for chord in best.progression.chords:
    print(chord)
