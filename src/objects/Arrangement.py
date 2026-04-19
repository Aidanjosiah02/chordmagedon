from dataclasses import dataclass
from src.constants import Part
from src.objects.Markov import Markov
from .ChordProgression import ChordProgression
from .Chord import Chord
from .BassLine import BassLine


@dataclass(slots=True)
class Arrangement:
    progression: ChordProgression
    bassline: BassLine
    fitness: float = 0

    def evaluate_fitness(self, markovs: list[Markov], starting_chords: list[Chord]):
        chord_markovs = [markov for markov in markovs if markov.part == Part.CHORDS]
        # bass_markovs = [markov for markov in markovs if markov.part == Part.BASS]
        chord_fitness = self.progression.evaluate_fitness(chord_markovs, starting_chords)
        bass_fitness = self.bassline.evaluate_fitness(self.progression.get_chords())
        # print("bass: ", bass_fitness, ". chord: ", chord_fitness)
        self.fitness = (3/5 * chord_fitness + 2/5 * bass_fitness)
        return self.fitness

    def get_progression(self) -> ChordProgression:
        return self.progression

    def get_bassline(self) -> BassLine:
        return self.bassline
    
    def get_fitness(self) -> float:
        return self.fitness

    def normalize(self) -> None:
        self.progression.normalize()
        self.bassline.transpose(-self.progression.get_root())

    def transpose(self, steps: int) -> None:
        self.progression.transpose(steps)
        self.bassline.transpose(steps)
