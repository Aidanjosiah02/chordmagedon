import re
from pathlib import Path
import pandas as pd
import pickle
from src.objects.Arrangemment import Arrangement
from src.constants import SECTION_REGEX


def split_sections(regex: str, progressions: list[str]) -> list[str]:
    split_progressions: list[str] = []
    for progression in progressions:
        split_progression = re.split(regex, progression)
        split_progressions.extend([
            section.strip()
            for section in split_progression
            if section.strip() and not section.startswith('<')
        ])
    return split_progressions

def parse_csv(path: Path, decade: int = 1980) -> list[str]:
    all_progressions: list[str] = []
    with pd.read_csv(path, chunksize=65536, usecols=["decade", "chords"]) as reader:
        for chunk in reader:
            chunk_progressions = chunk.loc[
                chunk["decade"] == decade, "chords"
            ].tolist()
            chunk_progressions = split_sections(SECTION_REGEX, chunk_progressions)
            all_progressions.extend(chunk_progressions)

    return all_progressions

def log_arrangements(arrangements: list[Arrangement], filepath: Path):
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'w') as file:
        for arr in arrangements:
            progression_str = " | ".join(
                f"({chord.root},{chord.quality.name},{chord.seventhType.name})"
                for chord in arr.progression.chords
            )
            bassline_str = ",".join(map(str, arr.bassline.notes))
            file.write(f"PROGRESSION: {progression_str}\n")
            file.write(f"BASSLINE: {bassline_str}\n")
            file.write("\n")

def write_arrangements(arrangements: list[Arrangement], filepath: Path):
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'wb') as file:
        pickle.dump(arrangements, file)

def load_arrangements(filepath: Path) -> list[Arrangement]:
    with open(filepath, 'rb') as file:
        return pickle.load(file)
