"""
ATM Straddle Pricer.

A long straddle = Buy ATM Call + Buy ATM Put (same strike, same expiry).
Profit if the underlying moves sharply in either direction.

This script:
  1. Finds the ATM CE and PE using instrument search
  2. Fetches their live LTPs
  3. Computes total straddle cost, breakeven points, and max loss

Usage:
  python options_strategies/straddle_pricer.py --token <TOKEN>
  python options_strategies/straddle_pricer.py --token <TOKEN> --query BANKNIFTY --expiry current_week
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import get_api_client, search_instrument, get_ltp


def main():
    parser = argparse.ArgumentParser(description="ATM straddle cost and breakevens")
    parser.add_argument("--token", required=True, help="Upstox access token or analytics token")
    parser.add_argument("--query", default="NIFTY", help="Underlying symbol (default: NIFTY)")
    parser.add_argument("--expiry", default="current_month", help="Expiry (default: current_month)")
    args = parser.parse_args()

    client = get_api_client(args.token)

    print(f"Pricing ATM straddle for {args.query} ({args.expiry})...\n")

    ce_resp = search_instrument(client, args.query, exchanges="NSE", segments="FO",
                                instrument_types="CE", expiry=args.expiry, atm_offset=0, records=1)
    pe_resp = search_instrument(client, args.query, exchanges="NSE", segments="FO",
                                instrument_types="PE", expiry=args.expiry, atm_offset=0, records=1)

    ce_list = ce_resp.data or []
    pe_list = pe_resp.data or []

    if not ce_list or not pe_list:
        print("Could not find ATM options. Try different symbol or expiry.")
        sys.exit(1)

    ce = ce_list[0]
    pe = pe_list[0]
    strike = ce.get("strike_price", 0)
    lot_size = ce.get("lot_size", 1)
    expiry = ce.get("expiry", "")

    keys = [ce["instrument_key"], pe["instrument_key"]]
    ltp_data = get_ltp(client, *keys)

    ce_price = ltp_data[ce["instrument_key"]].last_price
    pe_price = ltp_data[pe["instrument_key"]].last_price

    straddle_cost = ce_price + pe_price
    upper_breakeven = strike + straddle_cost
    lower_breakeven = strike - straddle_cost
    max_loss = straddle_cost * lot_size

    print(f"{'Leg':<10} {'Symbol':<30} {'Strike':>10} {'LTP':>10}")
    print("-" * 65)
    print(f"{'Call':<10} {ce['trading_symbol']:<30} {strike:>10.2f} {ce_price:>10.2f}")
    print(f"{'Put':<10} {pe['trading_symbol']:<30} {strike:>10.2f} {pe_price:>10.2f}")
    print("-" * 65)

    print(f"\nExpiry            : {expiry}")
    print(f"Strike            : {strike:,.2f}")
    print(f"Total Straddle    : {straddle_cost:,.2f}  (CE {ce_price:.2f} + PE {pe_price:.2f})")
    print(f"Lot size          : {lot_size}")
    print(f"Total cost/lot    : ₹{max_loss:,.2f}")
    print()
    print(f"Upper breakeven   : {upper_breakeven:,.2f}  (+{straddle_cost:.2f} from strike)")
    print(f"Lower breakeven   : {lower_breakeven:,.2f}  (-{straddle_cost:.2f} from strike)")
    print(f"Max loss (at exp) : ₹{max_loss:,.2f} per lot  (if underlying stays at {strike:.0f})")
    print(f"Required move     : {(straddle_cost / strike * 100):.2f}% in either direction to break even")


if __name__ == "__main__":
    main()
