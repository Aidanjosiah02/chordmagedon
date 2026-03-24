import re
from pathlib import Path
import pandas as pd
from timeit import default_timer
import pickle

from src.objects.ChordProgression import ChordProgression
from src.objects.Chord import Chord
from src.constants import CHORD_REGEX, CHORD_REGEX2, CHORD_REGEX3, CHORD_REGEX4, NOTE_MAP, QUALITY_ENUM_MAP, SECTION_REGEX, Quality, SeventhType

def split_sections(regex: str, progressions: list[str]) -> list[str]:
    split_progressions: list[str] = []
    for progression in progressions:
        split_progression = re.split(regex, progression)
        split_progressions.extend([section.strip() for section in split_progression if section.strip() and not section.startswith('<')])
    return split_progressions

def dim_extension_evaluator(extension: str|None):
    match extension:
        case None: return SeventhType.NONE
        case "b7": return SeventhType.DOMINANT
        case x if x.startswith("maj"): return SeventhType.MAJOR
        case _: return SeventhType.DIMINISHED # b9 etc has a diminished 7th.

def reg_extension_evaluator(extension: str|None):
    match extension:
        case None: return SeventhType.NONE
        case x if x.startswith("maj"): return SeventhType.MAJOR
        case _: return SeventhType.DOMINANT

def parse_csv(path:Path, decade:int=1980) -> list[str]:
    all_progressions: list[str] = []
    with pd.read_csv(path, chunksize=65536, usecols=["decade", "chords"]) as reader:
        for chunk in reader:
            chunk_progressions = chunk.loc[chunk["decade"] == decade, "chords"].tolist()
            chunk_progressons = split_sections(SECTION_REGEX, chunk_progressions)
            all_progressions.extend(chunk_progressons)
    return all_progressions



def parse_progressions_old(slash_progression_strings: list[str]) -> list[list[Chord]]:

    chord_progressions: list[list[Chord]] = []
    for slash_progression_string in slash_progression_strings:

        slash_chord_strings: list[str] = slash_progression_string.split(' ')
        chord_progression: list[Chord] = []
        for slash_chord_string in slash_chord_strings:

            slash_chord = slash_chord_string.split("/")
            chord_string = slash_chord[0]
            
            # Finding the root note
            match: re.Match[str] | None = CHORD_REGEX.match(chord_string)
            if not match:
                print(f"No root found for {slash_chord_string}")
                continue
            root_note: int = NOTE_MAP[match.group('root')]
            bass_note: int = NOTE_MAP[slash_chord[1]] if len(slash_chord) > 1 and slash_chord[1] else root_note
            remainder_string: str = match.group('remainder')

            # Finding the quality (dim, min, sus2, etc.)
            quality_string = ""
            if remainder_string.endswith(("sus2", "sus4")):
                quality_string = remainder_string[-4:]
                remainder_string = remainder_string[:-4]
            else:
                match = CHORD_REGEX2.match(remainder_string)
                if match:
                    quality_string = match.group('quality')
                    remainder_string = match.group('remainder')
            quality: Quality = QUALITY_ENUM_MAP[quality_string]

            # Finding the extensions (7th, major 9th, etc.)
            extension_string = ""
            match: re.Match[str] | None = CHORD_REGEX3.match(remainder_string)
            if match:
                extension_string = match.group("extension")
                remainder_string = match.group("remainder")

            extension = SeventhType.NONE
            if quality == Quality.DIMINISHED:
                if extension_string != '':
                    extension = dim_extension_evaluator(extension_string)
            else:
                extension = reg_extension_evaluator(extension_string)

            chord = Chord(root_note, quality, extension, remainder_string, bass_note)
            chord_progression.append(chord)

        chord_progressions.append(chord_progression)

    return chord_progressions



# Combined regex and match degrouping improved performance by 25%
def parse_progressions(slash_progression_strings: list[str]) -> list[ChordProgression]:

    chord_progressions: list[ChordProgression] = []
    for slash_progression_string in slash_progression_strings:

        slash_chord_strings: list[str] = slash_progression_string.split(' ')
        chords: list[Chord] = []
        for slash_chord_string in slash_chord_strings:

            slash_chord = slash_chord_string.split("/")
            chord_string = slash_chord[0]
            
            quality_string = ""
            if chord_string.endswith(("sus2", "sus4")):
                quality_string = chord_string[-4:]
                chord_string = chord_string[:-4]
            match: re.Match[str] | None = CHORD_REGEX4.match(chord_string)
            if not match:
                print(f"No root found for {slash_chord_string}")
                continue
            root_raw, quality_str, extension_str, remainder_str = match.groups()
            root_note: int = NOTE_MAP[root_raw]
            bass_note: int = NOTE_MAP[slash_chord[1]] if len(slash_chord) > 1 and slash_chord[1] else root_note
            if not quality_string:
                quality_string = quality_str
            quality: Quality = QUALITY_ENUM_MAP[quality_string]
            extension_string = extension_str
            extension = SeventhType.NONE
            if quality == Quality.DIMINISHED:
                if extension_string != '':
                    extension = dim_extension_evaluator(extension_string)
            else:
                extension = reg_extension_evaluator(extension_string)
            remainder_string: str = remainder_str

            chord = Chord(root_note, quality, extension, remainder_string, bass_note)
            chords.append(chord)
        chord_progressions.append(ChordProgression(chords))

    return chord_progressions



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

def main():
    start = default_timer()
    chord_progression_strings = parse_csv(Path("data/chordonomicon_v2.csv"))
    end = default_timer()
    print(f"Loading the dataset takes {end - start} seconds")

    start = default_timer()
    parse_progressions(chord_progression_strings)
    end = default_timer()
    print(f"Parsing the dataset takes {end - start} seconds")

if __name__ == "__main__":
    main()