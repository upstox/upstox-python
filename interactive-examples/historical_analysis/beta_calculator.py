"""
Stock Beta Calculator — measure a stock's volatility relative to NIFTY 50.

Beta = Cov(stock returns, index returns) / Var(index returns)

  Beta > 1  → stock is MORE volatile than the index (amplifies moves)
  Beta = 1  → stock moves in line with the index
  Beta < 1  → stock is LESS volatile (defensive)
  Beta < 0  → stock moves OPPOSITE to the index (rare)

Also reports the Pearson correlation coefficient (R) between returns.

Usage:
  python historical_analysis/beta_calculator.py --token <TOKEN>
  python historical_analysis/beta_calculator.py --token <TOKEN> --query TCS --days 90
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
RESET = "\033[0m"

NIFTY_KEY = "NSE_INDEX|Nifty 50"


def daily_returns(closes):
    return [(closes[i] / closes[i - 1]) - 1 for i in range(1, len(closes))]


def covariance(xs, ys):
    n = len(xs)
    mx, my = mean(xs), mean(ys)
    return sum((xs[i] - mx) * (ys[i] - my) for i in range(n)) / (n - 1)


def variance(xs):
    mx = mean(xs)
    return sum((x - mx) ** 2 for x in xs) / (len(xs) - 1)


def correlation(xs, ys):
    cov = covariance(xs, ys)
    std_x = math.sqrt(variance(xs))
    std_y = math.sqrt(variance(ys))
    if std_x == 0 or std_y == 0:
        return 0
    return cov / (std_x * std_y)


def main():
    parser = argparse.ArgumentParser(description="Stock beta vs NIFTY 50")
    parser.add_argument("--token", required=True, help="Upstox access or analytics token")
    parser.add_argument("--query", default="RELIANCE", help="Stock name (default: RELIANCE)")
    parser.add_argument("--days",  type=int, default=60,
                        help="Trading days for calculation (default: 60)")
    args = parser.parse_args()

    client = get_api_client(args.token)

    print(f"\nComputing beta for {args.query.upper()} vs NIFTY 50 ({args.days} days)...\n")

    # Resolve stock instrument key
    resp = search_instrument(client, args.query, exchanges="NSE", segments="EQ", records=3)
    hits = resp.data or []
    if not hits:
        print(f"Stock '{args.query}' not found on NSE.")
        sys.exit(1)

    stock_key = hits[0]["instrument_key"]
    trading_symbol = hits[0].get("trading_symbol", args.query.upper())

    # Fetch historical data for both stock and NIFTY
    to_date = date.today().isoformat()
    from_date = (date.today() - timedelta(days=int(args.days * 1.6))).isoformat()

    stock_candles = get_historical_candles(client, stock_key, "days", 1, to_date, from_date)
    nifty_candles = get_historical_candles(client, NIFTY_KEY, "days", 1, to_date, from_date)

    if not stock_candles or not nifty_candles:
        print("Could not fetch historical data.")
        sys.exit(1)

    # Reverse to chronological, extract closes
    stock_closes = [float(c[4]) for c in reversed(stock_candles) if len(c) > 4]
    nifty_closes = [float(c[4]) for c in reversed(nifty_candles) if len(c) > 4]

    # Align lengths
    min_len = min(len(stock_closes), len(nifty_closes))
    stock_closes = stock_closes[-min_len:]
    nifty_closes = nifty_closes[-min_len:]

    if min_len < args.days:
        print(f"Warning: only {min_len} common trading days available (requested {args.days}).")

    if min_len < 10:
        print(f"Insufficient data: {min_len} days.")
        sys.exit(1)

    stock_rets = daily_returns(stock_closes)
    nifty_rets = daily_returns(nifty_closes)

    # Compute beta and correlation
    cov = covariance(stock_rets, nifty_rets)
    var_idx = variance(nifty_rets)
    beta = cov / var_idx if var_idx else 0
    corr = correlation(stock_rets, nifty_rets)

    # Annualised volatility
    stock_vol = math.sqrt(variance(stock_rets)) * math.sqrt(252) * 100
    nifty_vol = math.sqrt(variance(nifty_rets)) * math.sqrt(252) * 100

    # Display
    print(f"  Stock          : {trading_symbol}")
    print(f"  Benchmark      : NIFTY 50")
    print(f"  Period         : {min_len} trading days")
    print(f"  Stock close    : {stock_closes[-1]:,.2f}")
    print(f"  NIFTY close    : {nifty_closes[-1]:,.2f}")
    print()
    print(f"  {BOLD}Beta           : {beta:.3f}{RESET}")
    print(f"  {BOLD}Correlation (R): {corr:.3f}{RESET}")
    print()
    print(f"  Stock annl vol : {stock_vol:.1f}%")
    print(f"  NIFTY annl vol : {nifty_vol:.1f}%")
    print()

    if beta > 1.2:
        print(f"  {RED}High beta{RESET} — {trading_symbol} amplifies NIFTY moves. "
              f"More volatile/aggressive.")
    elif beta > 0.8:
        print(f"  {CYAN}Moderate beta{RESET} — {trading_symbol} tracks NIFTY closely.")
    elif beta > 0:
        print(f"  {GREEN}Low beta{RESET} — {trading_symbol} is defensive relative to NIFTY.")
    else:
        print(f"  {RED}Negative beta{RESET} — {trading_symbol} tends to move opposite to NIFTY.")

    if abs(corr) > 0.7:
        print(f"  Strong correlation ({corr:.2f}) — returns are highly aligned with NIFTY.")
    elif abs(corr) > 0.4:
        print(f"  Moderate correlation ({corr:.2f}) — some alignment with NIFTY.")
    else:
        print(f"  Weak correlation ({corr:.2f}) — returns diverge significantly from NIFTY.")
    print()


if __name__ == "__main__":
    main()
