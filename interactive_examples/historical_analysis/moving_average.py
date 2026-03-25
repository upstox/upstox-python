"""
Moving Average Crossover using Historical Candles.

Fetches daily candles via the analytics token and computes:
  - Simple Moving Average (SMA) for configurable fast and slow periods
  - Current signal: BULLISH (fast > slow) or BEARISH (fast < slow)
  - Recent crossover detection

This is a classic trend-following signal widely used in algorithmic trading.

Usage:
  python historical_analysis/moving_average.py --token <ANALYTICS_TOKEN>
  python historical_analysis/moving_average.py --token <TOKEN> --query INFY --fast 20 --slow 50
"""

import argparse
import sys
import os
from statistics import mean

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import get_api_client, search_instrument, get_historical_candles


def sma(prices, period):
    if len(prices) < period:
        return None
    return mean(prices[-period:])


def main():
    parser = argparse.ArgumentParser(description="SMA crossover signal using historical data")
    parser.add_argument("--token", required=True,
                        help="Analytics token or access token")
    parser.add_argument("--query", default="RELIANCE", help="Stock name (default: RELIANCE)")
    parser.add_argument("--exchange", default="NSE", help="Exchange (default: NSE)")
    parser.add_argument("--fast", type=int, default=20, help="Fast SMA period (default: 20)")
    parser.add_argument("--slow", type=int, default=50, help="Slow SMA period (default: 50)")
    args = parser.parse_args()

    client = get_api_client(args.token)

    print(f"Computing SMA({args.fast}) / SMA({args.slow}) for '{args.query}' on {args.exchange}...\n")

    resp = search_instrument(client, args.query, exchanges=args.exchange, segments="EQ", records=3)
    instruments = resp.data or []
    if not instruments:
        print(f"Instrument '{args.query}' not found.")
        sys.exit(1)

    inst = instruments[0]
    instrument_key = inst["instrument_key"]
    trading_symbol = inst.get("trading_symbol", args.query)

    from datetime import date
    to_date = date.today().isoformat()

    # Fetch enough candles for the slow period + some history
    candles = get_historical_candles(client, instrument_key, "days", 1, to_date)

    if not candles:
        print("No candle data returned.")
        sys.exit(1)

    # candles newest-first → reverse
    candles = list(reversed(candles))
    closes = [float(c[4]) for c in candles if len(c) > 4]

    if len(closes) < args.slow:
        print(f"Not enough data: need {args.slow} candles, got {len(closes)}.")
        sys.exit(1)

    fast_sma = sma(closes, args.fast)
    slow_sma = sma(closes, args.slow)

    # Check for crossover in last 5 sessions
    crossover = None
    for i in range(len(closes) - 5, len(closes)):
        if i < args.slow:
            continue
        prev_fast = mean(closes[i - args.fast: i])
        prev_slow = mean(closes[i - args.slow: i])
        curr_fast = mean(closes[i - args.fast + 1: i + 1])
        curr_slow = mean(closes[i - args.slow + 1: i + 1])
        if prev_fast < prev_slow and curr_fast > curr_slow:
            crossover = ("BULLISH CROSSOVER", candles[i][0])
        elif prev_fast > prev_slow and curr_fast < curr_slow:
            crossover = ("BEARISH CROSSOVER", candles[i][0])

    print(f"Instrument        : {trading_symbol}")
    print(f"Current price     : {closes[-1]:,.2f}")
    print(f"SMA({args.fast:>3})           : {fast_sma:,.2f}")
    print(f"SMA({args.slow:>3})           : {slow_sma:,.2f}")
    print()

    if fast_sma > slow_sma:
        signal = "BULLISH"
        detail = f"SMA({args.fast}) is above SMA({args.slow}) — uptrend in place."
    else:
        signal = "BEARISH"
        detail = f"SMA({args.fast}) is below SMA({args.slow}) — downtrend in place."

    print(f"Signal            : {signal}")
    print(f"                    {detail}")

    if crossover:
        print(f"\nRecent crossover  : {crossover[0]} detected around {str(crossover[1])[:10]}")

    # Print last 10 closes with rolling SMAs
    print(f"\nLast 10 sessions:")
    print(f"  {'Date':<12} {'Close':>10} {'SMA({})'.format(args.fast):>10} {'SMA({})'.format(args.slow):>10}")
    print("  " + "-" * 45)
    for i in range(max(0, len(closes) - 10), len(closes)):
        ts = str(candles[i][0])[:10]
        close_val = closes[i]
        f_sma = mean(closes[i - args.fast + 1: i + 1]) if i >= args.fast - 1 else None
        s_sma = mean(closes[i - args.slow + 1: i + 1]) if i >= args.slow - 1 else None
        f_str = f"{f_sma:>10.2f}" if f_sma else f"{'--':>10}"
        s_str = f"{s_sma:>10.2f}" if s_sma else f"{'--':>10}"
        print(f"  {ts:<12} {close_val:>10.2f} {f_str} {s_str}")


if __name__ == "__main__":
    main()
