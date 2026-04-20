import statistics
import copy
import random
from typing import cast

from src.formulas import score_saturator
from src.objects.MixedProgression import MixedProgression
from src.objects.Markov import Markov
from src.objects.Chord import Chord
from src.utils.io_handler import load_pickle
from src.constants import (
    ARRANGEMENT_PICKLE, GENERATIONS, PROCESSED_DIR, MARKOV_PICKLE_SUFFIX, ELITE_RATIO, 
    MUTATION_RATE, POPULATION_SIZE, NOTE_MAP, OCTAVE_NOTE_COUNT, ALLOWED_PAIRS_OF_QUALITY_AND_SEVENTH_TYPE, Quality, SeventhType, 
)
from src.objects.Arrangement import Arrangement
from src.objects.ChordProgression import ChordProgression
from src.objects.BassLine import BassLine
from src.widgets.CompositionKeySelection import CompositionKeySelection
from src.widgets.ChordsInput import ChordsInput
from src.utils.parser import parse_arrangements
from src.types import Key, ChordTuple
from src.utils.midi_export import export_midi


def mutate(parent: Arrangement, mutation_rate: float = MUTATION_RATE):
    mutated_chords: list[Chord] = []
    mutated_notes: list[int] = []

    for chord, bass_note in zip(parent.progression.chords, parent.bassline.notes):
        if random.random() > mutation_rate:
            mutated_chords.append(chord)
        else: 
            new_root = (chord.root + random.choice([-7, 7])) % OCTAVE_NOTE_COUNT
            if random.random() < 0.4:
                new_quality, new_seventh = random.choice(ALLOWED_PAIRS_OF_QUALITY_AND_SEVENTH_TYPE)
            else:
                new_quality = chord.quality
                new_seventh = chord.seventhType
            mutated_chords.append(Chord(new_root, new_quality, new_seventh))

        if random.random() > mutation_rate:
            mutated_notes.append(bass_note)
        else:
            mutated_notes.append((bass_note + random.choice([-7, 7])) % OCTAVE_NOTE_COUNT)
            
    return Arrangement(progression = ChordProgression(mutated_chords), bassline = BassLine(mutated_notes))



def uniform_crossover(parentA: Arrangement, parentB: Arrangement) -> list[Arrangement]:
    children: list[Arrangement] = []
    for _ in range(2):
        progression: list[Chord] = []
        bassline: list[int] = []
        for index, (a, b) in enumerate(zip(parentA.progression.chords, parentB.progression.chords)):
            if random.random() < 0.5:
                progression.append(a)
                bassline.append(parentA.bassline.notes[index])
            else:
                progression.append(b)
                bassline.append(parentB.bassline.notes[index])

        children.append(Arrangement(progression = ChordProgression(progression), bassline = BassLine(bassline)))
    return children


def tournament_selection(population: list[Arrangement], selection_count: int = 6):
    competitors = random.sample(population, selection_count)
    return max(competitors, key=lambda arrangement: arrangement.fitness)











def get_best_next_chord(progression: list[Chord | None], index: int, markovs: list[Markov]) -> ChordTuple | None:
    progression_tuples = [chord.to_tuple() if chord else None for chord in progression]
    for markov in markovs:
        # if we don't have enough history for this Markov's order, try the next lower-order markov.
        if index < markov.order:
            continue
        context_start = index - markov.order
        context = tuple(progression_tuples[context_start : index])
        if None in context:
            continue
        transitions = markov.get_entry_by_key(context) # type: ignore
        if transitions:
            saturated_transitions: dict[ChordTuple, float] = {}
            for chord_tuple, count in transitions.items():
                score = score_saturator(max(transitions.values()), count)
                saturated_transitions[chord_tuple] = score
            options = list(saturated_transitions.keys())
            weights = list(saturated_transitions.values())
            
            return random.choices(options, weights=weights, k=1)[0]
            # # https://www.geeksforgeeks.org/python/python-get-key-with-maximum-value-in-dictionary/
            # # Returning here since a higher-order markov that matches is best.
            # return max(transitions, key=transitions.get) # type: ignore
    return None # If no matches exist.


