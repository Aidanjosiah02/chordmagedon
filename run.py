from pathlib import Path
from src.constants import DATASET, LOG, PICKLE
from src.utils.io_handler import log_arrangements, parse_csv, write_arrangements
from src.utils.parser import parse_arrangements

def main():
    print(f"Loading {DATASET}...")
    chord_progression_strings = parse_csv(Path(DATASET))
    print(f"Parsing the dataset...")
    arrangements = parse_arrangements(chord_progression_strings)
    print(f"\nFinal arrangement example:\n\t{arrangements[-1]}\n")
    print(f"Storing log file at: {LOG},\nand Pickle file at: {PICKLE}")
    log_arrangements(arrangements, Path(LOG))
    write_arrangements(arrangements, Path(PICKLE))


if __name__ == "__main__":
    main()
