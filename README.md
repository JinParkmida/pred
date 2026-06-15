# pred

`pred` is a transparent football prediction engine scaffold for analysing the FIFA World Cup 2026. The project uses the word **football** in user-facing output while still accepting source names that use "soccer".

The engine is designed to combine:

- Historical international match results.
- World Cup history.
- Team-rating models such as Elo.
- Goal models such as Poisson and Dixon-Coles-style extensions.
- Third-party prediction verdicts with source provenance.
- Betting-market odds supplied by the user for mathematical value analysis.

## Helpful source repositories

These repositories are suitable inputs or references for adapters:

- `martj42/international_results` for international match history.
- `jfjelstul/worldcup` for historical World Cup data.
- `statsbomb/open-data` for event-level open data where available.
- `probberechts/soccerdata` for retrieving public football data from multiple providers.
- transparent World Cup prediction repositories that publish model assumptions and forecasts.

## Quick start

```bash
python -m pred.cli demo
```

## Design principles

1. Preserve every input source and timestamp so verdicts can be audited.
2. Keep models explainable before adding complexity.
3. Backtest before displaying betting-edge output.
4. Treat odds outputs as mathematical probabilities, not guarantees or financial advice.
