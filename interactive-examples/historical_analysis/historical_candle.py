"""
Historical Candle Data using the Analytics Token.

Demonstrates the analytics token use case:
  - No OAuth flow needed
  - 1-year token validity
  - Read-only access to historical market data

Fetches OHLC + Volume + OI candles for any instrument.

Usage:
  python historical_analysis/historical_candle.py --token <ANALYTICS_TOKEN> --query RELIANCE
  python historical_analysis/historical_candle.py --token <TOKEN> --query NIFTY --unit days --interval 1 --bars 30
"""

import argparse
import sys
import os
from datetime import date, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import get_api_client, search_instrument, get_historical_candles


def main():
    parser = argparse.ArgumentParser(
        description="Fetch historical OHLC candles — ideal for use with analytics token"
    )
    parser.add_argument("--token", required=True,
                        help="Analytics token or access token (analytics token recommended for this use case)")
    parser.add_argument("--query", default="RELIANCE", help="Instrument name (default: RELIANCE)")
    parser.add_argument("--exchange", default="NSE", help="Exchange (default: NSE)")
    parser.add_argument("--unit", default="days", help="Time unit: minutes, hours, days, weeks, months (default: days)")
    parser.add_argument("--interval", type=int, default=1, help="Interval count (default: 1)")
    parser.add_argument("--bars", type=int, default=20, help="Number of candles to display (default: 20)")
    args = parser.parse_args()

    client = get_api_client(args.token)

    print(f"Fetching {args.interval}{args.unit} candles for '{args.query}' on {args.exchange}...\n")
    print("(Using analytics token — no OAuth flow required for historical data)")
    print()

    # Find the equity instrument
    resp = search_instrument(client, args.query, exchanges=args.exchange, segments="EQ", records=3)
    instruments = resp.data or []
    if not instruments:
        print(f"Instrument '{args.query}' not found.")
        sys.exit(1)

    inst = instruments[0]
    instrument_key = inst["instrument_key"]
    trading_symbol = inst.get("trading_symbol", args.query)

    print(f"Instrument : {trading_symbol}  ({instrument_key})")
    print()

    to_date = date.today().isoformat()

    candles = get_historical_candles(client, instrument_key, args.unit, args.interval, to_date)

    if not candles:
        print("No candle data returned.")
        sys.exit(1)

    # candles are newest-first; take the last N
    display = candles[:args.bars]

    print(f"{'Date/Time':<22} {'Open':>10} {'High':>10} {'Low':>10} {'Close':>10} {'Volume':>12} {'OI':>10}")
    print("-" * 90)

    for candle in reversed(display):
        # candle = [timestamp, open, high, low, close, volume, oi]
        ts    = str(candle[0])[:19] if len(candle) > 0 else ""
        open_ = float(candle[1]) if len(candle) > 1 else 0
        high  = float(candle[2]) if len(candle) > 2 else 0
        low   = float(candle[3]) if len(candle) > 3 else 0
        close = float(candle[4]) if len(candle) > 4 else 0
        vol   = int(candle[5])   if len(candle) > 5 else 0
        oi    = int(candle[6])   if len(candle) > 6 else 0

        print(f"{ts:<22} {open_:>10.2f} {high:>10.2f} {low:>10.2f} {close:>10.2f} {vol:>12,} {oi:>10,}")


if __name__ == "__main__":
    main()
