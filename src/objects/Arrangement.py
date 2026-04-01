from dataclasses import dataclass
from src.constants import Part
from src.objects.Markov import Markov
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

    def evaluate_fitness(self, markovs: list[Markov]):
        chord_markovs = [markov for markov in markovs if markov.part == Part.CHORDS]
        # bass_markovs = [markov for markov in markovs if markov.part == Part.BASS]
        chord_fitness = self.progression.evaluate_fitness(chord_markovs) 
        # bass_fitness = self.bassline.evaluate_fitness(bass_markovs)
        self.fitness = chord_fitness # + bass_fitness
        return self.fitness
    
    def get_progression(self) -> ChordProgression:
        return self.progression
