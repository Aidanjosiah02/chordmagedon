from typing import TYPE_CHECKING
from src.constants import Part
from src.types import Chain, Key, ChordTuple

if TYPE_CHECKING:
    from src.objects.Arrangement import Arrangement

class Markov:
    def __init__(self, order: int, part: Part):
        self.chain: Chain = {}
        self.order = order
        self.part = part

    def build(self, arrangements: list["Arrangement"]):
        sequences = [arrangement.progression.to_tuples() for arrangement in arrangements]
        self.build_from_sequences(sequences)
    
    # this is an approach taht lets the object act more stupid.
    # pass in a sequence of tuples rather than have it figure out the Arrangement class.
    def build_from_sequences(self, sequences: list[list[ChordTuple]]):
        for sequence in sequences:
            for index in range(len(sequence) - self.order):
                context = tuple(sequence[index : index + self.order])
                target = sequence[index + self.order]
                if context not in self.chain:
                    # initialize empty key entry
                    self.chain[context] = {}
                # key entry guaranteed to exist
                target_dict = self.chain[context]
                # get() finds value stored or returns 0 if nothing found. Always add 1.
                # initializes target chord key automatically if not exists and stores it there.
                target_dict[target] = target_dict.get(target, 0) + 1

    def get_score(self, sequence: list[ChordTuple], index: int, influence: float = 0.5) -> float:
        if index + self.order >= len(sequence):
            return 0.0
        
        context: Key
        if self.order == 1:
            context = (sequence[index],)
        else:
            context = tuple(sequence[index : index + self.order])
        
        target = sequence[index + self.order]
        transition_dict = self.chain.get(context)     
        if not transition_dict:
            return 0.0
        count = transition_dict.get(target, 0)
        if count == 0:
            return 0.0

        total: int = sum(transition_dict.values())
        relative_freq = count / total
        return 1 - (1 / (1 + 100 * relative_freq * influence))
    
    def get_entry_by_key(self, key: Key) -> dict[ChordTuple, int]:
        return self.chain.get(key, {})
    
    # Iterator that yields (context, transitions) pairs one by one.
    def __iter__(self):
        for context, transitions in self.chain.items():
            yield context, transitions

    def __len__(self) -> int:
        return len(self.chain)
    