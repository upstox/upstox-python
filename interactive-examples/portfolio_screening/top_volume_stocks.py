"""
Top Volume Stocks Scanner.

Searches for a list of well-known stocks, fetches their full market quotes,
and ranks them by trading volume (and optionally by % change).

This demonstrates using instrument search + get_full_market_quote together
to build a simple market scanner.

Usage:
  python portfolio_screening/top_volume_stocks.py --token <TOKEN>
  python portfolio_screening/top_volume_stocks.py --token <TOKEN> --sort change
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import get_api_client, search_instrument, get_full_quote

# Representative large-cap Nifty 50 stocks
DEFAULT_STOCKS = [
    "RELIANCE", "HDFCBANK", "INFY", "TCS", "ICICIBANK",
    "BHARTIARTL", "SBIN", "WIPRO", "HCLTECH", "AXISBANK",
    "LT", "KOTAKBANK", "TITAN", "ASIANPAINT", "MARUTI",
]


def find_equity(client, symbol):
    resp = search_instrument(client, symbol, exchanges="NSE", segments="EQ", records=3)
    data = resp.data or []
    for inst in data:
        if symbol.upper() == inst.get("trading_symbol", "").upper():
            return inst
    return data[0] if data else None


def main():
    parser = argparse.ArgumentParser(description="Rank stocks by volume or price change")
    parser.add_argument("--token", required=True, help="Upstox access token or analytics token")
    parser.add_argument(
        "--stocks",
        default=",".join(DEFAULT_STOCKS),
        help="Comma-separated list of stock symbols",
    )
    parser.add_argument(
        "--sort", default="volume", choices=["volume", "change", "ltp"],
        help="Sort by: volume, change (%% change), ltp (default: volume)",
    )
    parser.add_argument("--top", type=int, default=10, help="Show top N results (default: 10)")
    args = parser.parse_args()

    client = get_api_client(args.token)
    symbols = [s.strip() for s in args.stocks.split(",")]

    print(f"Resolving {len(symbols)} instruments on NSE...\n")

    inst_map = {}
    for sym in symbols:
        inst = find_equity(client, sym)
        if inst:
            inst_map[sym] = inst

    if not inst_map:
        print("No instruments found.")
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
        chg     = ltp - prev
        chg_pct = (chg / prev * 100) if prev else 0
        volume  = q.volume or 0
        oi      = q.oi or 0
        rows.append({
            "symbol": sym,
            "ltp": ltp,
            "prev": prev,
            "chg": chg,
            "chg_pct": chg_pct,
            "volume": volume,
            "oi": oi,
        })

    sort_key = {"volume": "volume", "change": "chg_pct", "ltp": "ltp"}[args.sort]
    rows.sort(key=lambda r: abs(r[sort_key]) if sort_key == "chg_pct" else r[sort_key], reverse=True)
    rows = rows[: args.top]

    print(f"Top {args.top} stocks by {args.sort.upper()}\n")
    print(f"{'#':<4} {'Symbol':<15} {'LTP':>10} {'Prev':>10} {'Chg':>10} {'Chg%':>8} {'Volume':>15} {'OI':>12}")
    print("-" * 90)

    for i, r in enumerate(rows, 1):
        arrow = "▲" if r["chg"] >= 0 else "▼"
        print(
            f"{i:<4} {r['symbol']:<15} {r['ltp']:>10,.2f} {r['prev']:>10,.2f} "
            f"{r['chg']:>+10.2f} {r['chg_pct']:>+7.2f}% {r['volume']:>15,} {r['oi']:>12,.0f}  {arrow}"
        )


if __name__ == "__main__":
    main()
