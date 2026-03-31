from dataclasses import dataclass
from src.constants import EXCLUSIONS, Quality, SeventhType

@dataclass(frozen=True, slots=True)
class Chord:
    root: int
    quality: Quality
    seventhType: SeventhType
    remainders: str

    def __post_init__(self):
        self._validate_root()
        self._validate_chord()

    def _validate_root(self):
        if not (0 <= self.root <= 11):
            raise ValueError(f"Root must be 0-11. Got {self.root}")

    def _validate_chord(self):
        if (self.quality, self.seventhType) in EXCLUSIONS:
            raise ValueError(f"Incompatible combination: {self.quality.name} and {self.seventhType.name}")
        
    def to_tuple(self) -> tuple[int, int, int]:
        return (self.root, self.quality.value, self.seventhType.value)
