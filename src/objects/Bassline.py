from dataclasses import dataclass

from src.formulas import score_saturator
from src.objects.Chord import Chord
from src.objects.ChordProgression import ChordProgression
from src.constants import OCTAVE_NOTE_COUNT

VALID_NASHVILLE_NUMBERS = set(range(0, 12))


@dataclass(slots=True)
class BassLine:
    notes: list[int]

    def __post_init__(self):
        for n in self.notes:
            if n not in VALID_NASHVILLE_NUMBERS:
                raise ValueError(f"Invalid note number: {n}. Must be 0-11.")

    def evaluate_fitness(self, progression: ChordProgression) -> float:
        chords: list[Chord] = progression.get_chords();
        score = 0
        for chord, bass_note in zip(chords, self.notes):
            chord_weights = chord.get_note_weights() # Perhaps alter in future to take a parameter that changes to what degree it gives notes. Ex. 0 = triad, 1 = 7ths included, 2 = 7ths + all other extentions, 3 option 2 + additionals.

            # Choosing the max since those with equal weights at the max are both perfectly fit.
            score += score_saturator(max(chord_weights), chord_weights[bass_note])
        return score / len(chords)
    
    def to_midi(self):
        pass

    def get_notes(self):
        return self.notes
    
    def transpose(self, steps: int) -> None:
        self.notes = [((note + steps) % OCTAVE_NOTE_COUNT) for note in self.notes]

        
