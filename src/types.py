from typing import TypeAlias

ChordTuple: TypeAlias = tuple[int, int, int]
SecondKey: TypeAlias = tuple[ChordTuple, ChordTuple]
FirstKey: TypeAlias = ChordTuple
Key: TypeAlias = FirstKey | SecondKey
FirstChain: TypeAlias = dict[FirstKey, dict[ChordTuple, int]]
SecondChain: TypeAlias = dict[SecondKey, dict[ChordTuple, int]]
# Chain: TypeAlias = dict[Key, dict[ChordTuple, int]]

Chain: TypeAlias = dict[Key, dict[ChordTuple, int]]