from src.objects.Arrangement import Arrangement
from src.types import SecondChain, FirstChain

def build_second_markov_chords(arrangements: list[Arrangement]):
    chain: SecondChain = {}
    for arrangement in arrangements:  
        chord_progression = arrangement.progression.to_tuples()
        chord_progression_length = len(chord_progression)
        for index in range(chord_progression_length):
            if chord_progression_length > (index + 2):
                key = (chord_progression[index], chord_progression[index + 1])
                value = chord_progression[index + 2]
                if key not in chain:
                    chain[key] = {value: 1}
                elif value not in chain[key]:
                    chain[key].update({value: 1})
                else:
                    chain[key][value] += 1
    return chain

def build_first_markov_chords(arrangements: list[Arrangement]):
    chain: FirstChain = {}
    for arrangement in arrangements:  
        chord_progression = arrangement.progression.to_tuples()
        chord_progression_length = len(chord_progression)
        for index in range(chord_progression_length):
            if chord_progression_length > (index + 1):
                key = chord_progression[index]
                value = chord_progression[index + 1]
                if key not in chain:
                    chain[key] = {value: 1}
                elif value not in chain[key]:
                    chain[key].update({value: 1})
                else:
                    chain[key][value] += 1
    return chain


from src.objects.Arrangement import Arrangement
from src.types import SecondChain, FirstChain

class MarkovBuilder:
    @classmethod
    def build(cls, arrangements: list[Arrangement], order: int = 1):
        chain = {}
        for arrangement in arrangements:
            chords = arrangement.progression.to_tuples()
            for i in range(len(chords) - order):
                state = chords[i] if order == 1 else tuple(chords[i : i + order])
                next_chord = chords[i + order]
                if state not in chain:
                    chain[state] = {}
                chain[state][next_chord] = chain[state].get(next_chord, 0) + 1
        return chain