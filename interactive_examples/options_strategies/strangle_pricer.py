"""
OTM Strangle Pricer.

A long strangle = Buy OTM Call + Buy OTM Put (different strikes, same expiry).
Cheaper than a straddle but requires a larger move to profit.

This script uses atm_offset to select OTM strikes:
  atm_offset=+1 → one strike above ATM for CE
  atm_offset=-1 → one strike below ATM for PE

Usage:
  python options_strategies/strangle_pricer.py --token <TOKEN>
  python options_strategies/strangle_pricer.py --token <TOKEN> --query BANKNIFTY --offset 2
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import get_api_client, search_instrument, get_ltp


def main():
    parser = argparse.ArgumentParser(description="OTM strangle cost and breakevens")
    parser.add_argument("--token", required=True, help="Upstox access token or analytics token")
    parser.add_argument("--query", default="NIFTY", help="Underlying symbol (default: NIFTY)")
    parser.add_argument("--expiry", default="current_month", help="Expiry (default: current_month)")
    parser.add_argument("--offset", type=int, default=1, help="OTM offset strikes (default: 1)")
    args = parser.parse_args()

    client = get_api_client(args.token)

    print(f"Pricing {args.offset}-strike OTM strangle for {args.query} ({args.expiry})...\n")

    # OTM call = ATM + offset, OTM put = ATM - offset
    ce_resp = search_instrument(client, args.query, exchanges="NSE", segments="FO",
                                instrument_types="CE", expiry=args.expiry,
                                atm_offset=args.offset, records=1)
    pe_resp = search_instrument(client, args.query, exchanges="NSE", segments="FO",
                                instrument_types="PE", expiry=args.expiry,
                                atm_offset=-args.offset, records=1)

    ce_list = ce_resp.data or []
    pe_list = pe_resp.data or []

    if not ce_list or not pe_list:
        print("Could not find strangle legs. Try different symbol, expiry, or offset.")
        sys.exit(1)

    ce = ce_list[0]
    pe = pe_list[0]
    ce_strike = ce.get("strike_price", 0)
    pe_strike = pe.get("strike_price", 0)
    lot_size = ce.get("lot_size", 1)

    keys = [ce["instrument_key"], pe["instrument_key"]]
    ltp_data = get_ltp(client, *keys)

    ce_price = ltp_data[ce["instrument_key"]].last_price
    pe_price = ltp_data[pe["instrument_key"]].last_price

    strangle_cost = ce_price + pe_price
    upper_breakeven = ce_strike + strangle_cost
    lower_breakeven = pe_strike - strangle_cost
    profit_zone_width = upper_breakeven - lower_breakeven

    print(f"{'Leg':<10} {'Symbol':<30} {'Strike':>10} {'LTP':>10}")
    print("-" * 65)
    print(f"{'Call (+{0})':<10} {ce['trading_symbol']:<30} {ce_strike:>10.2f} {ce_price:>10.2f}".format(args.offset))
    print(f"{'Put (-{0})':<10} {pe['trading_symbol']:<30} {pe_strike:>10.2f} {pe_price:>10.2f}".format(args.offset))
    print("-" * 65)

    print(f"\nStrangle width     : {ce_strike - pe_strike:.2f} points  ({ce_strike:.0f} CE / {pe_strike:.0f} PE)")
    print(f"Total premium      : {strangle_cost:.2f}  (CE {ce_price:.2f} + PE {pe_price:.2f})")
    print(f"Lot size           : {lot_size}")
    print(f"Total cost/lot     : ₹{strangle_cost * lot_size:,.2f}")
    print()
    print(f"Upper breakeven    : {upper_breakeven:,.2f}")
    print(f"Lower breakeven    : {lower_breakeven:,.2f}")
    print(f"Profit zone width  : {profit_zone_width:,.2f} points")
    print(f"Max loss (at exp)  : ₹{strangle_cost * lot_size:,.2f} per lot  (if underlying stays between {pe_strike:.0f}–{ce_strike:.0f})")


if __name__ == "__main__":
    main()
