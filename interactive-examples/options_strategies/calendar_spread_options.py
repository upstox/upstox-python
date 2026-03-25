"""
Options Calendar Spread.

A calendar spread = Sell near-month option + Buy far-month option (same strike).
Profits from time decay: near-month decays faster than far-month.

Net debit = far_month_premium - near_month_premium.

Usage:
  python options_strategies/calendar_spread_options.py --token <TOKEN>
  python options_strategies/calendar_spread_options.py --token <TOKEN> --query BANKNIFTY --type PE
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import get_api_client, search_instrument, get_ltp


def find_atm_option(client, query, expiry, itype):
    resp = search_instrument(client, query, exchanges="NSE", segments="FO",
                             instrument_types=itype, expiry=expiry,
                             atm_offset=0, records=1)
    opts = resp.data or []
    return opts[0] if opts else None


def main():
    parser = argparse.ArgumentParser(description="Options calendar spread — same strike, two expiries")
    parser.add_argument("--token", required=True, help="Upstox access token or analytics token")
    parser.add_argument("--query", default="NIFTY", help="Underlying symbol (default: NIFTY)")
    parser.add_argument("--type", dest="opt_type", default="CE", choices=["CE", "PE"],
                        help="Option type (default: CE)")
    args = parser.parse_args()

    client = get_api_client(args.token)

    print(f"Building {args.opt_type} calendar spread for {args.query} (near vs far month)...\n")

    near_opt = find_atm_option(client, args.query, "current_month", args.opt_type)
    far_opt  = find_atm_option(client, args.query, "next_month",    args.opt_type)

    if not near_opt or not far_opt:
        print("Could not find both legs.")
        sys.exit(1)

    keys = [near_opt["instrument_key"], far_opt["instrument_key"]]
    ltp_data = get_ltp(client, *keys)

    near_prem = ltp_data[near_opt["instrument_key"]].last_price
    far_prem  = ltp_data[far_opt["instrument_key"]].last_price

    net_debit = far_prem - near_prem
    lot_size  = near_opt.get("lot_size", 1)

    print(f"{'Action':<8} {'Symbol':<30} {'Strike':>10} {'Expiry':<14} {'Premium':>10}")
    print("-" * 77)
    near_expiry = near_opt.get("expiry", "")
    far_expiry  = far_opt.get("expiry", "")

    print(f"{'SELL':<8} {near_opt['trading_symbol']:<30} "
          f"{near_opt.get('strike_price',0):>10.2f} {near_expiry:<14} {near_prem:>10.2f}")
    print(f"{'BUY':<8} {far_opt['trading_symbol']:<30}  "
          f"{far_opt.get('strike_price',0):>10.2f} {far_expiry:<14} {far_prem:>10.2f}")
    print("-" * 77)

    print(f"\nNet debit              : {net_debit:>8.2f}  per unit")
    print(f"Net debit per lot      : ₹{net_debit * lot_size:,.2f}")
    print(f"\nProfit mechanism       : Near-month ({near_expiry}) decays faster.")
    print(f"Ideal outcome          : Near option expires worthless; far option retains value.")
    print(f"Risk                   : Large underlying move hurts both legs equally.")

    if net_debit < 0:
        print(f"\nNote: net credit of {abs(net_debit):.2f} received — unusual, check liquidity.")


if __name__ == "__main__":
    main()
