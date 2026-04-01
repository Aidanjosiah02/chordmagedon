from dataclasses import dataclass
import random
from src.objects.Markov import Markov
from src.constants import CHORD_TRANSITION_INFLUENCE
from src.objects.Chord import Chord
from src.types import ChordTuple

@dataclass(slots=True)
class ChordProgression:
    chords: list[Chord]
    root: int = 0
    fitness: float = 0

    def evaluate_fitness(self, markovs: list[Markov]) -> float:
        if not self.chords:
            return 0.0

        chord_tuples = self.to_tuples()
        num_chords = len(chord_tuples)
        num_markovs = len(markovs)
        
        total_progression_score = 0.0
        for index in range(num_chords):
            score = 0.0
            for markov in markovs:
                score += markov.get_score(chord_tuples, index, CHORD_TRANSITION_INFLUENCE)
            # Average score from different Markov chain orders
            total_progression_score += (score / num_markovs)
        self.fitness = total_progression_score / num_chords
        return self.fitness

    def to_tuples(self) -> list[ChordTuple]:
        return [chord.to_tuple() for chord in self.chords]
    
    def mutate(self, mutation_power: float = 0.1):
        for index in range(len(self.chords)):
            if random.random() < mutation_power:
                pass
