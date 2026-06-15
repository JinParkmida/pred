"""Consensus verdict aggregation."""

from __future__ import annotations

from statistics import pstdev

from pred.models.types import ConsensusVerdict, Match, ProbabilitySet, SourceVerdict


def combine(match: Match, verdicts: list[SourceVerdict], weights: dict[str, float] | None = None) -> ConsensusVerdict:
    if not verdicts:
        raise ValueError("at least one verdict is required")
    weights = weights or {}
    weighted_home = weighted_draw = weighted_away = total_weight = 0.0
    home_probs: list[float] = []
    for verdict in verdicts:
        weight = weights.get(verdict.source, 1.0)
        probs = verdict.probabilities.normalized()
        weighted_home += probs.home * weight
        weighted_draw += probs.draw * weight
        weighted_away += probs.away * weight
        total_weight += weight
        home_probs.append(probs.home)
    if total_weight <= 0:
        raise ValueError("total consensus weight must be positive")
    probabilities = ProbabilitySet(
        weighted_home / total_weight,
        weighted_draw / total_weight,
        weighted_away / total_weight,
    ).normalized()
    disagreement = pstdev(home_probs) if len(home_probs) > 1 else 0.0
    return ConsensusVerdict(match, tuple(verdicts), probabilities, disagreement)
