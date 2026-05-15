"""
Income Statement — revenue, profit and EPS trends across reporting periods.

Fetches the income statement from the Upstox Fundamentals API and displays
key line items (revenue, operating profit, net profit, EPS) over time.

Usage:
  python fundamentals/income_statement.py --token <TOKEN>
  python fundamentals/income_statement.py --token <TOKEN> --symbol TCS
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import get_api_client, search_instrument, die
import upstox_client

BOLD  = "\033[1m"
GREEN = "\033[32m"
CYAN  = "\033[36m"
RESET = "\033[0m"

# Line items to highlight at the top of the table
PRIORITY_ITEMS = (
    "revenue", "net revenue", "total revenue", "net sales", "total income",
    "operating profit", "ebitda", "ebit",
    "profit before tax", "pbt",
    "net profit", "pat", "profit after tax",
    "eps", "earnings per share",
)


def resolve_symbol(client, symbol: str):
    resp = search_instrument(client, symbol, exchanges="NSE", segments="EQ", records=1)
    hits = resp.data or []
    if not hits:
        die(f"No NSE equity instrument found for '{symbol}'.")
    return hits[0].get("isin", ""), hits[0].get("instrument_key", "")


def _fmt(v):
    if v in (None, "", "—"):
        return "—"
    try:
        return f"{float(v):>14,.2f}"
    except (TypeError, ValueError):
        return str(v)[:14]


def _is_priority(name: str) -> bool:
    nl = name.lower()
    return any(k in nl for k in PRIORITY_ITEMS)


def _print_table(entries, periods):
    max_cols = 6
    periods = periods[:max_cols]
    col_w   = 14
    label_w = 38

    header_periods = "  ".join(f"{str(p)[:col_w]:>{col_w}}" for p in periods)
    print(f"  {BOLD}{'Particular':<{label_w}} {header_periods}{RESET}")
    print("  " + "─" * (label_w + (col_w + 2) * len(periods)))

    for name, hist in entries:
        vals = (hist or [])[:max_cols]
        while len(vals) < len(periods):
            vals.append(None)
        row_vals = "  ".join(f"{_fmt(v).strip():>{col_w}}" for v in vals)
        color = CYAN if _is_priority(name) else ""
        print(f"  {color}{str(name):<{label_w}}{RESET} {row_vals}")


def main():
    parser = argparse.ArgumentParser(description="Income Statement via Fundamentals API")
    parser.add_argument("--token",  required=True, help="Upstox access or analytics token")
    parser.add_argument("--symbol", default="RELIANCE", help="Stock symbol (default: RELIANCE)")
    args = parser.parse_args()

    client = get_api_client(args.token)
    isin, _ = resolve_symbol(client, args.symbol)
    if not isin:
        die(f"Could not resolve ISIN for '{args.symbol}'.")

    print(f"\nFetching income statement for {args.symbol.upper()} (ISIN: {isin})...\n")

    api = upstox_client.FundamentalsApi(client)
    try:
        response = api.get_income_statement(isin)
    except Exception as e:
        die(f"API error: {e}")

    data = response.data
    if not data:
        die("No data returned.")

    raw = data.to_dict() if hasattr(data, "to_dict") else (data if isinstance(data, dict) else vars(data))

    units  = raw.get("units_in") or ""
    period = raw.get("time_period") or ""
    stmts  = raw.get("income_statement") or raw.get("full_statement") or []

    print(f"  Period type  : {period or '—'}")
    print(f"  Units        : {units or '—'}")
    print()

    if not stmts:
        die("No income statement entries found.")

    items = stmts if isinstance(stmts, list) else [stmts]

    entries = []
    periods = []
    for item in items:
        if hasattr(item, "to_dict"):
            item = item.to_dict()
        elif not isinstance(item, dict):
            item = vars(item) if hasattr(item, "__dict__") else {}
        name = str(item.get("particular") or item.get("name") or "—")
        hist = item.get("history") or []
        if not periods and hist:
            # try to find period labels from sibling "period" key or index
            periods = list(range(1, len(hist) + 1))
        entries.append((name, hist))

    if not entries:
        die("No line items found.")

    # Sort: priority items first
    priority = [(n, h) for n, h in entries if _is_priority(n)]
    rest     = [(n, h) for n, h in entries if not _is_priority(n)]

    _print_table(priority + rest, periods)
    print()


if __name__ == "__main__":
    main()
