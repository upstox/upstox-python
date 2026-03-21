# Options Trading Strategies

Ready-to-run Python examples for common Nifty 50 options strategies using the [Upstox Python SDK](https://pypi.org/project/upstox-python-sdk/).

Each script finds the required option legs via `InstrumentsApi.search_instrument()` and places market orders via `OrderApiV3.place_order()`. Replace `ACCESS_TOKEN` with your token before running.

> **Note:** All strategies default to **Nifty 50** but work with any index. To switch, change the `query` argument in `search_instrument()` — for example, use `"Nifty Bank"` for Bank Nifty, `"Nifty Fin Service"` for FinNifty, or `"SENSEX"` for BSE Sensex.

## Strategy Categories

### [Bullish](bullish/)

Strategies that profit when the market moves **up**. Use these when you expect Nifty 50 to rise.

| Strategy | Description |
|----------|-------------|
| [Buy Call](bullish/) | Simplest bullish bet — buy an ATM call, profit increases as market rises. |
| [Sell Put](bullish/) | Collect premium by selling an ATM put — profitable if market stays flat or rises. |
| [Bull Call Spread](bullish/) | Buy ATM call, sell OTM call to reduce cost — capped profit, capped loss. |
| [Bull Put Spread](bullish/) | Sell ATM put, buy lower OTM put — profit from premium if market stays above short strike. |
| [Bull Butterfly](bullish/) | Buy ATM call, sell 2× ATM+1 call, buy ATM+2 call — low cost, peak profit at middle strike. |
| [Bull Condor](bullish/) | Buy ATM call, sell ATM+1 and ATM+2, buy ATM+3 — wider profit zone than butterfly at slightly higher cost. |
| [Long Calendar with Calls](bullish/) | Sell current-week ATM call, buy next-week ATM call — profits from near-term time decay then upside. |
| [Long Synthetic Future](bullish/) | Buy ATM call, sell ATM put — replicates a long futures payoff using options. |
| [Call Ratio Back Spread](bullish/) | Sell ATM call, buy 2× OTM call — low-cost entry, profits accelerate on a large rally. |
| [Range Forward](bullish/) | Sell OTM put, buy OTM call — near-zero cost bullish position, unlimited risk on both sides. |

---

### [Bearish](bearish/)

Strategies that profit when the market moves **down**. Use these when you expect Nifty 50 to fall.

| Strategy | Description |
|----------|-------------|
| [Buy Put](bearish/) | Simplest bearish bet — buy an ATM put, profit increases as market falls. |
| [Sell Call](bearish/) | Collect premium by selling an ATM call — profitable if market stays flat or falls. |
| [Bear Call Spread](bearish/) | Sell ATM call, buy higher OTM call to cap risk — profit from premium if market stays below short strike. |
| [Bear Put Spread](bearish/) | Buy ATM put, sell lower OTM put to reduce cost — capped profit, capped loss. |
| [Bear Butterfly](bearish/) | Buy ATM put, sell 2× ATM-1 put, buy ATM-2 put — low cost, peak profit at middle strike. |
| [Bear Condor](bearish/) | Buy ATM put, sell ATM-1 and ATM-2, buy ATM-3 — wider profit zone than butterfly at slightly higher cost. |
| [Long Calendar with Puts](bearish/) | Sell current-week ATM put, buy next-week ATM put — profits from near-term time decay then downside. |
| [Short Synthetic Future](bearish/) | Sell ATM call, buy ATM put — replicates a short futures payoff using options. |
| [Put Ratio Back Spread](bearish/) | Sell ATM put, buy 2× OTM put — low-cost entry, profits accelerate on a large fall. |
| [Risk Reversal](bearish/) | Sell OTM call, buy OTM put — near-zero cost bearish position, unlimited risk on both sides. |

---

### [Neutral](neutral/)

Strategies that profit when the market moves **sideways** or stays range-bound. Use these when you expect low volatility.

| Strategy | Description |
|----------|-------------|
| [Short Straddle](neutral/) | Sell ATM call and ATM put at the same strike — maximum premium collected, profits if market barely moves. |
| [Short Strangle](neutral/) | Sell OTM call and OTM put — wider breakeven range than straddle, lower premium collected. |
| [Iron Butterfly](neutral/) | Sell ATM call and put, buy OTM call and put as wings — limited risk version of short straddle. |
| [Short Iron Condor](neutral/) | Sell OTM call and put, buy further OTM wings — wider range than iron butterfly, fully capped risk. |
| [Batman](neutral/) | Double butterfly (call + put side) — profits in a narrow range, defined risk on both sides. |

---

### [Others](others/)

Strategies that combine directional and volatility views, or are primarily volatility plays regardless of market direction.

| Strategy | Description |
|----------|-------------|
| [Call Ratio Spread](others/) | Buy ATM call, sell 2× OTM call — near-zero cost, profits at short strike, unlimited upside risk. |
| [Put Ratio Spread](others/) | Buy ATM put, sell 2× OTM put — near-zero cost, profits at short strike, large downside risk. |
| [Long Straddle](others/) | Buy ATM call and ATM put — profits from a big move in either direction. |
| [Long Strangle](others/) | Buy OTM call and OTM put — cheaper than straddle, needs a larger move to profit. |
| [Long Iron Butterfly](others/) | Buy ATM call and put, sell OTM wings — defined-risk volatility play, profits outside the short strikes. |
| [Long Iron Condor](others/) | Buy OTM call and put, sell further OTM wings — cheaper breakout play with fully capped risk. |
| [Strip](others/) | Buy ATM call and 2× ATM put — volatility play with bearish tilt, downside pays twice. |
| [Strap](others/) | Buy 2× ATM call and ATM put — volatility play with bullish tilt, upside pays twice. |
