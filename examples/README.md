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
| [**user/**](user/) | User profile, fund and margin details. |
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
| [**trade-profit-and-loss/**](trade-profit-and-loss/) | P&amp;L report, report metadata, trade charges. |
| [**strategies/**](strategies/) | Ready-to-run options strategy examples for Nifty 50 (bullish, bearish, neutral). |

### Options Strategies

Each strategy script searches for the required Nifty 50 option legs using the Instruments API and places market orders via the v3 Order API.

#### [Bullish](strategies/bullish/)

| File | Strategy | Legs |
|------|----------|------|
| [buy_call.py](strategies/bullish/buy_call.py) | **Buy Call** | BUY ATM CE |
| [sell_put.py](strategies/bullish/sell_put.py) | **Sell Put** | SELL ATM PE |
| [bull_call_spread.py](strategies/bullish/bull_call_spread.py) | **Bull Call Spread** | BUY ATM CE + SELL ATM+1 CE |
| [bull_put_spread.py](strategies/bullish/bull_put_spread.py) | **Bull Put Spread** | SELL ATM PE + BUY ATM-1 PE |

#### [Bearish](strategies/bearish/)

| File | Strategy | Legs |
|------|----------|------|
| [buy_put.py](strategies/bearish/buy_put.py) | **Buy Put** | BUY ATM PE |
| [sell_call.py](strategies/bearish/sell_call.py) | **Sell Call** | SELL ATM CE |
| [bear_call_spread.py](strategies/bearish/bear_call_spread.py) | **Bear Call Spread** | SELL ATM CE + BUY ATM+1 CE |
| [bear_put_spread.py](strategies/bearish/bear_put_spread.py) | **Bear Put Spread** | BUY ATM PE + SELL ATM-1 PE |

#### [Neutral](strategies/neutral/)

| File | Strategy | Legs |
|------|----------|------|
| [short_straddle.py](strategies/neutral/short_straddle.py) | **Short Straddle** | SELL ATM CE + SELL ATM PE |
| [short_strangle.py](strategies/neutral/short_strangle.py) | **Short Strangle** | SELL ATM+1 CE + SELL ATM-1 PE |
| [iron_butterfly.py](strategies/neutral/iron_butterfly.py) | **Iron Butterfly** | SELL ATM CE + SELL ATM PE + BUY ATM+2 CE + BUY ATM-2 PE |
| [batman.py](strategies/neutral/batman.py) | **Batman** | BUY ATM CE + SELL 2× ATM+1 CE + BUY ATM+2 CE + BUY ATM PE + SELL 2× ATM-1 PE + BUY ATM-2 PE |

## Documentation

- [Upstox API Documentation](https://upstox.com/developer/api-documentation)
- [Upstox Python SDK (PyPI)](https://pypi.org/project/upstox-python-sdk/)
