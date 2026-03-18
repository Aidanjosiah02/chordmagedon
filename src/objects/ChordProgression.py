import random

from objects.Chord import Chord

class ChordProgression:
    def __init__(self, input_chords: list[Chord], root:int=0):
        self.chords = input_chords
        self.root = root
        self.fitness = 0.0

    def mutate(self, mutation_power:float=0.1):
        for index in range(len(self.chords)):
            if random.random() < mutation_power:
                pass
    
    def get_fitness():
        pass

    def to_midi():
        pass