def find_bridge_chords2(markov: Markov, progression: list[Chord | None], index: int, chord_after: Chord):
    matches: dict[ChordTuple, int] = {}
    after_tuple = chord_after.to_tuple()
    
    # Subtract 1 because one slot in the key is the missing chord X
    history_needed = markov.order - 1
    if index < history_needed:
        return matches

    # Get context leading up to the gap
    context_start = index - history_needed
    past_context = [chord.to_tuple() for chord in progression[context_start:index]]
    
    for key, targets in markov.chain.items():

        if list(key[:history_needed]) == past_context:
            if after_tuple in targets:
                chord_x = key[-1]
                matches[chord_x] = targets[after_tuple]
                
    return matches

def fill_progression_gaps(mixed_progression: MixedProgression, markovs: list[Markov]) -> ChordProgression:
    tonic: Chord
    first_chord = mixed_progression[0]
    if first_chord:
        tonic = first_chord
    else: 
        tonic = Chord(0, Quality(0), SeventhType(0))
    
    filled_chords = list(mixed_progression.get_chords()) + [tonic] # Adding the tonic to give it an end goal
    markovs_sorted = sorted(markovs, key=lambda m: m.order, reverse=True)

    for index1 in range(len(filled_chords)):
        if filled_chords[index1] is None:
            chord_after = None
            gap_end_index = len(filled_chords) # Default to end of list
            for index2 in range(index1, len(filled_chords)):
                if filled_chords[index2] is not None:
                    chord_after = filled_chords[index2]
                    gap_end_index = index2
                    break
            
            gap_size = gap_end_index - index1
            filled = False
            # Using the bridge if and only if there exists a 1-space gap.
            if gap_size == 1 and chord_after:
                for markov in markovs_sorted:
                    matches = find_bridge_chords2(markov, filled_chords, index1, chord_after)
                    if matches:

                        # Attempt to make less likely but still realistic transitions a chance to occur.
                        saturated_matches: dict[ChordTuple, float] = {}
                        for chord, count in matches.items():
                            score = score_saturator(max(matches.values()), count)
                            saturated_matches[chord] = score
                        
                        # Selecting based on probability
                        options = list(saturated_matches.keys())
                        selection_weights = list(saturated_matches.values())
                        chosen_tuple = random.choices(options, weights=selection_weights, k=1)[0]
                        filled_chords[index1] = Chord(chosen_tuple[0], Quality(chosen_tuple[1]), SeventhType(chosen_tuple[2]))

                        filled = True
                        break
            
            if not filled:
                # Get the best next chord from our Markovs
                next_chord_tuple = get_best_next_chord(filled_chords, index1, markovs_sorted)
                if next_chord_tuple:
                    filled_chords[index1] = Chord(next_chord_tuple[0], Quality(next_chord_tuple[1]), SeventhType(next_chord_tuple[2]))
                elif index1 > 0:
                    filled_chords[index1] = filled_chords[index1-1] # TODO: Change to random rather than previous chord. if none found.
                else: 
                    filled_chords[index1] = tonic # TODO: Change to random rather than previous chord. if none found.

    return ChordProgression(filled_chords[:-1], mixed_progression.get_root()) # Chop off the end to remove the temporary tonic.



def merge_user_chords_with_arrangements(arrangements: list[Arrangement], user_chords: MixedProgression) -> list[MixedProgression]:
    user_progression_length = len(user_chords)
    mixed_progressions: list[MixedProgression] = []
    for arrangement in arrangements:
        mixed_progression: MixedProgression = MixedProgression(list(arrangement.get_progression().get_chords()), user_chords.get_root())
        
        # extends the stored progression to the length of the user's chord progression.
        stored_progression_length = len(mixed_progression)
        if stored_progression_length < user_progression_length:
            mixed_progression.get_chords().extend([None] * (user_progression_length - stored_progression_length))
        elif stored_progression_length > user_progression_length:
            del mixed_progression.get_chords()[user_progression_length:]

        # 2. Overwrite non-None user chords at their appropriate positions
        for index in range(user_progression_length):
            user_chord = user_chords[index]
            if user_chord is not None:
                mixed_progression[index] = user_chord
        mixed_progressions.append(mixed_progression)
                
    return mixed_progressions



