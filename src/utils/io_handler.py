import re
from pathlib import Path
import pandas as pd
import pickle
from src.objects.ChordProgression import ChordProgression
from src.constants import SECTION_REGEX

def split_sections(regex: str, progressions: list[str]) -> list[str]:
    split_progressions: list[str] = []
    for progression in progressions:
        split_progression = re.split(regex, progression)
        split_progressions.extend([section.strip() for section in split_progression if section.strip() and not section.startswith('<')])
    return split_progressions

def parse_csv(path:Path, decade:int=1980) -> list[str]:
    all_progressions: list[str] = []
    with pd.read_csv(path, chunksize=65536, usecols=["decade", "chords"]) as reader:
        for chunk in reader:
            chunk_progressions = chunk.loc[chunk["decade"] == decade, "chords"].tolist()
            chunk_progressons = split_sections(SECTION_REGEX, chunk_progressions)
            all_progressions.extend(chunk_progressons)
    return all_progressions

def log_progressions(chord_progressions: list[ChordProgression], filepath: Path):
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'w') as file:
        for progression in chord_progressions:
            string_chords: list[str] = []
            for chord in progression.chords:
                chord_tuple = f"({chord.root},{chord.quality.name},{chord.seventhType.name},'{chord.remainders}',{chord.bass})"
                string_chords.append(chord_tuple)
            file.write(" -> ".join(string_chords) + '\n')

def write_progressions(chord_progressions: list[ChordProgression], filepath: Path):
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'wb') as file:
        pickle.dump(chord_progressions, file)

def load_progressions(filepath: Path) -> list[ChordProgression]:
    with open(filepath, 'rb') as file:
        return pickle.load(file)
