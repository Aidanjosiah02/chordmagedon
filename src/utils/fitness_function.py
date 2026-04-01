from src.types import ChordTuple, Chain, Key

def get_markov_score(markov_chain: Chain, context: Key, transition_target: ChordTuple, transition_influence: float = 0.5) -> float:
    transition_dict = markov_chain[context]
    transition_occurrence: int = transition_dict[transition_target]
    transition_total: int = sum(transition_dict.values())
    relative_freq = transition_occurrence / transition_total
    score = 1 - (1 / (1 + 100 * relative_freq * transition_influence))
    return score

