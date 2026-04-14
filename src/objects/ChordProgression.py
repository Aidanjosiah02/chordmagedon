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
                score += markov.get_score(chord_tuples,
                                          index, CHORD_TRANSITION_INFLUENCE)
            # Average score from different Markov chain orders
            total_progression_score += (score / num_markovs)
        fitness = total_progression_score / num_chords

        # penalize duplication
        fitness = fitness - (0.5 * self.duplication_ratio())

        self.fitness = fitness
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

    # Allows the Markov chain to impilcitly encode transition probabilities based on their pitch relative to the key of the chord progression. 
    # Also may help crossovers be more consistent as all chord progressions will be of the same key before transposing.
    def normalize(self) -> None:
        note_occurrence = self._get_all_note_weights()

        best_score = -1
        best_shift = 0
        for shift in range(OCTAVE_NOTE_COUNT):
            score = 0
            for index in range(OCTAVE_NOTE_COUNT):
                score += note_occurrence[(index + shift) %
                                         OCTAVE_NOTE_COUNT] * SCALE_MASK[index]

            if score > best_score:
                best_score = score
                best_shift = shift

        self.root = best_shift

        if best_shift != 0:
            for chord in self.chords:
                # As best_shift describes how many shifts the mask had to make to find the best match,
                # best_shift consequently describes how many semitones the current chord progression is ABOVE C, or, 0.
                # Therefore, to shift the chord progression down to 0, we must transpose DOWN by subtracting best_shift.
                chord.transpose(-best_shift)

    def transpose(self, steps: int) -> None:
        for chord in self.chords:
            chord.transpose(steps)
            
    def duplication_ratio(self) -> int:
        unique_count = len(set(self.chords))
        total_count = len(self.chords)
        return 1 - (unique_count / total_count)
