from dataclasses import dataclass
from src.constants import BASE_CHORD_WEIGHT, EXCLUSIONS, NOTE_POSITIONS, OCTAVE_NOTE_COUNT, POSITION_WEIGHTS, Quality, SeventhType
from src.types import ChordTuple

@dataclass(slots=True)
class Chord:
    root: int
    quality: Quality
    seventhType: SeventhType = SeventhType.NONE
    remainders: str = ""

    def __hash__(self):
        return hash((self.root, self.quality, self.seventhType))

    def __post_init__(self):
        self._validate_root()
        self._validate_chord()

    def _validate_root(self):
        if not (0 <= self.root < OCTAVE_NOTE_COUNT):
            raise ValueError(f"Root must be 0-{OCTAVE_NOTE_COUNT - 1}. Got {self.root}")

    def _validate_chord(self):
        if (self.quality, self.seventhType) in EXCLUSIONS:
            raise ValueError(f"Incompatible combination: {self.quality.name} and {self.seventhType.name}")
        
    def get_note_weights(self) -> list[int]:
        weights = [0] * OCTAVE_NOTE_COUNT
        intervals = NOTE_POSITIONS[self.quality.value]
        
        for index, interval in enumerate(intervals):
            note = (self.root + interval) % OCTAVE_NOTE_COUNT
            # Base weight for being in the chord
            weights[note] += BASE_CHORD_WEIGHT
            # Add extra weight if index is 0 (Root) or 2 (Fifth)
            if index < len(POSITION_WEIGHTS):
                weights[note] += POSITION_WEIGHTS[index]
        return weights

    def transpose(self, steps: int) -> None:
        self.root = (self.root + steps) % OCTAVE_NOTE_COUNT
        
    def to_tuple(self) -> ChordTuple:
        return (self.root, self.quality.value, self.seventhType.value)
