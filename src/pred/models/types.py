"""Shared domain types for football predictions."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from enum import Enum
from typing import Any


class Outcome(str, Enum):
    """Three-way football match outcomes."""

    HOME = "home"
    DRAW = "draw"
    AWAY = "away"


@dataclass(frozen=True)
class Team:
    name: str
    fifa_code: str | None = None


@dataclass(frozen=True)
class Match:
    home: Team
    away: Team
    played_on: date | None = None
    home_goals: int | None = None
    away_goals: int | None = None
    neutral: bool = True
    source: str = "manual"

    @property
    def is_result(self) -> bool:
        return self.home_goals is not None and self.away_goals is not None


@dataclass(frozen=True)
class ProbabilitySet:
    home: float
    draw: float
    away: float

    def normalized(self) -> "ProbabilitySet":
        total = self.home + self.draw + self.away
        if total <= 0:
            raise ValueError("probabilities must sum to a positive value")
        return ProbabilitySet(self.home / total, self.draw / total, self.away / total)

    def as_dict(self) -> dict[str, float]:
        return {"home": self.home, "draw": self.draw, "away": self.away}


@dataclass(frozen=True)
class SourceVerdict:
    source: str
    model: str
    probabilities: ProbabilitySet
    explanation: str
    features: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass(frozen=True)
class ConsensusVerdict:
    match: Match
    verdicts: tuple[SourceVerdict, ...]
    probabilities: ProbabilitySet
    disagreement: float
