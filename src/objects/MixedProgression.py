from dataclasses import dataclass
from src.objects.Chord import Chord


@dataclass(slots=True)
class MixedProgression:
    chords: list[Chord | None]
    root: int = 0

    def __len__(self) -> int:
        return len(self.chords)
    
    def __getitem__(self, index: int) -> Chord | None:
        return self.chords[index]
    
    def __setitem__(self, key: int, value: Chord) -> None:
        self.chords[key] = value

    # def to_tuples(self) -> list[ChordTuple | None]:
    #     return [chord.to_tuple() for chord in self.chords if chord is not None else None]

    def get_chords(self) -> list[Chord | None]:
        return self.chords

    def get_root(self) -> int:
        return self.root

    def transpose(self, steps: int) -> None:
        for chord in self.chords:
            if chord is not None:
                chord.transpose(steps)

