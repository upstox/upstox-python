"""
Implied / Expected Move Calculator — how much the market expects a stock/index to move.

The expected move is derived from the ATM straddle premium for the nearest expiry:

  Expected Move = ATM CE premium + ATM PE premium
  Expected Move % = Expected Move / Spot Price × 100
  Upper bound = Spot + Expected Move
  Lower bound = Spot − Expected Move

Statistically, the actual price stays within ±1 expected move ~68% of the time
(one standard deviation assumption).

Usage:
  python options_analytics/implied_move.py --token <TOKEN>
  python options_analytics/implied_move.py --token <TOKEN> --query BANKNIFTY
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import get_api_client, search_instrument, get_ltp

BOLD  = "\033[1m"
GREEN = "\033[32m"
RED   = "\033[31m"
CYAN  = "\033[36m"
RESET = "\033[0m"

INDEX_LTP_KEYS = {
    "NIFTY":      "NSE_INDEX|Nifty 50",
    "BANKNIFTY":  "NSE_INDEX|Nifty Bank",
    "FINNIFTY":   "NSE_INDEX|Nifty Fin Service",
    "MIDCPNIFTY": "NSE_INDEX|NIFTY MID SELECT",
    "SENSEX":     "BSE_INDEX|SENSEX",
}


def main():
    parser = argparse.ArgumentParser(description="Implied/expected move from ATM straddle")
    parser.add_argument("--token",  required=True, help="Upstox access or analytics token")
    parser.add_argument("--query",  default="NIFTY", help="Underlying (default: NIFTY)")
    parser.add_argument("--expiry", default="current_month",
                        help="Expiry filter (default: current_month)")
    args = parser.parse_args()

    client = get_api_client(args.token)
    query_upper = args.query.upper()

    print(f"\nCalculating expected move for {query_upper}...\n")

    # Get spot price
    spot_key = INDEX_LTP_KEYS.get(query_upper)
    if spot_key:
        ltp_data = get_ltp(client, spot_key)
        entry = ltp_data.get(spot_key, {})
        spot = entry.get("last_price") if isinstance(entry, dict) else getattr(entry, "last_price", 0)
    else:
        resp = search_instrument(client, args.query, exchanges="NSE", segments="EQ", records=1)
        hits = resp.data or []
        if not hits:
            print(f"Cannot find '{args.query}'.")
            sys.exit(1)
        eq_key = hits[0]["instrument_key"]
        ltp_data = get_ltp(client, eq_key)
        entry = ltp_data.get(eq_key, {})
        spot = entry.get("last_price") if isinstance(entry, dict) else getattr(entry, "last_price", 0)

    if not spot:
        print("Could not fetch spot price.")
        sys.exit(1)

    # Find ATM CE and PE
    ce_resp = search_instrument(client, args.query, exchanges="NSE", segments="FO",
                                instrument_types="CE", expiry=args.expiry,
                                atm_offset=0, records=1)
    pe_resp = search_instrument(client, args.query, exchanges="NSE", segments="FO",
                                instrument_types="PE", expiry=args.expiry,
                                atm_offset=0, records=1)

    ce_hits = ce_resp.data or []
    pe_hits = pe_resp.data or []

    if not ce_hits or not pe_hits:
        print("Could not find ATM options. Try a different --expiry.")
        sys.exit(1)

    ce_key = ce_hits[0]["instrument_key"]
    pe_key = pe_hits[0]["instrument_key"]
    ce_strike = ce_hits[0].get("strike_price", 0)
    expiry_date = ce_hits[0].get("expiry", args.expiry)

    # Fetch LTP for both legs
    ltp_data = get_ltp(client, ce_key, pe_key)

    def get_price(data, key):
        entry = data.get(key, {})
        return entry.get("last_price") if isinstance(entry, dict) else getattr(entry, "last_price", 0)

    ce_premium = get_price(ltp_data, ce_key) or 0
    pe_premium = get_price(ltp_data, pe_key) or 0

    if not ce_premium and not pe_premium:
        print("Could not fetch ATM option premiums.")
        sys.exit(1)

    expected_move = ce_premium + pe_premium
    expected_move_pct = expected_move / spot * 100
    upper = spot + expected_move
    lower = spot - expected_move

    # Display
    print(f"  Underlying      : {query_upper}")
    print(f"  Spot price      : {spot:,.2f}")
    print(f"  ATM strike      : {ce_strike:,.0f}")
    print(f"  Expiry          : {expiry_date}")
    print()
    print(f"  ATM CE premium  : {ce_premium:,.2f}")
    print(f"  ATM PE premium  : {pe_premium:,.2f}")
    print(f"  Straddle cost   : {BOLD}{expected_move:,.2f}{RESET}")
    print()
    print(f"  {BOLD}Expected Move   : {expected_move:,.2f}  ({expected_move_pct:.2f}%){RESET}")
    print(f"  {GREEN}Upper bound     : {upper:,.2f}  (+{expected_move_pct:.2f}%){RESET}")
    print(f"  {RED}Lower bound     : {lower:,.2f}  (-{expected_move_pct:.2f}%){RESET}")
    print()
    print(f"  The market expects {query_upper} to stay within"
          f" {CYAN}{lower:,.2f} – {upper:,.2f}{RESET} by expiry (~68% probability).")
    print()


if __name__ == "__main__":
    main()
