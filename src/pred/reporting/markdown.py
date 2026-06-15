"""Markdown reporting for prediction verdicts."""

from __future__ import annotations

from pred.models.types import ConsensusVerdict


def render_consensus(verdict: ConsensusVerdict) -> str:
    probs = verdict.probabilities
    lines = [
        f"# {verdict.match.home.name} vs {verdict.match.away.name}",
        "",
        "## Overall verdict",
        f"- Home win: {probs.home:.1%}",
        f"- Draw: {probs.draw:.1%}",
        f"- Away win: {probs.away:.1%}",
        f"- Source disagreement: {verdict.disagreement:.3f}",
        "",
        "## Source verdicts",
    ]
    for source in verdict.verdicts:
        p = source.probabilities.normalized()
        lines.append(f"- **{source.source}/{source.model}**: {p.home:.1%} / {p.draw:.1%} / {p.away:.1%} — {source.explanation}")
    return "\n".join(lines)
