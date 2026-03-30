import pickle
from src.constants import PICKLE
from src.objects.Arrangemment import Arrangement

arrangements: list[Arrangement] = []
with open(PICKLE, 'rb') as file:
    arrangements = pickle.load(file)

def generate_markov_chord_occurence(arrangements: list[Arrangement]):
    chain: dict[tuple[tuple[int,int,int], tuple[int,int,int]], dict[tuple[int,int,int], int]] = {}
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

print(generate_markov_chord_occurence(arrangements))