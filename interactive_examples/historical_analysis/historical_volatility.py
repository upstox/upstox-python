"""
Historical Volatility Calculator.

Computes 30-day (and configurable) realised/historical volatility from
daily close prices fetched via the analytics token.

Historical Volatility (HV) = annualised standard deviation of log returns.

  log_return_i = ln(Close_i / Close_{i-1})
  HV_daily = std(log_returns) over N days
  HV_annual = HV_daily * sqrt(252)

Compare HV to the options-implied ATM straddle cost for a quick
IV vs HV comparison (a premium implies options are expensive).

Usage:
  python historical_analysis/historical_volatility.py --token <ANALYTICS_TOKEN>
  python historical_analysis/historical_volatility.py --token <TOKEN> --query INFY --window 20
"""

import argparse
import sys
import os
import math
from statistics import stdev, mean

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import get_api_client, search_instrument, get_historical_candles


def log_returns(closes):
    return [math.log(closes[i] / closes[i - 1]) for i in range(1, len(closes))]


def hv(returns, window):
    if len(returns) < window:
        return None
    r = returns[-window:]
    return stdev(r) * math.sqrt(252) * 100  # in percent


def main():
    parser = argparse.ArgumentParser(
        description="Realised historical volatility from daily candles"
    )
    parser.add_argument("--token", required=True,
                        help="Analytics token or access token")
    parser.add_argument("--query", default="NIFTY 50", help="Instrument name (default: NIFTY 50)")
    parser.add_argument("--exchange", default="NSE", help="Exchange (default: NSE)")
    parser.add_argument("--segment", default="INDEX", help="Segment: EQ or INDEX (default: INDEX)")
    parser.add_argument("--window", type=int, default=30, help="Volatility window in days (default: 30)")
    args = parser.parse_args()

    client = get_api_client(args.token)

    print(f"Computing {args.window}-day historical volatility for '{args.query}'...\n")

    resp = search_instrument(
        client, args.query,
        exchanges=args.exchange,
        segments=args.segment,
        records=3,
    )
    instruments = resp.data or []
    if not instruments:
        # Fallback to EQ
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

    candles = get_historical_candles(client, instrument_key, "days", 1, to_date)
    if not candles:
        print("No candle data returned.")
        sys.exit(1)

    candles = list(reversed(candles))
    closes = [float(c[4]) for c in candles if len(c) > 4]

    if len(closes) < args.window + 1:
        print(f"Need {args.window + 1} sessions, got {len(closes)}.")
        sys.exit(1)

    returns = log_returns(closes)

    hv_window  = hv(returns, args.window)
    hv_20      = hv(returns, 20)
    hv_10      = hv(returns, 10)
    hv_5       = hv(returns, 5)

    print(f"Instrument   : {trading_symbol}")
    print(f"Data points  : {len(closes)} daily closes")
    print(f"Current close: {closes[-1]:,.2f}")
    print()
    print(f"Historical Volatility (annualised):")
    print(f"  5-day   HV  : {hv_5:.2f}%"   if hv_5   else "  5-day  HV  : --")
    print(f"  10-day  HV  : {hv_10:.2f}%"  if hv_10  else "  10-day HV  : --")
    print(f"  20-day  HV  : {hv_20:.2f}%"  if hv_20  else "  20-day HV  : --")
    print(f"  {args.window}-day  HV  : {hv_window:.2f}%" if hv_window else f"  {args.window}-day HV  : --")

    # Rolling 30-day HV over last 6 months
    print(f"\nRolling {args.window}-day HV over last 6 periods:")
    print(f"  {'End Date':<12} {'Close':>10} {'HV(%)':>10}")
    print("  " + "-" * 35)
    step = max(len(returns) // 6, args.window)
    checkpoints = range(args.window, len(returns) + 1, max((len(returns) - args.window) // 6, 1))
    for idx in list(checkpoints)[-6:]:
        seg = returns[:idx]
        hv_val = hv(seg, args.window)
        ts = str(candles[idx][0])[:10] if idx < len(candles) else "--"
        close_val = closes[idx] if idx < len(closes) else 0
        if hv_val:
            print(f"  {ts:<12} {close_val:>10.2f} {hv_val:>10.2f}%")


if __name__ == "__main__":
    main()
