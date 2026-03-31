from src.objects.Arrangement import Arrangement
from src.types import Chain, ChordTuple, Key

def build_markov_chords(arrangements: list[Arrangement]):
    chain: Chain = {}
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

# Additive smoothing for converting occurrences to scores.
# An optional non-linear flag for boosting rare chord progressions.
def additive_smoothing(count: int, trials: int, dimensions: int, pseudocount: float, non_linear: bool):
    dimension_weight = pseudocount * dimensions
    if non_linear:
        dimension_weight = dimension_weight * (count/trials)
    numerator = count + pseudocount
    denominator = trials + dimension_weight
    print(str(numerator) + " / " + str(denominator))
    return numerator/denominator

def get_markov_score(markov_chain: Chain, context: Key, transition_target: ChordTuple, transition_influence: float = 0.5) -> float:
    transition_dict = markov_chain[context]
    print(transition_dict)
    transition_occurrence: int = transition_dict[transition_target]
    print(transition_occurrence)
    transition_total: int = sum(transition_dict.values())
    print(transition_total)
    # return additive_smoothing(transition_occurrence, transition_total, ADDITIVE_SMOOTHING_VOCABULARY, ADDITIVE_SMOOTHING_VALUE, False)

    # Provide a tiny non-zero floor for the GA
    relative_freq = transition_occurrence / transition_total

    score = 1 - (1 / (1 + 100 * relative_freq * transition_influence))
    
    return score