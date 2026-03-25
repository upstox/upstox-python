"""
Option Greeks Dashboard — fetch live delta, gamma, theta, vega, and IV
for ATM ± N strikes using the MarketQuoteV3Api option-greeks endpoint.

Usage:
  python options_analytics/option_greeks.py --token <TOKEN>
  python options_analytics/option_greeks.py --token <TOKEN> --query BANKNIFTY --strikes 7
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import get_api_client, search_instrument
import upstox_client

BOLD  = "\033[1m"
GREEN = "\033[32m"
RED   = "\033[31m"
CYAN  = "\033[36m"
DIM   = "\033[2m"
RESET = "\033[0m"


def fetch_options(client, query: str, n: int, expiry: str):
    """Return list of (offset, instrument_dict) for CE and PE at ATM ±n."""
    instruments = []
    for offset in range(-n, n + 1):
        for itype in ("CE", "PE"):
            resp = search_instrument(client, query,
                                     exchanges="NSE", segments="FO",
                                     instrument_types=itype, expiry=expiry,
                                     atm_offset=offset, records=1)
            hits = resp.data or []
            if hits:
                instruments.append((offset, itype, hits[0]))
    return instruments


def g(obj, attr, default=None):
    if obj is None:
        return default
    return obj.get(attr, default) if isinstance(obj, dict) else getattr(obj, attr, default)


def fmt(val, digits=4, pct=False):
    if val is None:
        return "—"
    if pct:
        return f"{float(val)*100:.1f}%"
    return f"{float(val):.{digits}f}"


def main():
    parser = argparse.ArgumentParser(description="Option greeks dashboard: delta/gamma/theta/vega/IV")
    parser.add_argument("--token",   required=True,            help="Upstox access or analytics token")
    parser.add_argument("--query",   default="NIFTY",          help="Underlying symbol (default: NIFTY)")
    parser.add_argument("--strikes", type=int, default=5,
                        help="Strikes on each side of ATM (default: 5)")
    parser.add_argument("--expiry",  default="current_month",  help="Expiry (default: current_month)")
    args = parser.parse_args()

    client = get_api_client(args.token)

    print(f"\nFetching option greeks for {args.query.upper()} ({args.expiry}), "
          f"ATM ±{args.strikes} strikes...\n")

    instruments = fetch_options(client, args.query, args.strikes, args.expiry)
    if not instruments:
        print("No options found.")
        sys.exit(1)

    # Collect all instrument keys
    keys = [inst["instrument_key"] for _, _, inst in instruments]
    # API accepts up to 50 instruments
    keys = keys[:50]

    api  = upstox_client.MarketQuoteV3Api(client)
    resp = api.get_market_quote_option_greek(instrument_key=",".join(keys))
    greeks_data = resp.data or {}

    # Build lookup: instrument_token → greeks object
    def token_of(obj):
        return g(obj, "instrument_token")

    lookup = {}
    for val in greeks_data.values():
        tok = token_of(val)
        if tok:
            lookup[tok] = val

    # Header
    print(f"{'Offset':>7}  {'Strike':>10}  {'Type':>4}  {'LTP':>10}  "
          f"{'IV':>7}  {'Delta':>8}  {'Gamma':>8}  {'Theta':>8}  {'Vega':>8}  {'OI':>12}")
    print("─" * 98)

    # Group by strike for display
    rows = []
    for offset, itype, inst in instruments:
        key    = inst["instrument_key"]
        strike = inst.get("strike_price", 0)
        sym    = inst.get("trading_symbol", "")

        # Find greek data by instrument_token
        gdata  = lookup.get(key)
        ltp    = g(gdata, "last_price")
        iv     = g(gdata, "iv")
        delta  = g(gdata, "delta")
        gamma  = g(gdata, "gamma")
        theta  = g(gdata, "theta")
        vega   = g(gdata, "vega")
        oi     = g(gdata, "oi")

        rows.append((offset, strike, itype, ltp, iv, delta, gamma, theta, vega, oi))

    rows.sort(key=lambda r: (r[1], r[2]))  # sort by strike, then CE before PE

    prev_strike = None
    for offset, strike, itype, ltp, iv, delta, gamma, theta, vega, oi in rows:
        if prev_strike and strike != prev_strike:
            print(f"{'':7}  {'─'*10}")
        prev_strike = strike

        is_atm  = offset == 0
        colour  = CYAN if is_atm else (GREEN if itype == "CE" else RED)
        off_str = f"ATM" if is_atm else f"{offset:+d}"
        oi_str  = f"{int(oi):,}" if oi else "—"
        ltp_str = f"{float(ltp):,.2f}" if ltp else "—"

        print(f"{colour}{off_str:>7}{RESET}  "
              f"{BOLD if is_atm else ''}{strike:>10,.0f}{RESET}  "
              f"{colour}{itype:>4}{RESET}  "
              f"{ltp_str:>10}  "
              f"{fmt(iv, pct=True):>7}  "
              f"{fmt(delta):>8}  "
              f"{fmt(gamma, 6):>8}  "
              f"{fmt(theta):>8}  "
              f"{fmt(vega):>8}  "
              f"{oi_str:>12}")

    print("─" * 98)
    print(f"\n  {DIM}Delta: directional sensitivity  |  Gamma: delta rate-of-change  |  "
          f"Theta: daily time decay  |  Vega: IV sensitivity{RESET}\n")


if __name__ == "__main__":
    main()
