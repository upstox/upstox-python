"""
Futures OI Buildup Scanner.

Searches for near-month futures of multiple stocks, fetches their
full market quotes, and ranks them by Open Interest (OI) to identify:

  - Long buildup   : Price ↑ + OI ↑  → fresh long positions being added (bullish)
  - Short buildup  : Price ↓ + OI ↑  → fresh short positions being added (bearish)
  - Long unwinding : Price ↓ + OI ↓  → longs exiting (bearish)
  - Short covering : Price ↑ + OI ↓  → shorts covering (bullish)

Usage:
  python portfolio_screening/futures_oi_buildup.py --token <TOKEN>
  python portfolio_screening/futures_oi_buildup.py --token <TOKEN> --sort oi
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import get_api_client, search_instrument, get_full_quote

DEFAULT_STOCKS = [
    "RELIANCE", "HDFCBANK", "INFY", "TCS", "ICICIBANK",
    "BHARTIARTL", "SBIN", "WIPRO", "HCLTECH", "AXISBANK",
    "LT", "KOTAKBANK", "TITAN", "ASIANPAINT", "MARUTI",
]


def find_near_future(client, symbol):
    """Find the near-month futures contract for a stock."""
    resp = search_instrument(
        client, symbol,
        exchanges="NSE",
        segments="FO",
        instrument_types="FUT",
        expiry="current_month",
        records=1,
    )
    data = resp.data or []
    return data[0] if data else None


def classify_buildup(chg_pct, oi):
    """Classify OI buildup signal based on price and OI direction."""
    # We only have current OI snapshot, not OI change.
    # Use price change as proxy:
    if chg_pct > 0.5:
        return "Long Buildup"
    elif chg_pct < -0.5:
        return "Short Buildup"
    elif chg_pct > 0:
        return "Short Covering"
    else:
        return "Long Unwinding"


def main():
    parser = argparse.ArgumentParser(description="Futures OI buildup scanner")
    parser.add_argument("--token", required=True, help="Upstox access token or analytics token")
    parser.add_argument(
        "--stocks",
        default=",".join(DEFAULT_STOCKS),
        help="Comma-separated stock symbols",
    )
    parser.add_argument(
        "--sort", default="oi", choices=["oi", "change", "volume"],
        help="Sort by: oi, change, volume (default: oi)",
    )
    parser.add_argument("--top", type=int, default=10, help="Show top N (default: 10)")
    args = parser.parse_args()

    client = get_api_client(args.token)
    symbols = [s.strip() for s in args.stocks.split(",")]

    print(f"Scanning near-month futures OI for {len(symbols)} stocks...\n")

    inst_map = {}
    for sym in symbols:
        fut = find_near_future(client, sym)
        if fut:
            inst_map[sym] = fut
        else:
            print(f"  No futures found for {sym}, skipping.")

    if not inst_map:
        print("No futures found.")
        sys.exit(1)

    all_keys = [inst["instrument_key"] for inst in inst_map.values()]
    quote_data = get_full_quote(client, *all_keys)

    rows = []
    for sym, inst in inst_map.items():
        key = inst["instrument_key"]
        q = quote_data.get(key)
        if not q:
            continue
        ltp     = q.last_price or 0
        prev    = q.ohlc.close if q.ohlc else 0
        chg_pct = ((ltp - prev) / prev * 100) if prev else 0
        oi      = q.oi or 0
        volume  = q.volume or 0
        signal  = classify_buildup(chg_pct, oi)
        rows.append({
            "symbol": sym,
            "contract": inst.get("trading_symbol", ""),
            "ltp": ltp,
            "chg_pct": chg_pct,
            "oi": oi,
            "volume": volume,
            "signal": signal,
            "expiry": inst.get("expiry", ""),
        })

    sort_key = {"oi": "oi", "change": "chg_pct", "volume": "volume"}[args.sort]
    rows.sort(key=lambda r: r[sort_key], reverse=True)
    rows = rows[: args.top]

    print(f"{'#':<4} {'Symbol':<12} {'Contract':<22} {'LTP':>10} {'Chg%':>8} {'OI':>14} {'Volume':>12} {'Signal':}")
    print("-" * 100)

    for i, r in enumerate(rows, 1):
        arrow = "▲" if r["chg_pct"] >= 0 else "▼"
        print(
            f"{i:<4} {r['symbol']:<12} {r['contract']:<22} "
            f"{r['ltp']:>10,.2f} {r['chg_pct']:>+7.2f}% "
            f"{r['oi']:>14,.0f} {r['volume']:>12,}  {r['signal']} {arrow}"
        )

    # Summary by signal type
    print("\nSignal summary:")
    for sig in ["Long Buildup", "Short Buildup", "Short Covering", "Long Unwinding"]:
        count = sum(1 for r in rows if r["signal"] == sig)
        if count:
            print(f"  {sig:<20}: {count} stocks")


if __name__ == "__main__":
    main()
