from enum import Enum

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

# For all "add" notes, keep an array.

CHORD_REGEX = r'^([A-G](?:s(?!us)|b)?)(.*)$'
CHORD_REGEX2 = r'^((?:(min|no3d|aug|dim))?)(.*)$'
CHORD_REGEX3 = r'^((?:((maj)?(b|s)?(7|9|11|13|15|17){1}(b$|s$)?))?)(.*)$'

SECTION_REGEX = r'(<[^>]+>)'

EXTENSION_REGEX = r'\d'

NOTE_MAP = {'C': 0, 'Cs': 1, 'Db': 1, 'D': 2, 'Ds': 3, 'Eb': 3, 'E': 4, 'F': 5, 'Fs': 6, 'Gb': 6, 'G': 7, 'Gs': 8, 'Ab': 8, 'A': 9, 'As': 10, 'Bb': 10, 'B': 11}

QUALITY_ENUM_MAP = {
    '': Quality.MAJOR,
    'min': Quality.MINOR,
    'sus2': Quality.SUS2,
    'sus4': Quality.SUS4,
    'no3d': Quality.POWER,
    'aug': Quality.AUGMENTED,
    'dim': Quality.DIMINISHED
}

# {'', 'minadd13', '13', 'dim9', '7sus4', 'maj13', '13b9', '7b9', 'dim', 'add13', 'minmaj9', 'majs911s', 'min9', '13b', 'maj9', 'minadd11', 'maj1311s', 'dim13b9', 'maj11', 'sus4', 'maj7sus2', 'majs9', 'maj911s', 'dimb9', '9', 'minmaj7', 'add11', 'maj7', 'dim7', 'augmaj9', 'aug', 'maj7sus4', '11b9', 'min11', 'min13', '11', 'minadd9', 'min7', 'add9', '7sus2', '11s', 'minmaj11', 'min', 'dimb7', 'augmaj7', 'sus2', 'no3d', '7'}

# {'', 'aug', 'sus4', 'dim', 'min', 'no3d', 'sus2'}
# {'', 'b9', 'maj7', 'add9', '11b9', 'maj1311s', '7sus4', 'maj7sus2', '11s', '13b', '7b9', '11', 'add13', 'majs911s', '7sus2', 'maj7sus4', '13b9', 'maj911s', 'maj11', '13', 'b7', 'add11', '9', 'majs9', 'maj13', 'maj9', '7'}

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

class TriadQuality(Enum):
    MAJOR = [0, 4, 7]
    MINOR = [0, 3, 7]
    DIMINISHED = [0, 3, 6]
    AUGMENTED = [0, 4, 8]
    SUS2 = [0, 2, 7]
    SUS4 = [0, 5, 7]

# {'', 'minadd13', '13', 'dim9', '7sus4', 'maj13', '13b9', '7b9', 'dim', 'add13', 'minmaj9', 'majs911s', 'min9', '13b', 'maj9', 'minadd11', 'maj1311s', 'dim13b9', 'maj11', 'sus4', 'maj7sus2', 'majs9', 'maj911s', 'dimb9', '9', 'minmaj7', 'add11', 'maj7', 'dim7', 'augmaj9', 'aug', 'maj7sus4', '11b9', 'min11', 'min13', '11', 'minadd9', 'min7', 'add9', '7sus2', '11s', 'minmaj11', 'min', 'dimb7', 'augmaj7', 'sus2', 'no3d', '7'}