


def score_saturator(max_value: int, value: int, influence: float = 0.5) -> float:
        relative_freq = value / max_value
        return 1 - (1 / (1 + 100 * relative_freq * influence))