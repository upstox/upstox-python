"""
OHLC Quote — open/high/low/close snapshot for one or more instruments (v3).

Uses the Upstox Market Quote v3 API. Returns both the previous candle's OHLC
and the live (in-progress) candle's OHLC at the requested interval.

Usage:
  python market_data/ohlc_quote.py --token <TOKEN>
  python market_data/ohlc_quote.py --token <TOKEN> --queries RELIANCE,TCS,INFY --interval 1d
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import get_api_client, resolve_equity, get_ohlc_quote, as_dict, die

BOLD  = "\033[1m"
GREEN = "\033[32m"
RED   = "\033[31m"
CYAN  = "\033[36m"
DIM   = "\033[2m"
RESET = "\033[0m"


def _row(label, ohlc):
    ohlc = as_dict(ohlc)
    if not ohlc:
        return None
    o, h, l, c = (ohlc.get(k) for k in ("open", "high", "low", "close"))
    if None in (o, h, l, c):
        return None
    colour = GREEN if c >= o else RED
    return (f"  {label:<12} {o:>10,.2f} {h:>10,.2f} {l:>10,.2f} "
            f"{colour}{c:>10,.2f}{RESET}")


def main():
    parser = argparse.ArgumentParser(description="OHLC quotes via Market Quote v3 API")
    parser.add_argument("--token",   required=True, help="Upstox access or analytics token")
    parser.add_argument("--queries", default="RELIANCE", help="Comma-separated symbols (default: RELIANCE)")
    parser.add_argument("--interval", default="1d", help="OHLC interval (default: 1d)")
    args = parser.parse_args()

    client = get_api_client(args.token)

    symbols = [s.strip() for s in args.queries.split(",") if s.strip()]
    resolved = {}
    for sym in symbols:
        inst = resolve_equity(client, sym)
        if inst:
            resolved[inst.get("instrument_key", "")] = sym
    if not resolved:
        die("Could not resolve any of the requested symbols.")

    print(f"\n{BOLD}Fetching OHLC quotes{RESET} (interval={args.interval}) "
          f"for {', '.join(resolved.values())}...\n")

    try:
        quotes = get_ohlc_quote(client, args.interval, *resolved.keys())
    except Exception as e:
        die(f"API error: {e}")

    if not quotes:
        die("No OHLC data returned.")

    for key, sym in resolved.items():
        q = as_dict(quotes.get(key))
        if not q:
            print(f"  {CYAN}{sym}{RESET}: no data\n")
            continue
        last = q.get("last_price")
        print(f"  {CYAN}{BOLD}{sym}{RESET}  last={last if last is not None else '—'}")
        print(f"  {DIM}{'':<12} {'Open':>10} {'High':>10} {'Low':>10} {'Close':>10}{RESET}")
        for label, node in (("Prev", q.get("prev_ohlc")), ("Live", q.get("live_ohlc"))):
            line = _row(label, node)
            if line:
                print(line)
        print()

    print(f"  {DIM}Instruments: {len(resolved)}{RESET}\n")


if __name__ == "__main__":
    main()
