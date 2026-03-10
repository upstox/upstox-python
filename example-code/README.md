# Upstox Developer API – Example Code

This folder contains **ready-to-use Python samples** for the [Upstox API v2](https://upstox.com/developer/api-documentation). Each example shows how to call the API using the official [Upstox Python SDK](https://pypi.org/project/upstox-python-sdk/) (`upstox_client`).

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
| **login/** | Authentication: get token from auth code, access-token request, logout. |
| **user/** | User profile, fund and margin details. |
| **orders/code/** | Order lifecycle: place (single/multi, v2 & v3), modify, cancel, order book, order details, order history, trades, historical trades, exit all positions. |
| **portfolio/** | Positions, holdings, MTF positions, convert positions. |
| **market-quote/** | LTP, full market quotes, OHLC (v2 & v3), option Greeks. |
| **historical-data/** | Historical and intraday candle data (v2 & v3). |
| **option-chain/** | Option contracts, put-call option chain. |
| **expired-instruments/** | Expiries, expired future/option contracts, expired historical candle data. |
| **market-information/** | Exchange status, market timings, market holidays. |
| **gtt-orders/** | Place, modify, cancel, and get details for GTT (Good Till Triggered) orders. |
| **margins/** | Margin details. |
| **charges/** | Brokerage details. |
| **trade-profit-and-loss/** | P&amp;L report, report metadata, trade charges. |

### Orders subfolder

The **orders/** folder has a dedicated [README](orders/README.md) with an index of all order examples (place, modify, cancel, order book, trades, etc.) and direct links to each snippet.

## How to use

1. Install the SDK: `pip install upstox-python-sdk`
2. Get credentials and an access token (see **login/** examples).
3. Open the `.md` file for the API you need (e.g. `orders/code/place-order.md`).
4. Copy the relevant Python block, replace `{your_access_token}` and any other placeholders, and run.

For production, keep credentials and tokens in environment variables or a secrets manager; do not hardcode them.

## Documentation

- [Upstox API Documentation](https://upstox.com/developer/api-documentation)
- [Upstox Python SDK (PyPI)](https://pypi.org/project/upstox-python-sdk/)
