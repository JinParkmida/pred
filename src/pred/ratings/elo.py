"""Elo rating utilities for international football."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass

from pred.models.types import Match


@dataclass(frozen=True)
class EloConfig:
    base_rating: float = 1500.0
    k_factor: float = 30.0
    home_advantage: float = 60.0


class EloRatings:
    def __init__(self, config: EloConfig | None = None) -> None:
        self.config = config or EloConfig()
        self._ratings: defaultdict[str, float] = defaultdict(lambda: self.config.base_rating)

    def rating(self, team_name: str) -> float:
        return self._ratings[team_name]

    @staticmethod
    def expected_score(rating_a: float, rating_b: float) -> float:
        return 1.0 / (1.0 + 10.0 ** ((rating_b - rating_a) / 400.0))

    @staticmethod
    def actual_score(home_goals: int, away_goals: int) -> float:
        if home_goals > away_goals:
            return 1.0
        if home_goals == away_goals:
            return 0.5
        return 0.0

    def update(self, match: Match) -> None:
        if not match.is_result:
            raise ValueError("cannot update Elo from a match without a result")
        home_rating = self.rating(match.home.name)
        away_rating = self.rating(match.away.name)
        adjusted_home = home_rating + (0.0 if match.neutral else self.config.home_advantage)
        expected_home = self.expected_score(adjusted_home, away_rating)
        actual_home = self.actual_score(match.home_goals or 0, match.away_goals or 0)
        change = self.config.k_factor * (actual_home - expected_home)
        self._ratings[match.home.name] = home_rating + change
        self._ratings[match.away.name] = away_rating - change

    def fit(self, matches: list[Match]) -> "EloRatings":
        for match in sorted(matches, key=lambda item: item.played_on or __import__("datetime").date.min):
            if match.is_result:
                self.update(match)
        return self
