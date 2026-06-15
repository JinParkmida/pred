"""Evaluation metrics for prediction backtests."""

from __future__ import annotations

from math import log

from pred.models.types import Outcome, ProbabilitySet


def outcome_probability(probabilities: ProbabilitySet, outcome: Outcome) -> float:
    return probabilities.as_dict()[outcome.value]


def log_loss(probabilities: ProbabilitySet, outcome: Outcome, epsilon: float = 1e-15) -> float:
    probability = min(max(outcome_probability(probabilities.normalized(), outcome), epsilon), 1.0)
    return -log(probability)


def brier_score(probabilities: ProbabilitySet, outcome: Outcome) -> float:
    probs = probabilities.normalized().as_dict()
    return sum((probs[key] - (1.0 if key == outcome.value else 0.0)) ** 2 for key in probs)
