import re
from src.objects.ChordProgression import ChordProgression
from src.objects.Bassline import BassLine
from src.objects.Arrangement import Arrangement
from src.objects.Chord import Chord
from src.constants import CHORD_REGEX, NOTE_MAP, QUALITY_ENUM_MAP, Quality, SeventhType


def dim_extension_evaluator(extension: str | None):
    match extension:
        case None: return SeventhType.NONE
        case "b7": return SeventhType.DOMINANT
        case x if x.startswith("maj"): return SeventhType.MAJOR
        case _: return SeventhType.DIMINISHED  # b9 etc has a diminished 7th.


def reg_extension_evaluator(extension: str | None):
    match extension:
        case None: return SeventhType.NONE
        case x if x.startswith("maj"): return SeventhType.MAJOR
        case _: return SeventhType.DOMINANT


def parse_arrangements(slash_arrangement_strings: list[str]) -> list[Arrangement]:
    arrangements: list[Arrangement] = []

    for slash_arrangement_string in slash_arrangement_strings:
        slash_chord_strings: list[str] = slash_arrangement_string.split(' ')

        chords: list[Chord] = []
        bass_notes: list[int] = []

        for slash_chord_string in slash_chord_strings:

            slash_chord = slash_chord_string.split("/")
            chord_string = slash_chord[0]

            # Handle suspended chords manually
            quality_string = ""
            if chord_string.endswith(("sus2", "sus4")):
                quality_string = chord_string[-4:]
                chord_string = chord_string[:-4]

            match: re.Match[str] | None = CHORD_REGEX.match(chord_string)
            if not match:
                print(f"No root found for {slash_chord_string}")
                continue

            root_match, quality_match, extension_match, remainder_match = match.groups()

            root_note: int = NOTE_MAP[root_match]

            # We can infer bass notes if we do not have a slash chord to tell us
            # what the bass note is
            if len(slash_chord) > 1 and slash_chord[1]:
                bass_note: int = NOTE_MAP[slash_chord[1]]
            else:
                bass_note: int = root_note

            # we need to make sure the bass note is in range
            bass_notes.append(bass_note % 13 or 13)

            # Quality handling
            if not quality_string:
                quality_string = quality_match

            quality: Quality = QUALITY_ENUM_MAP[quality_string]

            extension_string = extension_match
            extension = SeventhType.NONE

            if quality == Quality.DIMINISHED:
                if extension_string != '':
                    extension = dim_extension_evaluator(extension_string)
            else:
                extension = reg_extension_evaluator(extension_string)

            chord = Chord(root_note, quality, extension,
                          remainder_match)
            chords.append(chord)

        progression = ChordProgression(chords)

        bassline = BassLine(bass_notes)

        arrangement = Arrangement(
            progression=progression,
            bassline=bassline
        )

        arrangement.validate()
        arrangements.append(arrangement)

    return arrangements
