from dataclasses import dataclass
import random
from src.constants import CHORD_TRANSITION_INFLUENCE
from src.objects.Chord import Chord
from src.utils.fitness_function import get_markov_score
from src.types import FirstChain, SecondChain

@dataclass(slots=True)
class ChordProgression:
    chords: list[Chord]
    root: int = 0
    fitness: float = 0

    # def __post_init__(self):
    #     self._find_key()

    # def _find_key(self):
    #     pass

    def mutate(self, mutation_power: float = 0.1):
        for index in range(len(self.chords)):
            if random.random() < mutation_power:
                pass

    def evaluate_fitness(self, first_markov: FirstChain, second_markov: SecondChain) -> float:
        scores: list[float] = []
        chords_length = len(self.chords)
        for index in range(chords_length):
            second_order_score: float = 0
            if chords_length > (index + 2):
                key = (self.chords[index].to_tuple(), self.chords[index + 1].to_tuple())
                value = self.chords[index + 2].to_tuple()
                second_order_score = get_markov_score(second_markov, key, value, CHORD_TRANSITION_INFLUENCE)
            first_order_score: float = 0
            if chords_length > (index + 1):
                key = self.chords[index].to_tuple()
                value = self.chords[index + 1].to_tuple()
                first_order_score = get_markov_score(first_markov, key, value, CHORD_TRANSITION_INFLUENCE)
            scores.append((second_order_score + first_order_score) / 2)   
        self.fitness = sum(scores) / len(scores)
        return self.fitness

    def to_midi():
        pass

    def to_tuples(self) -> list[tuple[int, int, int]]:
        return [chord.to_tuple() for chord in self.chords]
    
