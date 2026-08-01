# Blackjack Card-Counting Simulator

A single-file Python simulation of 6-deck blackjack that plays every hand using
basic strategy, Illustrious 18 count-based deviations, and a Kelly-scaled Hi-Lo
bet spread, then plots bankroll (PnL) over the course of the session.

## What it does

- Deals out a 6-deck shoe (312 cards) and reshuffles once fewer than 36 cards remain.
- Plays every hand according to:
  - **Basic strategy** (hard totals, soft totals, pair splitting) for a dealer
    that stands on all 17s (S17), with double-after-split allowed. Doubling is
    restricted to two-card hands, with the correct fallback per cell (hit for
    `D` cells, stand for `Ds` cells).
  - **Illustrious 18** deviations, applied when the Hi-Lo true count crosses the
    listed threshold (e.g. stand on 16 vs. 10 at TC ≥ 0, take insurance at TC ≥ 3).
- Tracks the running count with Hi-Lo values (2-6 = +1, 7-9 = 0, 10/A = -1) and
  converts it to a true count (`running count / decks remaining`). Every card
  that leaves the shoe is counted exactly once, including the dealer's hole card
  at the point it is revealed.
- Sizes each bet as a fraction of current capital, scaled by the true count (see
  below).
- Splits pairs up to 4 hands (per the pair-splitting table), including a
  dedicated path for split aces (one card each, no further action, per casino rules).
- Handles insurance, blackjack payouts (3:2), doubling, busts, and the dealer's
  peek for blackjack before the player acts.
- Simulates 100,000 rounds, stops early if the bankroll drops to $10 or below,
  and plots capital-over-rounds at the end with `matplotlib`.

## Bet spread

Bets are sized at roughly **half Kelly**, using `f* = edge / variance` with
blackjack's per-hand variance of ~1.32 and an edge of about 0.5% per true count
above +1:

| True count | Fraction of bankroll |
|---|---|
| < +2 | 0.10% (table minimum) |
| +2 | 0.19% |
| +3 | 0.38% |
| +4 | 0.57% |
| +5 | 0.76% |
| ≥ +6 | 0.95% |

Betting materially above full Kelly makes the long-run growth rate negative even
with a genuine edge — at 2× Kelly it is exactly zero, and beyond that ruin is
certain. Half Kelly trades a little growth for a large reduction in drawdown,
which also hedges against the edge estimate itself being optimistic.

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

Cards are represented as plain integers, with `0` standing for an Ace and `10`
covering 10/J/Q/K.

## Reading the output

The PnL curve is a random walk, not a smooth trend line. Expected profit grows
with the number of rounds, but noise grows with its square root, so the line
stays jagged no matter how long the run is — it only gradually tilts. With
blackjack's ~1.15 SD per hand and an edge of well under 1%, roughly 50,000 hands
are needed before the trend reliably dominates the noise.

A single run therefore says very little about whether a change helped. To
compare two configurations, run many seeds and compare the **median** outcome;
means are badly skewed by a handful of lucky runs.

## Simplifications / known limitations

- No surrender.
- Bet sizing uses the true count as of the end of the previous round, since bets
  are placed before any cards are dealt. The count resets on reshuffle.
- The dealer's hole card is folded into the count at the end of every round,
  including rounds where a real dealer would not expose it.
- Deck penetration is fixed at reshuffling with 36 cards left (~88% penetration),
  which is deeper than most real casinos allow.
- `risk` sizes a single hand, so a round that splits and doubles can put several
  times that fraction on the table at once; Kelly is not adjusted for this.
