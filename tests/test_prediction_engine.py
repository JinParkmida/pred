from pred.models.poisson import match_probabilities, poisson_probability
from pred.models.types import Match, SourceVerdict, Team
from pred.odds.convert import decimal_to_implied_probability, expected_value
from pred.verdicts.consensus import combine


def test_poisson_probability_known_zero_goal_case():
    assert round(poisson_probability(0, 1.5), 6) == 0.22313


def test_match_probabilities_normalize():
    probabilities = match_probabilities(1.4, 1.1)
    assert round(probabilities.home + probabilities.draw + probabilities.away, 6) == 1.0
    assert probabilities.home > probabilities.away


def test_consensus_combines_source_verdicts():
    match = Match(Team("Denmark"), Team("Korea Republic"))
    verdicts = [
        SourceVerdict("elo", "elo", match_probabilities(1.3, 1.0), "rating gap"),
        SourceVerdict("poisson", "poisson", match_probabilities(1.5, 1.1), "goal model"),
    ]
    consensus = combine(match, verdicts)
    assert len(consensus.verdicts) == 2
    assert consensus.probabilities.home > consensus.probabilities.away
    assert consensus.disagreement >= 0


def test_odds_helpers():
    assert decimal_to_implied_probability(2.0) == 0.5
    assert round(expected_value(0.55, 2.0), 6) == 0.1

from pred.evaluation.metrics import brier_score, log_loss
from pred.models.types import Outcome, ProbabilitySet


def test_evaluation_metrics_reward_confident_correct_predictions():
    strong = ProbabilitySet(0.8, 0.1, 0.1)
    weak = ProbabilitySet(0.4, 0.3, 0.3)
    assert log_loss(strong, Outcome.HOME) < log_loss(weak, Outcome.HOME)
    assert brier_score(strong, Outcome.HOME) < brier_score(weak, Outcome.HOME)
