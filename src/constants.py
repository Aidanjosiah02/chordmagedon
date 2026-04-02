from enum import Enum
from pathlib import Path
from re import compile

class Quality(Enum):
    MAJOR = 0
    MINOR = 1
    SUS2 = 2
    SUS4 = 3
    POWER = 4
    AUGMENTED = 5
    DIMINISHED = 6

class SeventhType(Enum):
    NONE = 0
    DOMINANT = 1
    MAJOR = 2
    DIMINISHED = 3

class Part(Enum):
    CHORDS = 0
    BASS = 1
    MELODY = 2
    DRUMS = 3

EXCLUSIONS = {
    (Quality.MAJOR, SeventhType.DIMINISHED),
    (Quality.MINOR, SeventhType.DIMINISHED),
    (Quality.AUGMENTED, SeventhType.DIMINISHED),
    (Quality.SUS2, SeventhType.DIMINISHED),
    (Quality.SUS4, SeventhType.DIMINISHED),
}

NOTE_MAP = {'C': 0, 'Cs': 1, 'Db': 1, 'D': 2, 'Ds': 3, 'Eb': 3, 'E': 4, 'F': 5, 'Fs': 6, 'Gb': 6, 'G': 7, 'Gs': 8, 'Ab': 8, 'A': 9, 'As': 10, 'Bb': 10, 'B': 11}

VOCAB_SIZE = len([
    (root, quality, seventhType) 
    for root in set(NOTE_MAP.values()) 
    for quality in Quality 
    for seventhType in SeventhType 
    if (quality, seventhType) not in EXCLUSIONS
])

CHORD_REGEX = compile(r'^(?P<root>[A-G](?:s(?!us)|b)?)(?P<quality>min|no3d|aug|dim)?(?P<extension>(?:maj)?[bs]?(?:7|9|11|13|15|17)(?:[bs](?![0-9]))?)?(?P<remainder>.*)$')

SECTION_REGEX = r'(<[^>]+>)'
EXTENSION_REGEX = r'\d'

QUALITY_ENUM_MAP: dict[str|None, Quality] = {
    None: Quality.MAJOR,
    'min': Quality.MINOR,
    'sus2': Quality.SUS2,
    'sus4': Quality.SUS4,
    'no3d': Quality.POWER,
    'aug': Quality.AUGMENTED,
    'dim': Quality.DIMINISHED
}

DATA_DIR = Path("data")
LOG_DIR = Path("logs")
PROCESSED_DIR = Path("processed")

DATASET = DATA_DIR / "chordonomicon_v2.csv"

ARRANGEMENT_LOG = "arrangements.log"
ARRANGEMENT_PICKLE = "arrangements.pkl"
MARKOV_LOG_SUFFIX = "markov_chords.log"
MARKOV_PICKLE_SUFFIX = "markov_chords.pkl"

CHORD_TRANSITION_INFLUENCE = 0.5

GENERATIONS = 1000
POPULATION_SIZE = 95000
MUTATION_RATE = 0.05


# Chord types extracted during testing:
# {'', 'minadd13', '13', 'dim9', '7sus4', 'maj13', '13b9', '7b9', 'dim', 'add13', 'minmaj9', 'majs911s', 'min9', '13b', 'maj9', 'minadd11', 'maj1311s', 'dim13b9', 'maj11', 'sus4', 'maj7sus2', 'majs9', 'maj911s', 'dimb9', '9', 'minmaj7', 'add11', 'maj7', 'dim7', 'augmaj9', 'aug', 'maj7sus4', '11b9', 'min11', 'min13', '11', 'minadd9', 'min7', 'add9', '7sus2', '11s', 'minmaj11', 'min', 'dimb7', 'augmaj7', 'sus2', 'no3d', '7'}