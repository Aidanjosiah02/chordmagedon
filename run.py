from pathlib import Path
from src.objects.Arrangement import Arrangement
from src.constants import ARRANGEMENT_LOG, ARRANGEMENT_PICKLE, DATASET, FIRST_MARKOV_CHORD_LOG, FIRST_MARKOV_CHORD_PICKLE, SECOND_MARKOV_CHORD_LOG, SECOND_MARKOV_CHORD_PICKLE
from src.utils.io_handler import log_arrangements, log_markov, parse_csv, write_pickle
from src.utils.parser import parse_arrangements
from src.utils.build_markov import build_first_markov_chords, build_second_markov_chords
from src.types import FirstChain, SecondChain

def run_dataset():
    print(f"\nLoading {DATASET}...")
    chord_progression_strings = parse_csv(Path(DATASET))
    print(f"Parsing the dataset...")
    arrangements = parse_arrangements(chord_progression_strings)
    print(f"\nFinal arrangement example:\n\t{arrangements[-1]}\n")
    print(f"Storing log file at: {ARRANGEMENT_LOG},\nand Pickle file at: {ARRANGEMENT_PICKLE}")
    log_arrangements(arrangements, Path(ARRANGEMENT_LOG))
    write_pickle(arrangements, Path(ARRANGEMENT_PICKLE))
    return arrangements

def run_first_markov(arrangements: list[Arrangement]) -> FirstChain:
    print(f"\nBuilding 1st-order chord Markov chain...")
    markov_chords = build_first_markov_chords(arrangements)
    key = next(iter(markov_chords))
    print(f"\nMarkov entry example:\n\t{key} -> {markov_chords[key]}\n")
    print(f"Storing log file at: {FIRST_MARKOV_CHORD_LOG},\nand Pickle file at: {FIRST_MARKOV_CHORD_PICKLE}")
    log_markov(markov_chords, Path(FIRST_MARKOV_CHORD_LOG))
    write_pickle(markov_chords, Path(FIRST_MARKOV_CHORD_PICKLE))
    return markov_chords

def run_second_markov(arrangements: list[Arrangement]) -> SecondChain:
    print(f"\nBuilding 2nd-order chord Markov chain...")
    markov_chords = build_second_markov_chords(arrangements)
    key = next(iter(markov_chords))
    print(f"\nMarkov entry example:\n\t{key} -> {markov_chords[key]}\n")
    print(f"Storing log file at: {SECOND_MARKOV_CHORD_LOG},\nand Pickle file at: {SECOND_MARKOV_CHORD_PICKLE}")
    log_markov(markov_chords, Path(SECOND_MARKOV_CHORD_LOG))
    write_pickle(markov_chords, Path(SECOND_MARKOV_CHORD_PICKLE))
    return markov_chords

def main():
    arrangements: list[Arrangement] = run_dataset()
    markov1 = run_first_markov(arrangements)
    markov2 = run_second_markov(arrangements)

    for arrangement in arrangements:
        fitness = arrangement.evaluate_fitness(markov1, markov2)
        # print(str(arrangement) + " = " + str(fitness))
    
    cliche_arrangement = max(arrangements, key=lambda a: a.fitness)
    print(cliche_arrangement)
    # context = ((4, 0, 0), (3, 1, 0))
    # target = (10, 1, 0)
    # print(get_markov_score(markov1, context, target))

    # context = (5, 0, 0)
    # target = (2, 6, 1)
    # print(get_markov_score(markov2, context, target))


if __name__ == "__main__":
    main()
