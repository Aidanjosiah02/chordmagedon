from pathlib import Path
from src.objects.Arrangement import Arrangement
from src.constants import ARRANGEMENT_LOG, ARRANGEMENT_PICKLE, DATASET, MARKOV_CHORD_LOG, MARKOV_CHORD_PICKLE
from src.utils.io_handler import log_arrangements, log_markov, parse_csv, write_pickle
from src.utils.parser import parse_arrangements
from src.utils.build_markov import build_markov_chords, get_markov_score
from src.types import Chain

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

def run_markov(arrangements: list[Arrangement]) -> Chain:
    print(f"\nBuilding chord Markov chain...")
    markov_chords = build_markov_chords(arrangements)
    key = next(iter(markov_chords))
    print(f"\nMarkov entry example:\n\t{key} -> {markov_chords[key]}\n")
    print(f"Storing log file at: {MARKOV_CHORD_LOG},\nand Pickle file at: {MARKOV_CHORD_PICKLE}")
    log_markov(markov_chords, Path(MARKOV_CHORD_LOG))
    write_pickle(markov_chords, Path(MARKOV_CHORD_PICKLE))
    return markov_chords

def main():
    arrangements = run_dataset()
    markov = run_markov(arrangements)

    context = ((4, 0, 0), (3, 1, 0))
    target = (10, 1, 0)
    print(get_markov_score(markov, context, target))

    context = ((0, 0, 0), (5, 0, 0))
    target = (2, 6, 1)
    print(get_markov_score(markov, context, target))


if __name__ == "__main__":
    main()
