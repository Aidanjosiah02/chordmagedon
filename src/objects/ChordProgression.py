from dataclasses import dataclass
import random
from src.objects.Markov import Markov
from src.constants import CHORD_TRANSITION_INFLUENCE, OCTAVE_NOTE_COUNT, SCALE_MASK
from src.objects.Chord import Chord
from src.types import ChordTuple
from src.constants import RESOLUTION_SCORE_TABLE
import math


@dataclass(slots=True)
class ChordProgression:
    chords: list[Chord]
    root: int = 0
    fitness: float = 0

    def evaluate_fitness(self, markovs: list[Markov], starting_chords: list[Chord]) -> float:
        if not self.chords:
            return 0.0

        chord_tuples = self.to_tuples()
        num_chords = len(chord_tuples)
        num_markovs = len(markovs)

        total_progression_score = 0.0

        # Check similarities to 80s music
        for index in range(num_chords):
            score = 0.0
            for markov in markovs:
                score += markov.get_score(chord_tuples,
                                          index, CHORD_TRANSITION_INFLUENCE)
            # Average score from different Markov chain orders
            total_progression_score += (score / num_markovs)
        fitness = (total_progression_score / num_chords)

        # Check song structure
        # We attempt to group the chord prog to reasonable phrases and average the score
        fitness += self.get_phrasing_average_score()

        fitness = fitness / 2

        # penalize overly duplication
        fitness = fitness * (1.0 - (0.2 * self.duplication_ratio()))

        # Penalize progressions not starting with our starting chords
        penalty = self.prefix_penalty(starting_chords)
        fitness -= penalty

        self.fitness = fitness
        return self.fitness

    def get_phrasing_average_score(self):
        phrase_lengths = [4, 5]
        scores = []

        for length in phrase_lengths:
            score = self.evaluate_phrase_of_length(length)
            scores.append(score)

        return sum(scores) / len(scores)

    def evaluate_phrase_of_length(self, length: int) -> float:
        total_score = 0.0
        transitions = 0
        repetition_penalty = 0.0

        for i in range(length, len(self.chords), length):
            prev_chord = self.chords[i - 1].quality
            curr_chord = self.chords[i].quality
            total_score += RESOLUTION_SCORE_TABLE[(prev_chord, curr_chord)]
            transitions += 1

            phrase_a = self.chords[i - length: i]
            phrase_b = self.chords[i: i + length]

            if len(phrase_a) == len(phrase_b):
                matches = sum(1 for a, b in zip(phrase_a, phrase_b)
                              if a.quality == b.quality)
                repetition_penalty += (matches / length) * 5.0

        if transitions == 0:
            return 0.0

        final_score = ((total_score / transitions) -
                       (repetition_penalty / transitions))
        return max(0.0, final_score / 100.0)

    def to_tuples(self) -> list[ChordTuple]:
        return [chord.to_tuple() for chord in self.chords]

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
        # Allows the Markov chain to impilcitly encode transition probabilities based on their pitch relative to the key of the chord progression.
        # Also may help crossovers be more consistent as all chord progressions will be of the same key before transposing.

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

    def duplication_ratio(self) -> float:
        if not self.chords:
            return 0.0
        unique_chords = {(c.root, c.quality, c.seventhType)
                         for c in self.chords}
        return 1 - (len(unique_chords) / len(self.chords))

    def prefix_penalty(self, starting_chords):
        penalty = 0.0
        length = min(len(starting_chords), len(self.chords))

        for i in range(length):
            a = self.chords[i]
            b = starting_chords[i]

            if a.root != b.root:
                penalty += 0.2
            if a.quality != b.quality:
                penalty += 0.1
            if a.seventhType != b.seventhType:
                penalty += 0.05

        return penalty / length if length > 0 else 0.0

