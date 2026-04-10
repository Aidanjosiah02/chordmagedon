from dataclasses import dataclass

from src.constants import OCTAVE_NOTE_COUNT

VALID_NASHVILLE_NUMBERS = set(range(0, 12))


@dataclass(slots=True)
class BassLine:
    notes: list[int]

    def __post_init__(self):
        for n in self.notes:
            if n not in VALID_NASHVILLE_NUMBERS:
                raise ValueError(f"Invalid note number: {n}. Must be 0-11.")

    def evaluate_fitness(self):
        pass

    def to_midi(self):
        pass

    def get_notes(self):
        return self.notes
    
    def transpose(self, steps: int) -> None:
        self.notes = [((note + steps) % OCTAVE_NOTE_COUNT) for note in self.notes]

        
