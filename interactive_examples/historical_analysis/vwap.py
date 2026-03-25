"""
VWAP (Volume Weighted Average Price) from Intraday Candles.

Fetches today's 1-minute candles and computes cumulative VWAP:

  Typical Price = (High + Low + Close) / 3
  VWAP = Sum(Typical Price × Volume) / Sum(Volume)

Price above VWAP → bullish intraday bias (buyers in control)
Price below VWAP → bearish intraday bias (sellers in control)

Usage:
  python historical_analysis/vwap.py --token <TOKEN>
  python historical_analysis/vwap.py --token <TOKEN> --query RELIANCE
  python historical_analysis/vwap.py --token <TOKEN> --query INFY --instrument_key NSE_EQ|INE009A01021
"""

import argparse
import sys
import os
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import get_api_client, search_instrument, get_historical_candles, get_ltp

BOLD  = "\033[1m"
GREEN = "\033[32m"
RED   = "\033[31m"
CYAN  = "\033[36m"
RESET = "\033[0m"


def main():
    parser = argparse.ArgumentParser(description="VWAP from intraday 1-min candles")
    parser.add_argument("--token", required=True, help="Upstox access or analytics token")
    parser.add_argument("--query", default="RELIANCE", help="Stock name (default: RELIANCE)")
    parser.add_argument("--instrument_key", default="",
                        help="Direct instrument key (skips search)")
    args = parser.parse_args()

    client = get_api_client(args.token)

    # Resolve instrument key
    if args.instrument_key:
        instrument_key = args.instrument_key
        trading_symbol = args.query.upper()
    else:
        resp = search_instrument(client, args.query, exchanges="NSE", segments="EQ", records=3)
        hits = resp.data or []
        if not hits:
            print(f"Instrument '{args.query}' not found on NSE.")
            sys.exit(1)
        instrument_key = hits[0]["instrument_key"]
        trading_symbol = hits[0].get("trading_symbol", args.query.upper())

    print(f"\nComputing VWAP for {trading_symbol}...\n")

    # Fetch today's 1-min candles
    to_date = date.today().isoformat()
    candles = get_historical_candles(client, instrument_key, "minutes", 1, to_date)

    if not candles:
        print("No intraday candle data returned. Market may be closed.")
        sys.exit(1)

    # Candles are [timestamp, open, high, low, close, volume, oi]
    # Reverse to chronological order
    candles = list(reversed(candles))

    cum_tp_vol = 0.0
    cum_vol = 0
    vwap_points = []

    for c in candles:
        if len(c) < 6:
            continue
        high = float(c[2])
        low = float(c[3])
        close = float(c[4])
        volume = int(c[5])

        typical_price = (high + low + close) / 3
        cum_tp_vol += typical_price * volume
        cum_vol += volume
        vwap = cum_tp_vol / cum_vol if cum_vol else 0
        vwap_points.append((c[0], close, vwap, volume))

    if not vwap_points:
        print("No valid candle data to compute VWAP.")
        sys.exit(1)

    current_vwap = vwap_points[-1][2]
    current_price = vwap_points[-1][1]
    total_volume = cum_vol

    # Also fetch live LTP for most current price
    ltp_data = get_ltp(client, instrument_key)
    ltp_entry = ltp_data.get(instrument_key, {})
    live_price = ltp_entry.get("last_price") if isinstance(ltp_entry, dict) else getattr(ltp_entry, "last_price", 0)
    if live_price:
        current_price = live_price

    deviation = (current_price - current_vwap) / current_vwap * 100 if current_vwap else 0

    # Display summary
    print(f"  Instrument    : {trading_symbol}")
    print(f"  Candles       : {len(vwap_points)} x 1-min")
    print(f"  Total volume  : {total_volume:,}")
    print()
    print(f"  {BOLD}VWAP           : {current_vwap:,.2f}{RESET}")
    print(f"  Current price  : {current_price:,.2f}")
    print(f"  Deviation      : {deviation:+.2f}%")
    print()

    if current_price > current_vwap:
        print(f"  {GREEN}Price is ABOVE VWAP{RESET} — bullish intraday bias (buyers in control).")
    elif current_price < current_vwap:
        print(f"  {RED}Price is BELOW VWAP{RESET} — bearish intraday bias (sellers in control).")
    else:
        print(f"  {CYAN}Price is AT VWAP{RESET} — neutral, at fair value.")

    # Show last 10 1-min VWAP snapshots
    print(f"\n  Last 10 VWAP snapshots (1-min):")
    print(f"  {'Time':>20}  {'Close':>10}  {'VWAP':>10}  {'Volume':>10}")
    print("  " + "-" * 55)
    for ts, close, vwap, vol in vwap_points[-10:]:
        ts_str = str(ts)[:19] if ts else "--"
        above = GREEN if close > vwap else RED
        print(f"  {ts_str:>20}  {above}{close:>10,.2f}{RESET}  {vwap:>10,.2f}  {vol:>10,}")

    print()


if __name__ == "__main__":
    main()
