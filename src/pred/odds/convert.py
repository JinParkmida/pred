"""Odds conversion utilities."""

from __future__ import annotations


def decimal_to_implied_probability(decimal_odds: float) -> float:
    if decimal_odds <= 1.0:
        raise ValueError("decimal odds must be greater than 1")
    return 1.0 / decimal_odds


def expected_value(model_probability: float, decimal_odds: float) -> float:
    if not 0.0 <= model_probability <= 1.0:
        raise ValueError("model_probability must be between 0 and 1")
    return model_probability * decimal_odds - 1.0
