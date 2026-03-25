"""
52-Week High/Low Proximity Check.

Fetches ~252 daily candles via the analytics token and computes:
  - 52-week high and low
  - Current price position within the range
  - Distance from high and low (absolute and %)
  - Signal: near 52-week high (breakout candidate) or near 52-week low (reversal candidate)

Usage:
  python historical_analysis/week_52_high_low.py --token <ANALYTICS_TOKEN>
  python historical_analysis/week_52_high_low.py --token <TOKEN> --query HDFCBANK
  python historical_analysis/week_52_high_low.py --token <TOKEN> --query NIFTY --segment INDEX
"""

import argparse
import sys
import os
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import get_api_client, search_instrument, get_historical_candles


def main():
    parser = argparse.ArgumentParser(description="52-week high/low proximity check")
    parser.add_argument("--token", required=True,
                        help="Analytics token or access token")
    parser.add_argument("--query", default="RELIANCE", help="Instrument name (default: RELIANCE)")
    parser.add_argument("--exchange", default="NSE", help="Exchange (default: NSE)")
    parser.add_argument("--segment", default="EQ", help="Segment: EQ or INDEX (default: EQ)")
    parser.add_argument("--threshold", type=float, default=5.0,
                        help="%% proximity threshold for high/low alerts (default: 5)")
    args = parser.parse_args()

    client = get_api_client(args.token)

    print(f"Fetching 52-week data for '{args.query}' on {args.exchange}...\n")

    resp = search_instrument(client, args.query, exchanges=args.exchange,
                             segments=args.segment, records=3)
    instruments = resp.data or []
    if not instruments:
        print(f"'{args.query}' not found.")
        sys.exit(1)

    inst = instruments[0]
    instrument_key = inst["instrument_key"]
    trading_symbol = inst.get("trading_symbol", args.query)

    to_date = date.today().isoformat()
    candles = get_historical_candles(client, instrument_key, "days", 1, to_date)

    if not candles:
        print("No candle data returned.")
        sys.exit(1)

    candles = list(reversed(candles))

    # Use up to last 252 trading days (~1 year)
    year_candles = candles[-252:]

    highs  = [float(c[2]) for c in year_candles if len(c) > 2]
    lows   = [float(c[3]) for c in year_candles if len(c) > 3]
    closes = [float(c[4]) for c in year_candles if len(c) > 4]

    if not closes:
        print("No data.")
        sys.exit(1)

    week52_high = max(highs)
    week52_low  = min(lows)
    current     = closes[-1]
    prev_close  = closes[-2] if len(closes) > 1 else current

    range_width   = week52_high - week52_low
    position_pct  = ((current - week52_low) / range_width * 100) if range_width else 50
    dist_from_high = ((week52_high - current) / week52_high) * 100
    dist_from_low  = ((current - week52_low)  / week52_low)  * 100
    daily_change   = ((current - prev_close) / prev_close) * 100

    # Build position bar
    bar_len = 40
    pos = int(position_pct / 100 * bar_len)
    bar = "[" + "-" * pos + "●" + "-" * (bar_len - pos) + "]"

    print(f"Instrument       : {trading_symbol}")
    print(f"Current price    : {current:,.2f}  ({daily_change:+.2f}% today)")
    print()
    print(f"52-week high     : {week52_high:,.2f}  ({dist_from_high:.1f}% below current high)")
    print(f"52-week low      : {week52_low:,.2f}  ({dist_from_low:.1f}% above current low)")
    print(f"52-week range    : {range_width:,.2f} points")
    print()
    print(f"Position in range: {position_pct:.1f}%")
    print(f"  Low {bar} High")
    print()

    if dist_from_high <= args.threshold:
        print(f"NEAR 52-WEEK HIGH — within {dist_from_high:.1f}% of {week52_high:,.2f}.")
        print("Watch for breakout or distribution. Volume confirmation key.")
    elif dist_from_low <= args.threshold:
        print(f"NEAR 52-WEEK LOW  — within {dist_from_low:.1f}% of {week52_low:,.2f}.")
        print("Watch for reversal or breakdown. Check fundamentals before buying.")
    else:
        print(f"Price is mid-range. {position_pct:.0f}% of the 52-week range.")

    print(f"\nData period      : {str(year_candles[0][0])[:10]} to {str(year_candles[-1][0])[:10]}")
    print(f"Sessions used    : {len(year_candles)}")


if __name__ == "__main__":
    main()