def get_user_chords(root: int):
    
    progression_length = int(input("Please give the desired chord progression length (ex. 8): "))
    user_progression: MixedProgression = MixedProgression([], root)
    user_progression_chords = user_progression.chords
    exit: bool = False
    iteration = 0
    while not exit and iteration < progression_length:
        iteration += 1
        print()
        print(NOTE_MAP)
        chord_root = input(f"Please input the note number value for chord {iteration} ('q' to finish, 's' to skip): ")
        if (chord_root == 'q'):
            break
        if (chord_root == 's'):
            user_progression_chords.append(None)
            continue
        print()
        print(Quality.to_string())
        chord_quality = input(f"Please input the chord quality for chord {iteration} ('q' to finish): ")
        if (chord_quality == 'q'):
            break
        print()
        print(SeventhType.to_string())
        chord_seventh = input(f"Please input the 7th type for chord {iteration} ('q' to finish): ")
        if (chord_seventh == 'q'):
            break
        user_progression_chords.append(Chord(int(chord_root), Quality(int(chord_quality)), SeventhType(int(chord_seventh))))
    
    padding = progression_length - len(user_progression_chords)
    if padding > 0:
        user_progression_chords.extend([None] * padding)

    return user_progression



def init_population(markovs: list[Markov], user_progression: MixedProgression, existing_arrangements: list[Arrangement], max_arrangements: int):
    
    mixed_progressions = merge_user_chords_with_arrangements(existing_arrangements, user_progression)
    if len(mixed_progressions) > max_arrangements:
        mixed_progressions = random.sample(mixed_progressions, max_arrangements)

    arrangements: list[Arrangement] = []
    for mixed_progression in mixed_progressions:
        progression: ChordProgression = fill_progression_gaps(mixed_progression, markovs)
        arrangement = Arrangement(progression, progression.generate_baseline())
        arrangements.append(arrangement)

    return arrangements



def main():
    markovs: list[Markov] = [
        load_pickle(PROCESSED_DIR / f"order1_{MARKOV_PICKLE_SUFFIX}"),
        load_pickle(PROCESSED_DIR / f"order2_{MARKOV_PICKLE_SUFFIX}"),
        load_pickle(PROCESSED_DIR / f"order3_{MARKOV_PICKLE_SUFFIX}"),
        load_pickle(PROCESSED_DIR / f"order4_{MARKOV_PICKLE_SUFFIX}")
    ] # type: ignore
    existing_arrangements: list[Arrangement] = load_pickle(PROCESSED_DIR / ARRANGEMENT_PICKLE) # type: ignore
    
    print()
    print(NOTE_MAP)
    progression_key = int(input("Please input the note number for the desired chord progression key: "))
    user_progression: MixedProgression = get_user_chords(progression_key)
    user_progression.transpose(-progression_key)
    print(user_progression)

    # init_population is where useer input is taken.
    # get_user_chords is used by init_population for chord inputs.
    arrangements: list[Arrangement] = init_population(markovs, user_progression, existing_arrangements, POPULATION_SIZE)
    print(arrangements)
    
    fitness_cache: dict[int, float] = {}

    print(f"\nStarting Evolution for {GENERATIONS} generations...")
    for generation in range(GENERATIONS):

        
        for arrangement in arrangements:
            arrangement_hash = hash(arrangement)
            if arrangement_hash in fitness_cache:
                arrangement.set_fitness(fitness_cache[arrangement_hash])
            else:
                fitness = arrangement.evaluate_fitness(markovs, user_progression.get_chords())
                fitness_cache[arrangement_hash] = fitness

        # for arrangement in arrangements:
        #     arrangement.evaluate_fitness(markovs, arrangement.get_progression().get_chords())
            
        fitnesses = [arrangement.get_fitness() for arrangement in arrangements]

        median_fitness = statistics.median(fitnesses)
        best = max(arrangements, key=lambda arrangement: arrangement.get_fitness())

        print(f"\nGeneration {generation}")
        print(f"Median fitness: {median_fitness:.4f}")
        print(f"Best fitness:   {best.fitness:.4f}")

        elite_count = max(1, int(ELITE_RATIO * POPULATION_SIZE))
        elites = sorted(arrangements, key=lambda arrangement: arrangement.get_fitness(), reverse=True)[:elite_count]

        unique_arrangement_hashes = {hash(elite) for elite in elites} # New to prevent duplicate progressions
        new_arrangements = [copy.deepcopy(elite) for elite in elites]

        while len(new_arrangements) < POPULATION_SIZE:

            parent1 = tournament_selection(arrangements)
            parent2 = tournament_selection(arrangements)
            children = uniform_crossover(parent1, parent2)

            for child in children:
                if len(new_arrangements) >= POPULATION_SIZE:
                    break
                adaptive_mutation = MUTATION_RATE
                if child.fitness < median_fitness:
                    adaptive_mutation *= 1.0

                mutated_child = mutate(child, mutation_rate=adaptive_mutation)

                # Only add if it's a new unique arrangement for this generation
                child_hash = hash(mutated_child)
                if child_hash not in unique_arrangement_hashes:
                    new_arrangements.append(mutated_child)
                    unique_arrangement_hashes.add(child_hash)

        arrangements = new_arrangements



    final_sorted = sorted(arrangements, key=lambda p: p.fitness, reverse=True)
    
    # 2. Take the top 3 (or the whole list if it's smaller than 3)
    top3_arrangements = final_sorted[:3]

    print("\n=== FINAL RESULTS (TOP 3) ===")
    for index, arrangement in enumerate(top3_arrangements, 1):
        print(f"\nRank {index}, with fitness: {arrangement.fitness:.4f}")
        print("--------------------------------")
        for chord in arrangement.get_progression().get_chords():
            print(chord)
        export_midi(arrangement, f"song_{index}.mid", 500000, 120)

    



