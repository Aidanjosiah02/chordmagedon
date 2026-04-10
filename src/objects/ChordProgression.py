from dataclasses import dataclass
import random
from src.objects.Markov import Markov
from src.constants import CHORD_TRANSITION_INFLUENCE, OCTAVE_NOTE_COUNT, SCALE_MASK
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
    
    def get_chords(self) -> list[Chord]:
        return self.chords
    
    def get_root(self) -> int:
        return self.root
    
    def _get_all_note_weights(self) -> list[int]:
        total_weights = [0] * OCTAVE_NOTE_COUNT
        for chord in self.chords:
            chord_weights = chord.get_note_weights()
            for note, weight in enumerate(chord_weights):
                total_weights[note] += weight
        return total_weights

    def normalize(self) -> None:
        note_occurrence = self._get_all_note_weights()
        
        best_score = -1
        best_shift = 0
        for shift in range(OCTAVE_NOTE_COUNT):
            score = 0
            for index in range(OCTAVE_NOTE_COUNT):
                score += note_occurrence[(index + shift) % OCTAVE_NOTE_COUNT] * SCALE_MASK[index]
                
            if score > best_score:
                best_score = score
                best_shift = shift
        
        self.root = best_shift

        if best_shift != 0:
            for chord in self.chords:
                chord.transpose(-best_shift)
