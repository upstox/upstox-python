# Upstox Developer API – Example Code

This folder contains **ready-to-use Python samples** for the [Upstox API](https://upstox.com/developer/api-documentation/open-api). Each example shows how to call the API using the official [Upstox Python SDK](https://pypi.org/project/upstox-python-sdk/) (`upstox_client`).

## Why use these samples?

- **Quick start** — Copy-paste examples for common flows (login, orders, market data, portfolio).
- **Correct usage** — Request/response patterns, error handling, and API version usage as recommended by Upstox.
- **Reference** — See how to structure `PlaceOrderRequest`, historical data params, and other API payloads.

Use these samples to build trading apps, dashboards, or integrations without guessing request shapes or SDK usage.

## Prerequisites

- **Python** 2.7 or 3.4+
- **SDK**: `pip install upstox-python-sdk`
- **Upstox developer account** and API credentials (client ID, client secret, redirect URI).
- **Access token** for authenticated APIs (obtain via [Login API](login/) samples).

For full setup, sandbox mode, and auth flow, see the main [Upstox Python SDK README](../README.md) in the repo root.

## Folder structure

Samples are grouped by API area. Each `.md` file contains one or more Python snippets you can run after replacing placeholders like `{your_access_token}` and `{your_client_id}`.

| Folder | Description |
|--------|-------------|
| [**login/**](login/) | Authentication: get token from auth code, access-token request, logout. |
| [**user/**](user/) | User profile, fund and margin details, IP management, kill switch. |
| [**orders/**](orders/) | Order lifecycle: place (single/multi, v2 & v3), modify, cancel, order book, order details, order history, trades, historical trades, exit all positions. |
| [**portfolio/**](portfolio/) | Positions, holdings, MTF positions, convert positions. |
| [**market-quote/**](market-quote/) | LTP, full market quotes, OHLC (v2 & v3), option Greeks. |
| [**historical-data/**](historical-data/) | Historical and intraday candle data (v2 & v3). |
| [**option-chain/**](option-chain/) | Option contracts, put-call option chain. |
| [**expired-instruments/**](expired-instruments/) | Expiries, expired future/option contracts, expired historical candle data. |
| [**market-information/**](market-information/) | Exchange status, market timings, market holidays. |
| [**gtt-orders/**](gtt-orders/) | Place, modify, cancel, and get details for GTT (Good Till Triggered) orders. |
| [**margins/**](margins/) | Margin details. |
| [**charges/**](charges/) | Brokerage details. |
| [**news/**](news/) | News articles by instrument keys, positions, or holdings. |
| [**trade-profit-and-loss/**](trade-profit-and-loss/) | P&amp;L report, report metadata, trade charges. |
| [**strategies/**](strategies/) | Ready-to-run options strategy examples for Nifty 50 (bullish, bearish, neutral, others). |

### Options Strategies

Each strategy script searches for the required Nifty 50 option legs using the Instruments API and places market orders via the v3 Order API.

#### [Bullish](strategies/bullish/)

| File | Strategy | Legs |
|------|----------|------|
| [buy_call.py](strategies/bullish/code/buy_call.py) | [**Buy Call**](strategies/bullish/README.md#buy-call--codebuy_callpy) | BUY ATM CE |
| [sell_put.py](strategies/bullish/code/sell_put.py) | [**Sell Put**](strategies/bullish/README.md#sell-put--codesell_putpy) | SELL ATM PE |
| [bull_call_spread.py](strategies/bullish/code/bull_call_spread.py) | [**Bull Call Spread**](strategies/bullish/README.md#bull-call-spread--codebull_call_spreadpy) | BUY ATM CE + SELL ATM+1 CE |
| [bull_put_spread.py](strategies/bullish/code/bull_put_spread.py) | [**Bull Put Spread**](strategies/bullish/README.md#bull-put-spread--codebull_put_spreadpy) | SELL ATM PE + BUY ATM-1 PE |
| [bull_butterfly.py](strategies/bullish/code/bull_butterfly.py) | [**Bull Butterfly**](strategies/bullish/README.md#bull-butterfly--codebull_butterflypy) | BUY ATM CE + SELL 2× ATM+1 CE + BUY ATM+2 CE |
| [bull_condor.py](strategies/bullish/code/bull_condor.py) | [**Bull Condor**](strategies/bullish/README.md#bull-condor--codebull_condorpy) | BUY ATM CE + SELL ATM+1 CE + SELL ATM+2 CE + BUY ATM+3 CE |
| [long_calendar_call.py](strategies/bullish/code/long_calendar_call.py) | [**Long Calendar with Calls**](strategies/bullish/README.md#long-calendar-with-calls--codelong_calendar_callpy) | SELL current-week ATM CE + BUY next-week ATM CE |
| [long_synthetic_future.py](strategies/bullish/code/long_synthetic_future.py) | [**Long Synthetic Future**](strategies/bullish/README.md#long-synthetic-future--codelong_synthetic_futurepy) | BUY ATM CE + SELL ATM PE |
| [call_ratio_back_spread.py](strategies/bullish/code/call_ratio_back_spread.py) | [**Call Ratio Back Spread**](strategies/bullish/README.md#call-ratio-back-spread--codecall_ratio_back_spreadpy) | SELL 1× ATM CE + BUY 2× ATM+1 CE |
| [range_forward.py](strategies/bullish/code/range_forward.py) | [**Range Forward**](strategies/bullish/README.md#range-forward--coderange_forwardpy) | SELL ATM-1 PE + BUY ATM+1 CE |

#### [Bearish](strategies/bearish/)

| File | Strategy | Legs |
|------|----------|------|
| [buy_put.py](strategies/bearish/code/buy_put.py) | [**Buy Put**](strategies/bearish/README.md#buy-put--codebuy_putpy) | BUY ATM PE |
| [sell_call.py](strategies/bearish/code/sell_call.py) | [**Sell Call**](strategies/bearish/README.md#sell-call--codesell_callpy) | SELL ATM CE |
| [bear_call_spread.py](strategies/bearish/code/bear_call_spread.py) | [**Bear Call Spread**](strategies/bearish/README.md#bear-call-spread--codebear_call_spreadpy) | SELL ATM CE + BUY ATM+1 CE |
| [bear_put_spread.py](strategies/bearish/code/bear_put_spread.py) | [**Bear Put Spread**](strategies/bearish/README.md#bear-put-spread--codebear_put_spreadpy) | BUY ATM PE + SELL ATM-1 PE |
| [bear_butterfly.py](strategies/bearish/code/bear_butterfly.py) | [**Bear Butterfly**](strategies/bearish/README.md#bear-butterfly--codebear_butterflypy) | BUY ATM PE + SELL 2× ATM-1 PE + BUY ATM-2 PE |
| [bear_condor.py](strategies/bearish/code/bear_condor.py) | [**Bear Condor**](strategies/bearish/README.md#bear-condor--codebear_condorpy) | BUY ATM PE + SELL ATM-1 PE + SELL ATM-2 PE + BUY ATM-3 PE |
| [long_calendar_put.py](strategies/bearish/code/long_calendar_put.py) | [**Long Calendar with Puts**](strategies/bearish/README.md#long-calendar-with-puts--codelong_calendar_putpy) | SELL current-week ATM PE + BUY next-week ATM PE |
| [short_synthetic_future.py](strategies/bearish/code/short_synthetic_future.py) | [**Short Synthetic Future**](strategies/bearish/README.md#short-synthetic-future--codeshort_synthetic_futurepy) | SELL ATM CE + BUY ATM PE |
| [put_ratio_back_spread.py](strategies/bearish/code/put_ratio_back_spread.py) | [**Put Ratio Back Spread**](strategies/bearish/README.md#put-ratio-back-spread--codeput_ratio_back_spreadpy) | SELL 1× ATM PE + BUY 2× ATM-1 PE |
| [risk_reversal.py](strategies/bearish/code/risk_reversal.py) | [**Risk Reversal**](strategies/bearish/README.md#risk-reversal--coderisk_reversalpy) | SELL ATM+1 CE + BUY ATM-1 PE |

#### [Neutral](strategies/neutral/)

| File | Strategy | Legs |
|------|----------|------|
| [short_straddle.py](strategies/neutral/code/short_straddle.py) | [**Short Straddle**](strategies/neutral/README.md#short-straddle--codeshort_straddlepy) | SELL ATM CE + SELL ATM PE |
| [short_strangle.py](strategies/neutral/code/short_strangle.py) | [**Short Strangle**](strategies/neutral/README.md#short-strangle--codeshort_stranglepy) | SELL ATM+1 CE + SELL ATM-1 PE |
| [iron_butterfly.py](strategies/neutral/code/iron_butterfly.py) | [**Iron Butterfly**](strategies/neutral/README.md#iron-butterfly--codeiron_butterflypy) | SELL ATM CE + SELL ATM PE + BUY ATM+2 CE + BUY ATM-2 PE |
| [batman.py](strategies/neutral/code/batman.py) | [**Batman**](strategies/neutral/README.md#batman--codebatmanpy) | BUY ATM CE + SELL 2× ATM+1 CE + BUY ATM+2 CE + BUY ATM PE + SELL 2× ATM-1 PE + BUY ATM-2 PE |
| [short_iron_condor.py](strategies/neutral/code/short_iron_condor.py) | [**Short Iron Condor**](strategies/neutral/README.md#short-iron-condor--codeshort_iron_condorpy) | SELL ATM+1 CE + BUY ATM+2 CE + SELL ATM-1 PE + BUY ATM-2 PE |

#### [Others](strategies/others/)

| File | Strategy | Legs |
|------|----------|------|
| [long_straddle.py](strategies/others/code/long_straddle.py) | [**Long Straddle**](strategies/others/README.md#long-straddle--codelong_straddlepy) | BUY ATM CE + BUY ATM PE |
| [long_strangle.py](strategies/others/code/long_strangle.py) | [**Long Strangle**](strategies/others/README.md#long-strangle--codelong_stranglepy) | BUY ATM+1 CE + BUY ATM-1 PE |
| [call_ratio_spread.py](strategies/others/code/call_ratio_spread.py) | [**Call Ratio Spread**](strategies/others/README.md#call-ratio-spread--codecall_ratio_spreadpy) | BUY 1× ATM CE + SELL 2× ATM+1 CE |
| [put_ratio_spread.py](strategies/others/code/put_ratio_spread.py) | [**Put Ratio Spread**](strategies/others/README.md#put-ratio-spread--codeput_ratio_spreadpy) | BUY 1× ATM PE + SELL 2× ATM-1 PE |
| [long_iron_butterfly.py](strategies/others/code/long_iron_butterfly.py) | [**Long Iron Butterfly**](strategies/others/README.md#long-iron-butterfly--codelong_iron_butterflypy) | BUY ATM CE + BUY ATM PE + SELL ATM+2 CE + SELL ATM-2 PE |
| [long_iron_condor.py](strategies/others/code/long_iron_condor.py) | [**Long Iron Condor**](strategies/others/README.md#long-iron-condor--codelong_iron_condorpy) | BUY ATM+1 CE + SELL ATM+2 CE + BUY ATM-1 PE + SELL ATM-2 PE |
| [strip.py](strategies/others/code/strip.py) | [**Strip**](strategies/others/README.md#strip--codestrippy) | BUY 1× ATM CE + BUY 2× ATM PE |
| [strap.py](strategies/others/code/strap.py) | [**Strap**](strategies/others/README.md#strap--codestrappy) | BUY 2× ATM CE + BUY 1× ATM PE |

## Interactive Examples

For 47 complete, runnable CLI scripts covering instrument search, futures spreads, options strategies, options analytics, arbitrage, historical analysis, and more, see the [interactive_examples/](../interactive_examples/) directory.

## Documentation

- [Upstox API Documentation](https://upstox.com/developer/api-documentation)
- [Upstox Python SDK (PyPI)](https://pypi.org/project/upstox-python-sdk/)
