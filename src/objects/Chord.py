from dataclasses import dataclass
from src.constants import Quality, SeventhType

@dataclass
class Chord:
    def __init__(self, root: int, quality: Quality, seventhType: SeventhType, alterations: str):
        self.root = root
        self.quality = quality
        self.seventhType = seventhType
        self.alterations = alterations
        self._validate_root()
        self._validate_chord()

    def _validate_root(self):
        if not (0 <= self.root <= 11):
            raise ValueError(f"Root must be 0-11. Got {self.root}")

    def _validate_chord(self):
        exclusions = {
            (Quality.DIMINISHED, SeventhType.MAJOR),
            (Quality.AUGMENTED, SeventhType.DIMINISHED),
            (Quality.SUS2, SeventhType.DIMINISHED),
            (Quality.SUS4, SeventhType.DIMINISHED),
        }
        if (self.quality, self.seventhType) in exclusions:
            raise ValueError(f"Incompatible combination: {self.quality.name} and {self.seventhType.name}")
        

    