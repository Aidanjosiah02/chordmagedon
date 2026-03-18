from src.constants import Alterations, Quality, Type

class Chord:
    def __init__(self, root: int, alts: Alterations, quality: Quality, chord_type: Type):
        self.root = root
        self.alts = alts
        self.quality = quality
        self.type = chord_type
        self._validate_root()
        self._validate_chord()

    def _validate_root(self):
        if not (0 <= self.root <= 11):
            raise ValueError(f"Root must be 0-11. Got {self.root}")

    def _validate_chord(self):
        exclusions = {
            (Alterations.AUGMENTED, Quality.MINOR),
            (Alterations.DIMINISHED, Quality.MAJOR),
        }
        if (self.quality, self.type) in exclusions:
            raise ValueError(f"Incompatible combination: {self.quality.name} and {self.type.name}")
        

    