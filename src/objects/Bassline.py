from dataclasses import dataclass

VALID_NASHVILLE_NUMBERS = set(range(1, 14))


@dataclass(slots=True)
class BassLine:
    notes: list[int]

    def __post_init__(self):
        for n in self.notes:
            if n not in VALID_NASHVILLE_NUMBERS:
                raise ValueError(f"Invalid note number: {n}. Must be 1–13.")

    def evaluate_fitness(self):
        pass

    def to_midi(self):
        pass

    def get_notes(self):
        return self.notes
