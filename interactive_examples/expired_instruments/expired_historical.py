"""
Expired Historical Candles — OHLC history for an expired contract.

Uses the Upstox Expired Instrument API. This example self-resolves a usable
expired contract: underlying → past expiry → first expired future contract →
its historical candles. Supply --expired-key to target a specific contract
directly (e.g. one printed by expired_future_contracts.py).

Intervals: 1minute, 30minute, day, week, month.

Usage:
  python expired_instruments/expired_historical.py --token <TOKEN>
  python expired_instruments/expired_historical.py --token <TOKEN> --query BANKNIFTY --interval day
  python expired_instruments/expired_historical.py --token <TOKEN> \
      --expired-key "NSE_FO|12345|26-12-2024" --from 2024-11-01 --to 2024-12-26
"""

import argparse
import sys
import os
from datetime import date, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import get_api_client, resolve_underlying, as_dict, die
import upstox_client

BOLD  = "\033[1m"
GREEN = "\033[32m"
RED   = "\033[31m"
CYAN  = "\033[36m"
DIM   = "\033[2m"
RESET = "\033[0m"


def _pick_expired_contract(api, underlying_key, expiry):
    """Return an expired future contract's instrument_key for the given expiry."""
    resp = api.get_expired_future_contracts(underlying_key, expiry)
    contracts = resp.data or []
    if not contracts:
        return None
    return as_dict(contracts[0]).get("instrument_key")


def main():
    parser = argparse.ArgumentParser(description="Expired historical candles via Expired Instrument API")
    parser.add_argument("--token",  required=True, help="Upstox access or analytics token")
    parser.add_argument("--query",  default="NIFTY", help="Underlying symbol (default: NIFTY)")
    parser.add_argument("--expired-key", default=None,
                        help="Target a specific expired instrument key directly")
    parser.add_argument("--interval", default="day",
                        choices=("1minute", "30minute", "day", "week", "month"),
                        help="Candle interval (default: day)")
    parser.add_argument("--from", dest="from_date", default=None, help="From date YYYY-MM-DD")
    parser.add_argument("--to",   dest="to_date",   default=None, help="To date YYYY-MM-DD")
    args = parser.parse_args()

    client = get_api_client(args.token)
    api = upstox_client.ExpiredInstrumentApi(client)

    expired_key = args.expired_key
    if not expired_key:
        inst = resolve_underlying(client, args.query)
        if not inst:
            die(f"Could not resolve an underlying for '{args.query}'.")
        underlying_key = inst.get("instrument_key", "")
        try:
            expiries = api.get_expiries(underlying_key).data or []
        except Exception as e:
            die(f"API error fetching expiries: {e}")
        past = sorted(e for e in (str(x) for x in expiries) if e < date.today().isoformat())
        if not past:
            die("No past expiry found to demonstrate expired historical data.")
        expiry = past[-1]
        expired_key = _pick_expired_contract(api, underlying_key, expiry)
        if not expired_key:
            die(f"No expired contract found for expiry {expiry}.")
        print(f"\n{DIM}Auto-selected expired contract {expired_key} (expiry {expiry}).{RESET}")

    to_date = args.to_date or date.today().isoformat()
    from_date = args.from_date or (date.today() - timedelta(days=180)).isoformat()

    print(f"\n{BOLD}Fetching expired historical candles{RESET} "
          f"key={expired_key} interval={args.interval} {from_date}→{to_date}...\n")

    try:
        response = api.get_expired_historical_candle_data(
            expired_key, args.interval, to_date, from_date)
    except Exception as e:
        die(f"API error: {e}")

    candles = getattr(response.data, "candles", None) or []
    if not candles:
        die("No candles returned for that range.")

    print(f"  {BOLD}{'Timestamp':<26} {'Open':>10} {'High':>10} {'Low':>10} {'Close':>10} {'Volume':>12}{RESET}")
    print("  " + "─" * 92)
    for c in candles[:30]:
        ts, o, h, l, cl, vol = c[0], c[1], c[2], c[3], c[4], c[5]
        colour = GREEN if cl >= o else RED
        print(f"  {str(ts):<26} {o:>10,.2f} {h:>10,.2f} {l:>10,.2f} "
              f"{colour}{cl:>10,.2f}{RESET} {vol:>12,}")

    print(f"\n  {DIM}Showing {min(len(candles), 30)} of {len(candles)} candles.{RESET}\n")


if __name__ == "__main__":
    main()
