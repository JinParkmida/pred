"""Known data and model source registry.

The registry keeps source metadata explicit before adapters download or parse
anything. This lets reports explain where every verdict came from.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SourceDefinition:
    name: str
    url: str
    purpose: str
    adapter: str | None = None


DEFAULT_SOURCES: tuple[SourceDefinition, ...] = (
    SourceDefinition(
        "international_results",
        "https://github.com/martj42/international_results",
        "Historical men's international football match results.",
        "pred.ingest.international_results",
    ),
    SourceDefinition(
        "worldcup",
        "https://github.com/jfjelstul/worldcup",
        "Historical FIFA World Cup matches, squads, and tournament data.",
        "pred.ingest.worldcup_history",
    ),
    SourceDefinition(
        "statsbomb_open_data",
        "https://github.com/statsbomb/open-data",
        "Open event-level data for selected competitions and matches.",
        "pred.ingest.statsbomb",
    ),
    SourceDefinition(
        "soccerdata",
        "https://github.com/probberechts/soccerdata",
        "Python library for retrieving public football datasets from multiple providers.",
        "pred.ingest.soccerdata_sources",
    ),
)
