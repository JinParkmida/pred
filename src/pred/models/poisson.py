"""Poisson goal model helpers."""

from __future__ import annotations

from math import exp, factorial

from pred.models.types import ProbabilitySet


def poisson_probability(goals: int, expected_goals: float) -> float:
    if goals < 0:
        raise ValueError("goals cannot be negative")
    if expected_goals <= 0:
        raise ValueError("expected_goals must be positive")
    return exp(-expected_goals) * expected_goals**goals / factorial(goals)


def match_probabilities(home_xg: float, away_xg: float, max_goals: int = 10) -> ProbabilitySet:
    home = draw = away = 0.0
    for home_goals in range(max_goals + 1):
        hp = poisson_probability(home_goals, home_xg)
        for away_goals in range(max_goals + 1):
            p = hp * poisson_probability(away_goals, away_xg)
            if home_goals > away_goals:
                home += p
            elif home_goals == away_goals:
                draw += p
            else:
                away += p
    return ProbabilitySet(home, draw, away).normalized()
