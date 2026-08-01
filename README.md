# Blackjack Card-Counting Simulator

A single-file Python simulation of 6-deck blackjack that plays every hand using
basic strategy, Illustrious 18 count-based deviations, and a Hi-Lo bet spread,
then plots bankroll (PnL) over the course of the session.

## What it does

- Deals out a 6-deck shoe (312 cards) and reshuffles once fewer than 36 cards remain.
- Plays every hand according to:
  - **Basic strategy** (hard totals, soft totals, pair splitting) for a dealer
    that stands on all 17s (S17), with double-after-split allowed.
  - **Illustrious 18** deviations, applied when the Hi-Lo true count crosses the
    listed threshold (e.g. stand on 16 vs. 10 at TC ≥ 0, take insurance at TC ≥ 3).
- Tracks the running count with Hi-Lo values (2-6 = +1, 7-9 = 0, 10/A = -1) and
  converts it to a true count (`running count / decks remaining`).
- Sizes each bet as a percentage of current capital, scaled up as the true count
  rises (a standard bet spread), and down when the count is negative.
- Splits pairs up to 4 hands (per the same pair-splitting table), including a
  dedicated path for split aces (one card each, no further action, per casino rules).
- Handles insurance, blackjack payouts (3:2), doubling, and busts.
- Simulates 3000 rounds, stops early if the bankroll drops to $10 or below, and
  plots capital-over-rounds at the end with `matplotlib`.

## Running it

```bash
python blackjack.py
```

Requires `matplotlib` (`pip install matplotlib`). A plot window opens once the
simulation finishes; close it to end the script.

## File layout

Everything lives in `blackjack.py`:

| Function | Purpose |
|---|---|
| `split` | Splits a pair into up to 4 hands, drawing replacement cards. |
| `handval` | Computes a hand's point total and whether it's hard or soft. |
| `one` | Draws a single card into a hand and updates the running count. |
| `specstrat` | Illustrious 18 deviation table (count-dependent overrides). |
| `basicstrat` | Basic strategy decision loop (hit/stand/double) for a hand. |
| `wl` | Settles a finished hand against the dealer's final total. |
| `hoturn` | Plays out the dealer's hand (hits to 17+). |
| `hocal` | Computes the dealer's hand value. |
| `bj` | Main simulation loop: deals, bets, resolves each round, and plots results. |

## Simplifications / known limitations

- No surrender.
- Bet sizing for a round uses the true count from the *end of the previous
  round*, not the current one (you bet before seeing your own cards, as in
  real play) — except immediately after a reshuffle, where the count resets.
- Deck penetration is fixed at reshuffling with 36 cards left (~88% penetration).
