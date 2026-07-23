# Upstox Python Interactive Examples

> **73 working examples** showcasing Upstox API features — **Instrument Search**, **Analytics Token**, **Market Data**, **Fundamentals**, **Expired Instruments**, **Charges & Margin**, and read-only **Account** data — across futures spreads, options strategies, arbitrage, historical analysis, live market data, fundamentals analysis, and more.
>
> Every example is **read-only**: it runs with any valid analytics or access token, needs no funded account, and never places an order. Trading/portfolio APIs are intentionally out of scope (see [What's not covered](#whats-not-covered)).

[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![upstox-python-sdk](https://img.shields.io/pypi/v/upstox-python-sdk?label=upstox-python-sdk)](https://pypi.org/project/upstox-python-sdk/)

---

## Quick Start

```bash
cd interactive_examples
pip install -r requirements.txt
python instrument_search/search_equity.py --token <TOKEN> --query RELIANCE
```

---


## 🚀 Try it Online

A Streamlit web app wraps every example with a UI — paste your token and run:

> **[▶ Open Live App](https://upstox-interactive-python.streamlit.app/)**

Or run locally:

```bash
git clone https://github.com/upstox/python-examples
cd python-examples
pip install -r requirements.txt
streamlit run streamlit_app.py
```

---




## Getting a Token

| Token | How to get | Valid for | Can trade? |
|---|---|---|---|
| **Analytics token** | [Developer Apps](https://account.upstox.com/developer/apps) → Analytics tab | **1 year** | No (read-only) |
| **Access token** | Standard OAuth flow | 1 day | Yes |

Use the **analytics token** for all examples below — no daily login needed.

---

## Test Runner

Run all examples automatically against a real token:

```bash
python test_runner.py --token <TOKEN>
```

- Validates the token before starting (falls back to an interactive prompt if `--token` is omitted)
- Runs every script non-interactively and reports PASS / FAIL with the reason
- A PASS requires exit 0 **and** non-empty output **and** no Python traceback
- Streaming scripts (WebSocket depth) are auto-aborted after 5 seconds and counted as PASS
- A separate **edge-case suite** feeds deliberately-bad inputs (unknown ticker, malformed date) and asserts each example fails *gracefully* — a clean error message, no traceback

---

## Examples

### Instrument Search
*Demonstrates the `GET /v2/instruments/search` endpoint — find instruments dynamically by name, exchange, segment, option type, expiry, and ATM offset.*

| Script | What it does |
|---|---|
| `instrument_search/search_equity.py` | Search equity stocks — instrument key, ISIN, lot size |
| `instrument_search/search_futures.py` | List all futures for a symbol sorted by expiry |
| `instrument_search/search_options.py` | Search options with expiry + ATM offset filters |

```bash
python instrument_search/search_equity.py --token <TOKEN> --query RELIANCE
python instrument_search/search_futures.py --token <TOKEN> --query BANKNIFTY
python instrument_search/search_options.py --token <TOKEN> --query NIFTY --expiry current_month
```

---

### Futures & Basis

| Script | What it does |
|---|---|
| `futures_basis/nifty_futures_spread.py` | Near vs far NIFTY futures — calendar spread + contango/backwardation signal |
| `futures_basis/banknifty_futures_spread.py` | Same for BankNifty (weekly expiries) |
| `futures_basis/cash_futures_basis.py` | Index spot vs futures — basis and implied annualised carry |
| `futures_basis/futures_roll_cost.py` | Cost to roll long/short from near to far month |
| `futures_basis/mcx_crude_spread.py` | MCX crude oil near/far spread |

```bash
python futures_basis/nifty_futures_spread.py --token <TOKEN>
python futures_basis/cash_futures_basis.py --token <TOKEN> --query "NIFTY 50"
python futures_basis/futures_roll_cost.py --token <TOKEN> --side long
```

---

### Options Strategies

| Script | What it does |
|---|---|
| `options_strategies/straddle_pricer.py` | ATM straddle — total premium, breakevens |
| `options_strategies/strangle_pricer.py` | OTM strangle — cost, breakevens |
| `options_strategies/bull_call_spread.py` | Bull call spread — net debit, max profit, breakeven |
| `options_strategies/iron_condor_setup.py` | Iron condor — 4 legs, net credit, profit zone |
| `options_strategies/butterfly_spread.py` | Butterfly spread — max profit at ATM at expiry |
| `options_strategies/calendar_spread_options.py` | Calendar spread — sell near, buy far, same strike |
| `options_strategies/put_call_parity.py` | Put-call parity check — C − P vs F − K deviation |

```bash
python options_strategies/straddle_pricer.py --token <TOKEN> --query NIFTY
python options_strategies/iron_condor_setup.py --token <TOKEN> --short_offset 2
python options_strategies/put_call_parity.py --token <TOKEN> --query BANKNIFTY
```

---

### Options Analytics

| Script | What it does |
|---|---|
| `options_analytics/options_chain_builder.py` | Live options chain across ±N strikes from ATM |
| `options_analytics/max_pain_calculator.py` | Max pain strike from OI — where option buyers lose most |
| `options_analytics/oi_skew.py` | CE vs PE OI by strike — support/resistance + PCR |
| `options_analytics/volatility_skew.py` | OTM PE/CE premium ratio — negative skew visualisation |
| `options_analytics/gamma_exposure.py` | Dealer gamma exposure (GEX) by strike |
| `options_analytics/option_chain_native.py` | Full option chain via dedicated `OptionsApi` — CE/PE OI, LTP, IV by strike |
| `options_analytics/option_greeks.py` | Delta, gamma, theta, vega, IV for ATM ± N strikes |
| `options_analytics/pcr_trend.py` | Put-Call Ratio from OI — per-strike breakdown + bullish/bearish signal |
| `options_analytics/iv_percentile.py` | IV Percentile & IV Rank — where current IV stands vs 1-year history |
| `options_analytics/implied_move.py` | Expected move from ATM straddle — upper/lower range as % |
| `options_analytics/expiry_decay.py` | Expiry-day premium decay — ATM ± N premiums as % of prior close |
| `options_analytics/option_contracts.py` | Enumerate live CE/PE contracts for an underlying via `OptionsApi.get_option_contracts` |

```bash
python options_analytics/options_chain_builder.py --token <TOKEN> --query NIFTY --strikes 5
python options_analytics/option_chain_native.py --token <TOKEN> --query NIFTY
python options_analytics/pcr_trend.py --token <TOKEN> --query NIFTY
python options_analytics/iv_percentile.py --token <TOKEN> --query NIFTY
python options_analytics/implied_move.py --token <TOKEN> --query NIFTY
python options_analytics/expiry_decay.py --token <TOKEN> --query NIFTY --strikes 3
```

---

### Arbitrage

| Script | What it does |
|---|---|
| `arbitrage/nse_bse_arbitrage.py` | Same stock on NSE vs BSE — price spread + arbitrage direction |
| `arbitrage/etf_vs_index.py` | ETF LTP vs index NAV — premium/discount |
| `arbitrage/currency_futures_spread.py` | USDINR near/far spread — interest rate parity |

```bash
python arbitrage/nse_bse_arbitrage.py --token <TOKEN> --query RELIANCE
python arbitrage/etf_vs_index.py --token <TOKEN>
python arbitrage/currency_futures_spread.py --token <TOKEN> --pair USDINR
```

---

### Historical Analysis
*These work best with the analytics token — fetch up to years of data without re-authenticating.*

| Script | What it does |
|---|---|
| `historical_analysis/historical_candle.py` | OHLC candles for any instrument and interval |
| `historical_analysis/moving_average.py` | SMA(20)/SMA(50) crossover signal |
| `historical_analysis/historical_volatility.py` | Annualised realised volatility from daily closes |
| `historical_analysis/week_52_high_low.py` | 52-week high/low and position-in-range |
| `historical_analysis/vwap.py` | VWAP from intraday 1-min candles — current price vs VWAP signal |
| `historical_analysis/beta_calculator.py` | Stock beta vs NIFTY 50 index + correlation coefficient |
| `historical_analysis/stock_correlation.py` | Pairwise Pearson correlation of daily returns for 2+ stocks |

```bash
python historical_analysis/historical_candle.py --token <ANALYTICS_TOKEN> --query RELIANCE
python historical_analysis/moving_average.py --token <ANALYTICS_TOKEN> --fast 20 --slow 50
python historical_analysis/vwap.py --token <TOKEN> --query RELIANCE
python historical_analysis/beta_calculator.py --token <TOKEN> --query RELIANCE --days 60
python historical_analysis/stock_correlation.py --token <TOKEN> --queries RELIANCE,TCS,INFY
```

---

### Portfolio & Screening

| Script | What it does |
|---|---|
| `portfolio_screening/sector_index_comparison.py` | NSE sector indices ranked by daily % change |
| `portfolio_screening/top_volume_stocks.py` | Search results ranked by traded volume |
| `portfolio_screening/futures_oi_buildup.py` | Futures OI scanner — long/short buildup signals |

```bash
python portfolio_screening/sector_index_comparison.py --token <TOKEN>
python portfolio_screening/top_volume_stocks.py --token <TOKEN>
python portfolio_screening/futures_oi_buildup.py --token <TOKEN>
```

---

### Market Data

| Script | What it does |
|---|---|
| `market_data/market_status.py` | Live open/closed/pre-open status for NSE, BSE, MCX, NFO, BFO, CDS |
| `market_data/market_holidays.py` | Full-year holiday calendar — upcoming vs past, with MCX partial session labels |
| `market_data/market_timings.py` | Exchange session windows for any date with ACTIVE highlight |
| `market_data/intraday_chart.py` | Terminal candlestick + volume chart (plotext) for any index |
| `market_data/live_depth.py` | Live 5-level depth: NIFTY FUT + SENSEX FUT + RELIANCE NSE/BSE in a 2×2 grid |
| `market_data/live_depth_d30.py` | 30-level depth via WebSocket *(requires Upstox Plus Pack)* |
| `market_data/live_depth_mcx.py` | Live depth for top MCX commodities (GOLD, SILVER, CRUDEOIL, NATURALGAS) |
| `market_data/live_depth_usdinr.py` | USDINR near-month futures — NSE CDS vs BSE BCD side by side |
| `market_data/ohlc_quote.py` | OHLC snapshot (prev + live candle) for one or more instruments via Market Quote v3 |
| `market_data/market_news.py` | Latest news articles for an instrument (or positions/holdings) |
| `market_data/market_holiday.py` | Whether a specific date is a market holiday, and which exchanges are closed |

```bash
python market_data/market_status.py --token <TOKEN>
python market_data/market_holidays.py --token <TOKEN>
python market_data/intraday_chart.py --token <TOKEN> --query SENSEX --interval 5
python market_data/live_depth.py --token <TOKEN>        # Ctrl-C to stop
python market_data/live_depth_mcx.py --token <TOKEN>    # Ctrl-C to stop
python market_data/ohlc_quote.py --token <TOKEN> --queries RELIANCE,TCS --interval 1d
python market_data/market_news.py --token <TOKEN> --query RELIANCE
python market_data/market_holiday.py --token <TOKEN> --date 2026-01-26
```

---

### Fundamentals Analysis
*Uses the [Upstox Fundamentals API](https://upstox.com/developer/api-documentation/fundamentals). Pass `--symbol` with a stock name — the ISIN is resolved automatically.*

| Script | What it does |
|---|---|
| `fundamentals/company_profile.py` | Sector, industry, market cap, employees and business overview |
| `fundamentals/key_ratios.py` | P/E, P/B, ROE, ROCE, D/E and more vs sector average |
| `fundamentals/balance_sheet.py` | Historical total assets, liabilities and derived equity |
| `fundamentals/income_statement.py` | Revenue, operating profit, net profit and EPS over time |
| `fundamentals/cash_flow.py` | Operating, investing and financing cash flows across periods |
| `fundamentals/corporate_actions.py` | Dividends, stock splits, bonuses — sorted most-recent first |
| `fundamentals/share_holdings.py` | Quarterly promoter / FII / DII / public shareholding |
| `fundamentals/competitors.py` | Peer companies in the same sector with market cap comparison |

```bash
python fundamentals/company_profile.py --token <TOKEN> --symbol RELIANCE
python fundamentals/key_ratios.py     --token <TOKEN> --symbol TCS
python fundamentals/balance_sheet.py  --token <TOKEN> --symbol HDFCBANK
python fundamentals/income_statement.py --token <TOKEN> --symbol INFY
python fundamentals/cash_flow.py      --token <TOKEN> --symbol WIPRO
python fundamentals/corporate_actions.py --token <TOKEN> --symbol HDFCBANK
python fundamentals/share_holdings.py --token <TOKEN> --symbol RELIANCE
python fundamentals/competitors.py    --token <TOKEN> --symbol TCS
```

### Market Information
*Uses the [Upstox Market Information API](https://upstox.com/developer/api-documentation/market-information). Note: **Market Holidays**, **Market Timings**, and **Exchange Status** live under `market_data/` above.*

| Script | What it does |
|---|---|
| `market_information/fii_data.py` | FII buy / sell / OI activity by segment (cash, futures, options) and interval |
| `market_information/dii_data.py` | DII buy / sell flow for the NSE cash market |
| `market_information/oi_data.py` | Per-strike call / put open interest for an underlying + expiry |
| `market_information/change_oi.py` | Per-strike change in OI over a configurable lookback |
| `market_information/max_pain.py` | Max pain strike + intraday max-pain vs spot |
| `market_information/pcr_data.py` | Overall PCR + intraday PCR / spot data points |

```bash
python market_information/fii_data.py  --token <TOKEN> --data-type "NSE_EQ|CASH" --interval 1D
python market_information/dii_data.py  --token <TOKEN> --interval 1M
python market_information/oi_data.py   --token <TOKEN> --expiry 2026-05-29
python market_information/change_oi.py --token <TOKEN> --expiry 2026-05-29 --interval 5
python market_information/max_pain.py  --token <TOKEN> --expiry 2026-05-29 --bucket-interval 60
python market_information/pcr_data.py  --token <TOKEN> --expiry 2026-05-29 --bucket-interval 60
```

---

### Expired Instruments
*Uses the [Upstox Expired Instrument API](https://upstox.com/developer/api-documentation/). Fetch expiry lists and the contracts / OHLC history of already-expired derivatives — useful for back-testing.*

| Script | What it does |
|---|---|
| `expired_instruments/expiries.py` | List all expiry dates available for an underlying |
| `expired_instruments/expired_option_contracts.py` | CE/PE contracts that existed for a past expiry |
| `expired_instruments/expired_future_contracts.py` | Futures contracts that existed for a past expiry |
| `expired_instruments/expired_historical.py` | OHLC history for an expired contract |

```bash
python expired_instruments/expiries.py --token <TOKEN> --query NIFTY
python expired_instruments/expired_option_contracts.py --token <TOKEN> --query NIFTY --expiry 2024-12-26
python expired_instruments/expired_future_contracts.py --token <TOKEN> --query NIFTY
python expired_instruments/expired_historical.py --token <TOKEN> --query NIFTY --interval day
```

---

### Charges & Margin
*Uses the [Upstox Charge API](https://upstox.com/developer/api-documentation/). These **compute** brokerage and required margin for a prospective order — nothing is sent to the exchange, no order is placed.*

| Script | What it does |
|---|---|
| `charges/brokerage_calculator.py` | Estimate brokerage + statutory charges for a what-if order |
| `charges/margin_calculator.py` | Estimate SPAN / exposure / total margin required for an order basket |

```bash
python charges/brokerage_calculator.py --token <TOKEN> --symbol RELIANCE --quantity 10 --price 1400
python charges/margin_calculator.py --token <TOKEN> --symbol RELIANCE --quantity 10 --price 1400
```

---

### Account (Read-Only)
*Uses read-only endpoints of the [Upstox User API](https://upstox.com/developer/api-documentation/). No account settings are changed and no funds are moved.*

| Script | What it does |
|---|---|
| `account/user_profile.py` | Profile — name, email, broker, enabled exchanges/products |
| `account/funds_margin.py` | Available / unavailable funds and margin (v3) |

```bash
python account/user_profile.py --token <TOKEN>
python account/funds_margin.py --token <TOKEN>
```

---

## What's not covered

By design, these examples cover only **read-only** APIs so every one runs with any
valid token and never touches a live account. The following SDK areas are
**intentionally excluded** because they place real orders or read/modify private
account state (they require a funded, OAuth-authenticated trading account):

- **Order placement & management** — `OrderApi`, `OrderApiV3` (incl. GTT orders)
- **Portfolio** — `PortfolioApi` (holdings, positions, MTF, convert positions)
- **P&L & trades** — `TradeProfitAndLossApi`, `PostTradeApi`
- **Mutual funds** — `MutualFundApi`
- **Account actions** — `UserApi` kill-switch / pay-in / payout / IP updates, `LoginApi` OAuth flow
- **Portfolio streaming** — `PortfolioDataStreamer` (order/position/holding updates)

---


## 🌐 Deploy the Streamlit App

The `streamlit_app.py` wraps all 73 examples in a browser UI with interactive inputs and charts (including Plotly charts for fundamentals).

### Streamlit Cloud (free, ~5 minutes)

1. Fork / push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New streamlit_app**
3. Select this repo, branch `main`, file `streamlit_app.py`
4. Click **Deploy** — you get a shareable URL instantly

### Run locally

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

---

## Project Structure

```
interactive_examples/
├── utils.py                          # Shared helpers — SDK client, search, quotes, history
├── streamlit_app.py                  # Browser UI wrapping all 73 examples
├── test_runner.py                    # Automated test harness for all examples
├── requirements.txt
├── instrument_search/                # 3 scripts
├── futures_basis/                    # 5 scripts
├── options_strategies/               # 7 scripts
├── options_analytics/                # 12 scripts
├── arbitrage/                        # 3 scripts
├── historical_analysis/              # 7 scripts
├── portfolio_screening/              # 3 scripts
├── market_data/                      # 11 scripts
├── fundamentals/                     # 8 scripts
├── market_information/               # 6 scripts
├── expired_instruments/              # 4 scripts
├── charges/                          # 2 scripts
└── account/                          # 2 scripts (read-only)
```

**Total: 73 example scripts across 13 categories.**

---

## API Reference

### Analytics Token

Every script accepts `--token` on the command line. The analytics token works **identically** to a daily access token — just pass it with `--token`. The only differences:

| | Access token | Analytics token |
|---|---|---|
| Validity | 1 day | 1 year |
| OAuth flow | Required daily | Not needed |
| Trading | Yes | No (read-only) |
| Market data | Yes | Yes |
| Historical data | Yes | Yes |

---

## Requirements

CLI examples need:

```
upstox-python-sdk
plotext
```

The Streamlit app additionally needs `streamlit`, `plotly`, `pandas`, and `numpy`.
Install everything at once with `pip install -r requirements.txt`.

Python 3.9+ required.
