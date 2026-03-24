from pathlib import Path
from src.constants import DATASET, LOG, PICKLE
from src.utils.parse_dataset import log_progressions, parse_csv, parse_progressions, write_progressions

def main():
    print(f"Loading {DATASET}...")
    chord_progression_strings = parse_csv(Path(DATASET))
    print(f"Parsing the dataset...")
    chord_progressions = parse_progressions(chord_progression_strings)
    print(f"\nFinal chord progression example:\n\t{chord_progressions[-1]}\n")
    print(f"Storing log file at: {LOG},\nand Pickle file at: {PICKLE}")
    log_progressions(chord_progressions, Path(LOG))
    write_progressions(chord_progressions, Path(PICKLE))

if __name__ == "__main__":
    main()