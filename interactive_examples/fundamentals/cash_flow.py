"""
Cash Flow — operating, investing and financing cash flows across periods.

Fetches the cash flow statement from the Upstox Fundamentals API and displays
operating / investing / financing activities alongside net cash flow over time.

Usage:
  python fundamentals/cash_flow.py --token <TOKEN>
  python fundamentals/cash_flow.py --token <TOKEN> --symbol WIPRO
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import get_api_client, search_instrument, die
import upstox_client

BOLD  = "\033[1m"
GREEN = "\033[32m"
RED   = "\033[31m"
CYAN  = "\033[36m"
RESET = "\033[0m"

PRIORITY_ITEMS = (
    "operating", "cash from operations", "net cash from operating",
    "investing", "cash from investing", "net cash from investing",
    "financing", "cash from financing", "net cash from financing",
    "net cash", "net change",
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
        f = float(v)
        color = GREEN if f > 0 else (RED if f < 0 else "")
        return f"{color}{f:>14,.2f}{RESET}"
    except (TypeError, ValueError):
        return str(v)[:14]


def _is_priority(name: str) -> bool:
    nl = name.lower()
    return any(k in nl for k in PRIORITY_ITEMS)


def main():
    parser = argparse.ArgumentParser(description="Cash Flow via Fundamentals API")
    parser.add_argument("--token",  required=True, help="Upstox access or analytics token")
    parser.add_argument("--symbol", default="RELIANCE", help="Stock symbol (default: RELIANCE)")
    parser.add_argument("--type",   default="consolidated",
                        choices=("consolidated", "standalone"),
                        help="Statement type (default: consolidated)")
    parser.add_argument("--fs",     default="false", choices=("true", "false"),
                        help="Full statement toggle — include detailed line-item breakdown (default: false)")
    args = parser.parse_args()

    client = get_api_client(args.token)
    isin, _ = resolve_symbol(client, args.symbol)
    if not isin:
        die(f"Could not resolve ISIN for '{args.symbol}'.")

    print(f"\nFetching cash flow statement for {args.symbol.upper()} (ISIN: {isin})"
          f" — type={args.type}, fs={args.fs}...\n")

    api = upstox_client.FundamentalsApi(client)
    try:
        response = api.get_cash_flow(isin, type=args.type, fs=args.fs)
    except Exception as e:
        die(f"API error: {e}")

    data = response.data
    if not data:
        die("No data returned.")

    raw = data.to_dict() if hasattr(data, "to_dict") else (data if isinstance(data, dict) else vars(data))

    units  = raw.get("units_in") or ""
    period = raw.get("time_period") or ""
    stmts  = raw.get("cash_flow") or raw.get("full_statement") or []

    print(f"  Period type  : {period or '—'}")
    print(f"  Units        : {units or '—'}")
    print()

    if not stmts:
        die("No cash flow entries found.")

    items = stmts if isinstance(stmts, list) else [stmts]

    def _flat(hist):
        out = []
        for h in (hist or []):
            if hasattr(h, "to_dict"):
                h = h.to_dict()
            if isinstance(h, dict):
                out.append((h.get("period"), h.get("value")))
            else:
                out.append((None, h))
        return out

    entries = []
    periods = []
    max_cols = 6

    for item in items:
        if hasattr(item, "to_dict"):
            item = item.to_dict()
        elif not isinstance(item, dict):
            item = vars(item) if hasattr(item, "__dict__") else {}
        name = str(item.get("category") or item.get("particular") or item.get("name") or "—")
        flat = _flat(item.get("history"))
        if not periods and flat:
            periods = [p if p is not None else f"P{i+1}" for i, (p, _) in enumerate(flat)]
        entries.append((name, [v for _, v in flat]))

    if not entries:
        die("No line items found.")

    periods = periods[:max_cols]
    col_w   = 16
    label_w = 38

    header_periods = "  ".join(f"{str(p)[:col_w]:>{col_w}}" for p in periods)
    print(f"  {BOLD}{'Particular':<{label_w}} {header_periods}{RESET}")
    print("  " + "─" * (label_w + (col_w + 2) * len(periods) + 12))

    priority = [(n, h) for n, h in entries if _is_priority(n)]
    rest     = [(n, h) for n, h in entries if not _is_priority(n)]

    for name, hist in priority + rest:
        vals = (hist or [])[:max_cols]
        while len(vals) < len(periods):
            vals.append(None)
        row_vals = "  ".join(f"{_fmt(v):>{col_w + 9}}" for v in vals)
        color = CYAN if _is_priority(name) else ""
        print(f"  {color}{str(name):<{label_w}}{RESET} {row_vals}")

    print()


if __name__ == "__main__":
    main()
