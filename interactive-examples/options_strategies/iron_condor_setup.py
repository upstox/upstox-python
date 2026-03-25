"""
Iron Condor Setup.

An iron condor =
  Sell OTM Put  + Buy further-OTM Put  (put spread)
  Sell OTM Call + Buy further-OTM Call (call spread)

Net credit received upfront. Profit if underlying stays in range.

  Max profit = net credit (if underlying expires between short strikes)
  Max loss   = spread width - net credit  (if underlying breaches outer strikes)
  Upper breakeven = short call strike + net credit
  Lower breakeven = short put strike  - net credit

Usage:
  python options_strategies/iron_condor_setup.py --token <TOKEN>
  python options_strategies/iron_condor_setup.py --token <TOKEN> --query BANKNIFTY --short_offset 1 --long_offset 3
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import get_api_client, search_instrument, get_ltp


def fetch_leg(client, query, expiry, itype, offset, records=1):
    resp = search_instrument(client, query, exchanges="NSE", segments="FO",
                             instrument_types=itype, expiry=expiry,
                             atm_offset=offset, records=records)
    legs = resp.data or []
    return legs[0] if legs else None


def main():
    parser = argparse.ArgumentParser(description="Iron condor setup and net credit")
    parser.add_argument("--token", required=True, help="Upstox access token or analytics token")
    parser.add_argument("--query", default="NIFTY", help="Underlying symbol (default: NIFTY)")
    parser.add_argument("--expiry", default="current_month", help="Expiry (default: current_month)")
    parser.add_argument("--short_offset", type=int, default=1, help="Offset for short legs (default: 1)")
    parser.add_argument("--long_offset", type=int, default=3, help="Offset for long hedge legs (default: 3)")
    args = parser.parse_args()

    client = get_api_client(args.token)

    print(f"Building iron condor for {args.query} ({args.expiry})...\n")

    # 4 legs
    short_call = fetch_leg(client, args.query, args.expiry, "CE", +args.short_offset)
    long_call  = fetch_leg(client, args.query, args.expiry, "CE", +args.long_offset)
    short_put  = fetch_leg(client, args.query, args.expiry, "PE", -args.short_offset)
    long_put   = fetch_leg(client, args.query, args.expiry, "PE", -args.long_offset)

    legs = {"short_call": short_call, "long_call": long_call,
            "short_put": short_put, "long_put": long_put}

    missing = [k for k, v in legs.items() if v is None]
    if missing:
        print(f"Could not find legs: {missing}. Try different offsets.")
        sys.exit(1)

    all_keys = [l["instrument_key"] for l in legs.values()]
    ltp_data = get_ltp(client, *all_keys)

    def ltp(inst):
        return ltp_data[inst["instrument_key"]].last_price

    sc_prem = ltp(short_call)
    lc_prem = ltp(long_call)
    sp_prem = ltp(short_put)
    lp_prem = ltp(long_put)

    net_credit = sc_prem - lc_prem + sp_prem - lp_prem
    call_spread_width = long_call.get("strike_price", 0) - short_call.get("strike_price", 0)
    put_spread_width  = short_put.get("strike_price", 0) - long_put.get("strike_price", 0)
    max_loss = max(call_spread_width, put_spread_width) - net_credit
    lot_size = short_call.get("lot_size", 1)

    upper_be = short_call.get("strike_price", 0) + net_credit
    lower_be = short_put.get("strike_price", 0) - net_credit

    print(f"{'Action':<8} {'Type':<8} {'Symbol':<30} {'Strike':>10} {'Premium':>10}")
    print("-" * 75)
    for action, itype, inst, prem in [
        ("SELL", "CALL", short_call, sc_prem),
        ("BUY",  "CALL", long_call,  lc_prem),
        ("SELL", "PUT",  short_put,  sp_prem),
        ("BUY",  "PUT",  long_put,   lp_prem),
    ]:
        print(f"{action:<8} {itype:<8} {inst['trading_symbol']:<30} "
              f"{inst.get('strike_price',0):>10.2f} {prem:>10.2f}")
    print("-" * 75)

    print(f"\nNet credit         : {net_credit:>8.2f}  per unit  (₹{net_credit * lot_size:,.2f}/lot)")
    print(f"Call spread width  : {call_spread_width:>8.2f} points")
    print(f"Put spread width   : {put_spread_width:>8.2f} points")
    print(f"Max profit         : {net_credit:>8.2f}  per unit  (₹{net_credit * lot_size:,.2f}/lot)")
    print(f"Max loss           : {max_loss:>8.2f}  per unit  (₹{max_loss * lot_size:,.2f}/lot)")
    print()
    print(f"Upper breakeven    : {upper_be:,.2f}")
    print(f"Lower breakeven    : {lower_be:,.2f}")
    print(f"Profit range       : {lower_be:,.0f} – {upper_be:,.0f}  ({upper_be - lower_be:.0f} points wide)")


if __name__ == "__main__":
    main()
