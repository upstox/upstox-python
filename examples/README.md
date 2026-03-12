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

## Documentation

- [Upstox API Documentation](https://upstox.com/developer/api-documentation)
- [Upstox Python SDK (PyPI)](https://pypi.org/project/upstox-python-sdk/)
