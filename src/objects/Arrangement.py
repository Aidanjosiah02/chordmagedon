from dataclasses import dataclass

from src.types import FirstChain, SecondChain
from .ChordProgression import ChordProgression
from .Bassline import BassLine


@dataclass(slots=True)
class Arrangement:
    progression: ChordProgression
    bassline: BassLine
    fitness: float = 0

    def validate(self):
        if self.progression is None or not self.progression.chords:
            raise ValueError(
                "Arrangement must contain a valid chord progression"
            )

    def evaluate_fitness(self, first_markov: FirstChain, second_markov: SecondChain):
        self.fitness = self.progression.evaluate_fitness(first_markov, second_markov) 
            # + self.bassline.evaluate_fitness(self.progression)
        return self.fitness
    
    def get_progression(self) -> ChordProgression:
        return self.progression
