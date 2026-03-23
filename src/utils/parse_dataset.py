import re
from pathlib import Path
import pandas as pd

from src.constants import CHORD_REGEX, CHORD_REGEX2, CHORD_REGEX3, EXTENSION_REGEX, NOTE_MAP, QUALITY_ENUM_MAP, SECTION_REGEX, Quality, SeventhType

def split_sections(regex: str, progressions: list[str]) -> list[str]:
    split_progressions: list[str] = []
    for progression in progressions:
        split_progression = re.split(regex, progression)
        split_progressions.extend([section.strip() for section in split_progression if section.strip() and not section.startswith('<')])
    return split_progressions






def dim_extension_evaluator(extension: str):
    match extension:
        case "": return SeventhType.NONE
        case "b7": return SeventhType.DOMINANT
        case x if x.startswith("maj"): return SeventhType.MAJOR
        case _: return SeventhType.DIMINISHED # b9 etc has a diminished 7th.

def reg_extension_evaluator(extension: str):
    match extension:
        case "": return SeventhType.NONE
        case x if x.startswith("maj"): return SeventhType.MAJOR
        case _: return SeventhType.DOMINANT

# def flatten_extension(extension: str) -> str:
#     if extension:
#         match = re.search(EXTENSION_REGEX, extension)
#         if match:
#             index = match.start()
#             return (extension[:index] + '7')
#     return ''

def parse_csv(path:Path, decade:int=1980) -> list[str]:
    all_progressions: list[str] = []
    with pd.read_csv(path, chunksize=65536, usecols=["decade", "chords"]) as reader:
        for chunk in reader:
            chunk_progressons = chunk.loc[chunk["decade"] == decade, "chords"].tolist()
            chunk_progressons = split_sections(SECTION_REGEX, chunk_progressons)
            all_progressions.extend(chunk_progressons)
    
    # roots: set[str] = set()
    # qualities: set[str] = set()
    # extensions: set[str] = set()
    # remainders: set[str] = set()
    all_clean_progressions = []
    for progression in all_progressions:
        chords = progression.split(' ')
        clean_chords: list[str] = []
        for chord in chords:
            clean_chord = chord.split("/")[0]
            match = re.match(CHORD_REGEX, clean_chord)
            root = match.group(1)
            remainder = match.group(2)
            # roots.add(root)

            match = re.match(CHORD_REGEX2, remainder)
            quality_string = match.group(1)
            quality = QUALITY_ENUM_MAP[quality_string]
            remainder = match.group(3)
            if quality == Quality.MAJOR:
                if remainder.endswith("sus2") or remainder.endswith("sus4"):
                    quality = QUALITY_ENUM_MAP[remainder[-4:]]
                    remainder = remainder[:-4]
            # qualities.add(quality)

            match = re.match(CHORD_REGEX3, remainder)
            extension = match.group(1)
            remainder = match.group(7)

            new_extension = SeventhType.NONE
            if quality == Quality.DIMINISHED:
                if extension != '':
                    new_extension = dim_extension_evaluator(extension)
            else:
                new_extension = reg_extension_evaluator(extension)


            # chord_tuple = (root, quality, extension, remainder)
            chord_tuple = (str(NOTE_MAP[root]), str(quality.value), str(new_extension.value), remainder)
            clean_chords.append(chord_tuple)
        all_clean_progressions.append(clean_chords)

    with open("log.txt", 'a') as file:
        for progression in all_clean_progressions:
            string_chords = []
            for chord in progression:
                string_chords.append('(' + ','.join(chord) + ')')
            file.write(','.join(string_chords) + '\n')

    # print(roots)
    # print(qualities)
    # print(extensions)
    # print(remainders)
    
    
    return all_clean_progressions

# {'Gb', 'Cs', 'As', 'D', 'E', 'Fs', 'Bb', 'Ab', 'Ds', 'Db', 'F', 'G', 'Gs', 'C', 'B', 'Eb', 'A'}
# {'', 'min', 'sus2', 'no3d', 'sus4', 'aug', 'dim'}
# {'', 'add13', 'b7', '13', 'maj13', 'maj11', 'majs911s', 'b9', 'add11', 'maj911s', '13b', '9', 'maj1311s', 'add9', 'majs9', '11s', '7b9', '11b9', '13b9', 'maj7', '11', '7', 'maj9'}

# print(parse_csv(Path("data\chordonomicon_v2.csv")))
progressions = parse_csv(Path("data/chordonomicon_v2.csv"))

