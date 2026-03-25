"""
Pairwise Stock Correlation — Pearson correlation of daily returns for 2+ stocks.

Useful for pairs trading and portfolio diversification:
  R close to +1  → stocks move together (correlated)
  R close to  0  → no linear relationship (diversified)
  R close to -1  → stocks move opposite (natural hedge)

Usage:
  python historical_analysis/stock_correlation.py --token <TOKEN>
  python historical_analysis/stock_correlation.py --token <TOKEN> --queries RELIANCE,TCS,INFY,HDFCBANK --days 90
"""

import argparse
import sys
import os
import math
from statistics import mean
from datetime import date, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import get_api_client, search_instrument, get_historical_candles

BOLD  = "\033[1m"
GREEN = "\033[32m"
RED   = "\033[31m"
CYAN  = "\033[36m"
DIM   = "\033[2m"
RESET = "\033[0m"


def daily_returns(closes):
    return [(closes[i] / closes[i - 1]) - 1 for i in range(1, len(closes))]


def pearson(xs, ys):
    n = len(xs)
    if n < 3:
        return 0
    mx, my = mean(xs), mean(ys)
    num = sum((xs[i] - mx) * (ys[i] - my) for i in range(n))
    dx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    dy = math.sqrt(sum((y - my) ** 2 for y in ys))
    if dx == 0 or dy == 0:
        return 0
    return num / (dx * dy)


def main():
    parser = argparse.ArgumentParser(description="Pairwise stock return correlation")
    parser.add_argument("--token",   required=True, help="Upstox access or analytics token")
    parser.add_argument("--queries", default="RELIANCE,TCS,INFY",
                        help="Comma-separated stock names (default: RELIANCE,TCS,INFY)")
    parser.add_argument("--days",    type=int, default=60,
                        help="Trading days (default: 60)")
    args = parser.parse_args()

    queries = [q.strip() for q in args.queries.split(",") if q.strip()]
    if len(queries) < 2:
        print("Need at least 2 stocks. Use --queries STOCK1,STOCK2,...")
        sys.exit(1)

    client = get_api_client(args.token)

    print(f"\nComputing correlation for {', '.join(queries)} ({args.days} days)...\n")

    to_date = date.today().isoformat()
    from_date = (date.today() - timedelta(days=int(args.days * 1.6))).isoformat()

    # Resolve and fetch data for each stock
    symbols = []
    all_returns = []

    for query in queries:
        resp = search_instrument(client, query, exchanges="NSE", segments="EQ", records=3)
        hits = resp.data or []
        if not hits:
            print(f"  Warning: '{query}' not found on NSE. Skipping.")
            continue

        inst_key = hits[0]["instrument_key"]
        symbol = hits[0].get("trading_symbol", query.upper())

        candles = get_historical_candles(client, inst_key, "days", 1, to_date, from_date)
        if not candles:
            print(f"  Warning: no data for '{symbol}'. Skipping.")
            continue

        closes = [float(c[4]) for c in reversed(candles) if len(c) > 4]
        if len(closes) < 10:
            print(f"  Warning: insufficient data for '{symbol}' ({len(closes)} days). Skipping.")
            continue

        symbols.append(symbol)
        all_returns.append(daily_returns(closes))

    if len(symbols) < 2:
        print("Need at least 2 valid stocks with data.")
        sys.exit(1)

    # Align all return series to the shortest length
    min_len = min(len(r) for r in all_returns)
    all_returns = [r[-min_len:] for r in all_returns]

    print(f"  Stocks: {', '.join(symbols)}")
    print(f"  Period: {min_len} trading days\n")

    # Compute and display correlation matrix
    n = len(symbols)
    max_sym_len = max(len(s) for s in symbols)
    col_width = max(max_sym_len, 8)

    # Header
    header = " " * (max_sym_len + 2)
    for s in symbols:
        header += f"{s:>{col_width}}  "
    print(header)
    print(" " * (max_sym_len + 2) + "-" * ((col_width + 2) * n))

    for i in range(n):
        row = f"{symbols[i]:>{max_sym_len}}  "
        for j in range(n):
            r = pearson(all_returns[i], all_returns[j])
            if i == j:
                row += f"{DIM}{'1.000':>{col_width}}{RESET}  "
            elif r > 0.7:
                row += f"{GREEN}{r:>{col_width}.3f}{RESET}  "
            elif r < -0.3:
                row += f"{RED}{r:>{col_width}.3f}{RESET}  "
            else:
                row += f"{r:>{col_width}.3f}  "
        print(row)

    # Highlight strongest and weakest pairs
    print()
    pairs = []
    for i in range(n):
        for j in range(i + 1, n):
            r = pearson(all_returns[i], all_returns[j])
            pairs.append((symbols[i], symbols[j], r))

    if pairs:
        pairs.sort(key=lambda p: p[2])
        lowest = pairs[0]
        highest = pairs[-1]
        print(f"  {GREEN}Most correlated{RESET}  : {highest[0]} & {highest[1]}  "
              f"(R = {highest[2]:.3f})")
        print(f"  {RED}Least correlated{RESET} : {lowest[0]} & {lowest[1]}  "
              f"(R = {lowest[2]:.3f})")

        if lowest[2] < 0.3:
            print(f"\n  {CYAN}Diversification opportunity{RESET}: "
                  f"{lowest[0]} and {lowest[1]} have low correlation — "
                  f"holding both reduces portfolio volatility.")
    print()


if __name__ == "__main__":
    main()
