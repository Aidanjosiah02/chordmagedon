from dataclasses import dataclass
from .chord_progression import ChordProgression


@dataclass(slots=True)
class Arrangement:
    progression: ChordProgression

    def validate(self):
        if self.progression is None or not self.progression.chords:
            raise ValueError(
                "Arrangement must contain a valid chord progression"
            )

    def fitness():
        return self.progression.fitness()
