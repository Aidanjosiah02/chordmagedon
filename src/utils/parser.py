import re
from src.objects.ChordProgression import ChordProgression
from src.objects.Chord import Chord
from src.constants import CHORD_REGEX, NOTE_MAP, QUALITY_ENUM_MAP, Quality, SeventhType

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

def parse_progressions(slash_progression_strings: list[str]) -> list[ChordProgression]:
    chord_progressions: list[ChordProgression] = []
    for slash_progression_string in slash_progression_strings:
        slash_chord_strings: list[str] = slash_progression_string.split(' ')
        chords: list[Chord] = []
        for slash_chord_string in slash_chord_strings:

            # Slash chord = chord/bass_note representation. 
            slash_chord = slash_chord_string.split("/")
            chord_string = slash_chord[0]
            
            # Suspended chords have the "sus" declaration at the end, which regex has a hard time with, so manual splitting here.
            quality_string = ""
            if chord_string.endswith(("sus2", "sus4")):
                quality_string = chord_string[-4:]
                chord_string = chord_string[:-4]

            # Regex splitting for the rest of the chord.
            match: re.Match[str] | None = CHORD_REGEX.match(chord_string)
            if not match:
                print(f"No root found for {slash_chord_string}")
                continue
            root_match, quality_match, extension_match, remainder_match = match.groups()

            # Root and bass found.
            root_note: int = NOTE_MAP[root_match]
            bass_note: int = NOTE_MAP[slash_chord[1]] if len(slash_chord) > 1 and slash_chord[1] else root_note

            # If the cord is NOT suspended, then quality_string will be empty here.
            if not quality_string:
                quality_string = quality_match
            quality: Quality = QUALITY_ENUM_MAP[quality_string]

            # If a 7th+ chord, determining the type while considering diminished chord rules.
            extension_string = extension_match
            extension = SeventhType.NONE
            if quality == Quality.DIMINISHED:
                if extension_string != '':
                    extension = dim_extension_evaluator(extension_string)
            else:
                extension = reg_extension_evaluator(extension_string)

            # Completed chord definition. See logs directory for example after running.
            chord = Chord(root_note, quality, extension, remainder_match, bass_note)
            chords.append(chord)
        chord_progressions.append(ChordProgression(chords))
    return chord_progressions
