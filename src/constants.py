from enum import Enum
from itertools import product
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

    @classmethod
    def to_string(cls):
        all_members: list[str] = []
        for member in cls:
            all_members.append(f"{member.name}: {member.value}")
        return "\n".join(all_members)
    
    def __str__(self):
        return self.to_string()

class SeventhType(Enum):
    NONE = 0
    DOMINANT = 1
    MAJOR = 2
    DIMINISHED = 3

    @classmethod
    def to_string(cls):
        all_members: list[str] = []
        for member in cls:
            all_members.append(f"{member.name}: {member.value}")
        return "\n".join(all_members)
    
    def __str__(self):
        return self.to_string()

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
ALL_PAIRS = list(product(Quality, SeventhType))

ALLOWED_PAIRS_OF_QUALITY_AND_SEVENTH_TYPE = [
    (q, s) for (q, s) in ALL_PAIRS
    if (q, s) not in EXCLUSIONS
]

NOTE_MAP = {'C': 0, 'Cs': 1, 'Db': 1, 'D': 2, 'Ds': 3, 'Eb': 3, 'E': 4, 'F': 5, 'Fs': 6, 'Gb': 6, 'G': 7, 'Gs': 8, 'Ab': 8, 'A': 9, 'As': 10, 'Bb': 10, 'B': 11}

VOCAB_SIZE = len([
    (root, quality, seventhType)
    for root in set(NOTE_MAP.values())
    for quality in Quality
    for seventhType in SeventhType
    if (quality, seventhType) not in EXCLUSIONS
])

SCALE_INVALID = {
    "STANDARD": {1, 3, 6, 8, 10},
    "HARMONIC_MINOR": {1, 4, 6, 9, 10},
    "MELODIC_MINOR_ASC": {1, 4, 6, 8, 10},
    "DIMINISHED": {1, 4, 7, 10}
}

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

LOG = "logs/chords-v1.log"
PICKLE = "processed/chord_progressions.pk1"
DATA_DIR = Path("data")
LOG_DIR = Path("logs")
PROCESSED_DIR = Path("processed")

DATASET = DATA_DIR / "chordonomicon_v2.csv"

ARRANGEMENT_LOG = "arrangements.log"
ARRANGEMENT_PICKLE = "arrangements.pkl"
MARKOV_LOG_SUFFIX = "markov_chords.log"
MARKOV_PICKLE_SUFFIX = "markov_chords.pkl"

CHORD_TRANSITION_INFLUENCE = 0.5

GENERATIONS = 64
POPULATION_SIZE = 8192
MUTATION_RATE = 0.15
ELITE_RATIO = 0.2

NOTE_POSITIONS = {
    Quality.MAJOR.value: [0, 4, 7],
    Quality.MINOR.value: [0, 3, 7],
    Quality.SUS2.value: [0, 2, 7],
    Quality.SUS4.value: [0, 5, 7],
    Quality.POWER.value: [0, 7],
    Quality.AUGMENTED.value: [0, 4, 8],
    Quality.DIMINISHED.value: [0, 3, 6],
}

SEVENTH_POSITIONS = {
    SeventhType.NONE.value: [],
    SeventhType.DOMINANT.value: [10],
    SeventhType.MAJOR.value: [11],
    SeventhType.DIMINISHED.value: [9],
}



POSITION_WEIGHTS = [5, 0, 2] 
BASE_CHORD_WEIGHT = 2

# SCALE_MASK = [6, 0, 5, 0, 5, 5, 0, 6, 1, 6, 0, 5]
SCALE_MASK = [7, 0, 5, 0, 5, 5, 0, 6, 0, 7, 0, 5]

OCTAVE_NOTE_COUNT = 12


RESOLUTION_SCORE_TABLE = {
    (q1, q2): 50  # default score
    for q1, q2 in product(Quality, repeat=2)
}

# Punish diminished
for q1 in Quality:
    RESOLUTION_SCORE_TABLE[(q1, Quality.DIMINISHED)] = 20

# reward majors and minors
RESOLUTION_SCORE_TABLE[(Quality.MAJOR, Quality.MAJOR)] = 100
RESOLUTION_SCORE_TABLE[(Quality.DIMINISHED, Quality.MAJOR)] = 90
RESOLUTION_SCORE_TABLE[(Quality.SUS2, Quality.MAJOR)] = 80
RESOLUTION_SCORE_TABLE[(Quality.SUS4, Quality.MAJOR)] = 80
RESOLUTION_SCORE_TABLE[(Quality.MINOR, Quality.MAJOR)] = 70
RESOLUTION_SCORE_TABLE[(Quality.MAJOR, Quality.MINOR)] = 70
RESOLUTION_SCORE_TABLE[(Quality.AUGMENTED, Quality.MINOR)] = 60

# SCALE_INVALID_NOTES = {
#     "STANDARD": {1, 3, 6, 8, 10},
#     "HARMONIC_MINOR": {1, 4, 6, 9, 10},
#     "MELODIC_MINOR_ASC": {1, 4, 6, 8, 10},
#     "DIMINISHED": {1, 4, 7, 10}
# }

# SCALE_WEIGHTS = {
#     # Strong emphasis on Root(0), Mediant(4), and Dominant(7)
#     "STANDARD": [5, 0, 2, 0, 4, 1, 0, 4, 0, 2, 0, 2],
#     # Root(0), Minor 3rd(3), Perfect 5th(7), and the "Leading Tone" Major 7th(11)
#     "HARMONIC_MINOR": [5, 0, 2, 4, 0, 2, 0, 4, 2, 0, 0, 4],
#     # Root(0), Minor 3rd(3), and the bright Major 6th(9) + Major 7th(11)
#     "MELODIC_MINOR_ASC": [5, 0, 2, 4, 0, 2, 0, 4, 0, 3, 0, 3],
#     # Symmetric weighting: Equal emphasis on the diminished chords [0, 3, 6, 9]
#     "DIMINISHED": [4, 0, 2, 4, 0, 2, 4, 0, 2, 4, 0, 2]
# }





# Chord types extracted during testing:
# {'', 'minadd13', '13', 'dim9', '7sus4', 'maj13', '13b9', '7b9', 'dim', 'add13', 'minmaj9', 'majs911s', 'min9', '13b', 'maj9', 'minadd11', 'maj1311s', 'dim13b9', 'maj11', 'sus4', 'maj7sus2', 'majs9', 'maj911s', 'dimb9', '9', 'minmaj7', 'add11', 'maj7', 'dim7', 'augmaj9', 'aug', 'maj7sus4', '11b9', 'min11', 'min13', '11', 'minadd9', 'min7', 'add9', '7sus2', '11s', 'minmaj11', 'min', 'dimb7', 'augmaj7', 'sus2', 'no3d', '7'}
