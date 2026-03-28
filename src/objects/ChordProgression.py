from dataclasses import dataclass
import random
from src.objects.Chord import Chord

@dataclass(slots=True)
class ChordProgression:
    chords: list[Chord]
    root: int = 0
    fitness: float = 0.0

    # def __post_init__(self):
    #     self._find_key()

    # def _find_key(self):
    #     pass

    def mutate(self, mutation_power: float = 0.1):
        for index in range(len(self.chords)):
            if random.random() < mutation_power:
                pass

    def evaluate_fitness():
        pass

    def to_midi():
        pass
