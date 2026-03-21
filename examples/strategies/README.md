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

---

### [Bearish](bearish/)

Strategies that profit when the market moves **down**. Use these when you expect Nifty 50 to fall.

| Strategy | Description |
|----------|-------------|
| [Buy Put](bearish/) | Simplest bearish bet — buy an ATM put, profit increases as market falls. |
| [Sell Call](bearish/) | Collect premium by selling an ATM call — profitable if market stays flat or falls. |
| [Bear Call Spread](bearish/) | Sell ATM call, buy higher OTM call to cap risk — profit from premium if market stays below short strike. |
| [Bear Put Spread](bearish/) | Buy ATM put, sell lower OTM put to reduce cost — capped profit, capped loss. |

---

### [Neutral](neutral/)

Strategies that profit when the market moves **sideways** or stays range-bound. Use these when you expect low volatility.

| Strategy | Description |
|----------|-------------|
| [Short Straddle](neutral/) | Sell ATM call and ATM put at the same strike — maximum premium collected, profits if market barely moves. |
| [Short Strangle](neutral/) | Sell OTM call and OTM put — wider breakeven range than straddle, lower premium collected. |
| [Iron Butterfly](neutral/) | Sell ATM call and put, buy OTM call and put as wings — limited risk version of short straddle. |
| [Batman](neutral/) | Double butterfly (call + put side) — profits in a narrow range, defined risk on both sides. |
