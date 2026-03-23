from dataclasses import dataclass
from src.constants import Quality, SeventhType

@dataclass(frozen=True, slots=True)
class Chord:
    _EXCLUSIONS = {
        (Quality.MAJOR, SeventhType.DIMINISHED),
        (Quality.MINOR, SeventhType.DIMINISHED),
        (Quality.AUGMENTED, SeventhType.DIMINISHED),
        (Quality.SUS2, SeventhType.DIMINISHED),
        (Quality.SUS4, SeventhType.DIMINISHED),
    }
    root: int
    quality: Quality
    seventhType: SeventhType
    remainders: str
    bass: int

    def __post_init__(self):
        self._validate_root()
        self._validate_chord()

    def _validate_root(self):
        if not (0 <= self.root <= 11):
            raise ValueError(f"Root must be 0-11. Got {self.root}")

    def _validate_chord(self):
        if (self.quality, self.seventhType) in self._EXCLUSIONS:
            raise ValueError(f"Incompatible combination: {self.quality.name} and {self.seventhType.name}")