main()


# def main():

#     keySelection = CompositionKeySelection()
#     key_root: int | None = keySelection.run() # type: ignore

#     if key_root is None:
#         print("No key Selected")
#         exit()

#     transposition_factor: int = -key_root # type: ignore

#     chordsInput = ChordsInput()
#     user_chords: list[Chord | None] = cast(list[Chord | None], chordsInput.run())
#     print(user_chords)

#     if not user_chords:
#         exit()
#     user_bass = [chord.root for chord in user_chords]
#     chord_list = Arrangement(progression=ChordProgression(user_chords), bassline=BassLine(user_bass))

#     arrangements: list[Arrangement] = load_pickle(PROCESSED_DIR / ARRANGEMENT_PICKLE) # type: ignore

#     unique_keys: set[Key] = set()
#     unique_arrangements: list[Arrangement] = []
#     for arrangement in arrangements:
#         key = tuple(chord.to_tuple() for chord in arrangement.progression.chords)
#         unique_keys.add(key)
#         unique_arrangements.append(arrangement)

#     for arrangement in unique_arrangements:
#         arrangement.progression.chords = chord_list.progression.get_chords() + arrangement.progression.get_chords()
#         arrangement.bassline.notes = chord_list.bassline.get_notes() + arrangement.bassline.get_notes()
#         arrangement.transpose(transposition_factor)


#     markov: Markov = load_pickle(PROCESSED_DIR / f"order2_{MARKOV_PICKLE_SUFFIX}") # type: ignore
#     for generation in range(GENERATIONS):

#         for arrangement in arrangements:
#             arrangement.evaluate_fitness([markov], chord_list.progression.get_chords())

#         fitnesses = [arrangement.get_fitness() for arrangement in arrangements]

#         median_fitness = statistics.median(fitnesses)
#         best = max(arrangements, key=lambda arrangement: arrangement.fitness)

#         print(f"\nGeneration {generation}")
#         print(f"Median fitness: {median_fitness:.4f}")
#         print(f"Best fitness:   {best.fitness:.4f}")

#         elite_count = max(1, int(ELITE_RATIO * POPULATION_SIZE))
#         elites = sorted(arrangements, key=lambda arrangement: arrangement.get_fitness(), reverse=True)[:elite_count]

#         new_arrangements = [copy.deepcopy(elite) for elite in elites]

#         while len(new_arrangements) < POPULATION_SIZE:

#             parent1 = tournament_selection(arrangements)
#             parent2 = tournament_selection(arrangements)
#             children = uniform_crossover(parent1, parent2)
#             for child in children:
#                 if len(new_arrangements) >= POPULATION_SIZE:
#                     break
#                 adaptive_mutation = MUTATION_RATE
#                 if child.fitness < median_fitness:
#                     adaptive_mutation *= 1.2

#                 mutated_child = mutate(child, mutation_rate=adaptive_mutation)
#                 new_arrangements.append(mutated_child)
#         arrangements = new_arrangements

#     best = max(arrangements, key=lambda p: p.fitness)

#     print("\n=== FINAL RESULT ===")
#     print(f"Best fitness: {best.fitness}")

#     for chord in best.progression.chords:
#         print(chord)

# main()
