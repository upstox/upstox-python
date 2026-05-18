"""
Balance Sheet — historical total assets, liabilities and equity over time.

Fetches balance sheet history from the Upstox Fundamentals API and displays
assets vs liabilities for each reporting period.

Usage:
  python fundamentals/balance_sheet.py --token <TOKEN>
  python fundamentals/balance_sheet.py --token <TOKEN> --symbol HDFCBANK
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


def resolve_symbol(client, symbol: str):
    resp = search_instrument(client, symbol, exchanges="NSE", segments="EQ", records=1)
    hits = resp.data or []
    if not hits:
        die(f"No NSE equity instrument found for '{symbol}'.")
    return hits[0].get("isin", ""), hits[0].get("instrument_key", "")


def _val(obj, key, default="—"):
    if obj is None:
        return default
    if isinstance(obj, dict):
        v = obj.get(key)
    else:
        v = getattr(obj, key, None)
    return v if v is not None else default


def _fmt(v):
    if v in (None, "—", ""):
        return "—"
    try:
        return f"{float(v):>16,.2f}"
    except (TypeError, ValueError):
        return str(v)


def main():
    parser = argparse.ArgumentParser(description="Balance Sheet via Fundamentals API")
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

    print(f"\nFetching balance sheet for {args.symbol.upper()} (ISIN: {isin})"
          f" — type={args.type}, fs={args.fs}...\n")

    api = upstox_client.FundamentalsApi(client)
    try:
        response = api.get_balance_sheet(isin, type=args.type, fs=args.fs)
    except Exception as e:
        die(f"API error: {e}")

    data = response.data
    if not data:
        die("No data returned.")

    raw = data.to_dict() if hasattr(data, "to_dict") else (data if isinstance(data, dict) else vars(data))

    units   = raw.get("units_in") or ""
    period  = raw.get("time_period") or ""
    history = raw.get("history") or []

    units_label = f" (in {units})" if units else ""
    print(f"  Period type  : {period or '—'}")
    print(f"  Units        : {units or '—'}")
    print()

    if history:
        col_w = 14
        print(f"  {BOLD}{'Period':<{col_w}} {'Total Assets':>18} {'Total Liabilities':>20} {'Equity':>18}{RESET}")
        print("  " + "─" * 72)

        for entry in history:
            if hasattr(entry, "to_dict"):
                entry = entry.to_dict()
            elif not isinstance(entry, dict):
                entry = vars(entry) if hasattr(entry, "__dict__") else {}

            p    = str(_val(entry, "period", "—"))
            ta   = _val(entry, "total_asset")
            tl   = _val(entry, "total_liability")
            eq   = None
            try:
                if ta not in (None, "—") and tl not in (None, "—"):
                    eq = float(ta) - float(tl)
            except (TypeError, ValueError):
                pass

            ta_s = _fmt(ta).strip()
            tl_s = _fmt(tl).strip()
            eq_s = _fmt(eq).strip() if eq is not None else "—"

            print(f"  {CYAN}{p:<{col_w}}{RESET} {ta_s:>18} {tl_s:>20} {GREEN}{eq_s:>18}{RESET}")
    else:
        # fall back to full_statement if history is empty
        full = raw.get("full_statement") or []
        if not full:
            die("No balance sheet data in response.")

        items = full if isinstance(full, list) else [full]
        print(f"  {BOLD}{'Particular':<40} {'Value':>18}{RESET}")
        print("  " + "─" * 62)
        for entry in items:
            if hasattr(entry, "to_dict"):
                entry = entry.to_dict()
            elif not isinstance(entry, dict):
                entry = vars(entry) if hasattr(entry, "__dict__") else {}
            particular = str(entry.get("particular") or "—")
            hist_vals  = entry.get("history") or []
            last = hist_vals[-1] if hist_vals else None
            if isinstance(last, dict):
                val = last.get("value")
            elif hasattr(last, "to_dict"):
                val = last.to_dict().get("value")
            else:
                val = last
            print(f"  {CYAN}{particular:<40}{RESET} {_fmt(val).strip():>18}")

    print()


if __name__ == "__main__":
    main()
