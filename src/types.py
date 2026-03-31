from typing import TypeAlias

ChordTuple: TypeAlias = tuple[int, int, int]
Key: TypeAlias = tuple[ChordTuple, ChordTuple]
Chain: TypeAlias = dict[Key, dict[ChordTuple, int]]
