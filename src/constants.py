from enum import Enum

class Alterations(Enum):
    DIMINISHED = 0
    AUGMENTED = 1

class Quality(Enum):
    MAJOR = 0
    MINOR = 1

class Type(Enum):
    TRIAD = 0
    POWER = 1
    SUS2 = 2
    SUS4 = 3
    SEVENTH = 4
    NINTH = 5
    ELEVENTH = 6
    THIRTEENTH = 7

CHORD_REGEX = r'^([A-G](?:s(?!us)|b)?)(.*)$'
SECTION_REGEX = r'(<[^>]+>)'

NOTE_MAP = {'C': 0, 'Cs': 1, 'Db': 1, 'D': 2, 'Ds': 3, 'Eb': 3, 'E': 4, 'F': 5, 'Fs': 6, 'Gb': 6, 'G': 7, 'Gs': 8, 'Ab': 8, 'A': 9, 'As': 10, 'Bb': 10, 'B': 11}

QUALITY_MAP = {
    'min': Quality.MINOR,
    'm': Quality.MINOR,
    'maj': Quality.MAJOR,
    '': Quality.MAJOR
}

TYPE_MAP = {
    'sus2': Type.SUS2,
    'sus4': Type.SUS4,
    '7': Type.SEVENTH,
    '9': Type.NINTH,
    '13': Type.THIRTEENTH,
    '': Type.TRIAD
}

# class Dictionary(Enum):
#     FLAT = 'b'
#     SHARP = 's'
#     MINOR = 'min'
#     MAJOR = 'maj'
#     SEVENTH = '7'
#     SUS2 = 'sus2'
#     SUS4 = 'sus4'
#     POWER = 'no3d'
#     ADD9 = 'add9'
#     ADD11 = 'add11'
#     ADD13 = 'add13' 