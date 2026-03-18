import re
from pathlib import Path
import pandas as pd

from src.constants import CHORD_REGEX, SECTION_REGEX, Quality, Type

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
            chunk_progressons = chunk.loc[chunk["decade"] == decade, "chords"].tolist()
            chunk_progressons = split_sections(SECTION_REGEX, chunk_progressons)
            all_progressions.extend(chunk_progressons)
    
    roots: set[str] = set()
    remainders: set[str] = set()
    for progression in all_progressions:
        chords = progression.split(' ')
        clean_chords: list[str] = []
        for chord in chords:
            clean_chord = chord.split("/")[0]
            match = re.match(CHORD_REGEX, clean_chord)
            root = match.group(1)
            remainder = match.group(2)
            roots.add(root)
            remainders.add(remainder)
            # root_value = NOTE_MAP[root]
    print(roots)
    print(remainders)
        # print(clean_chords)
    
    return all_progressions



# print(parse_csv(Path("data\chordonomicon_v2.csv")))
parse_csv(Path("data/chordonomicon_v2.csv"))

