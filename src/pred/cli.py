"""Command-line interface for the prediction engine."""

from __future__ import annotations

import argparse

from pred.models.poisson import match_probabilities
from pred.models.types import Match, SourceVerdict, Team
from pred.reporting.markdown import render_consensus
from pred.verdicts.consensus import combine


def demo() -> str:
    match = Match(Team("Denmark", "DEN"), Team("Korea Republic", "KOR"))
    verdict = SourceVerdict(
        source="demo",
        model="poisson",
        probabilities=match_probabilities(1.45, 1.10),
        explanation="Demo Poisson verdict using illustrative expected goals.",
        features={"home_xg": 1.45, "away_xg": 1.10},
    )
    return render_consensus(combine(match, [verdict]))


def main() -> None:
    parser = argparse.ArgumentParser(description="Transparent football prediction engine")
    parser.add_argument("command", choices=["demo"], help="command to run")
    args = parser.parse_args()
    if args.command == "demo":
        print(demo())


if __name__ == "__main__":
    main()
