"""
Butterfly Spread Pricer.

A long call butterfly =
  Buy 1 lower-strike Call  (ATM - offset)
  Sell 2 middle-strike Calls  (ATM)
  Buy 1 upper-strike Call  (ATM + offset)

Net debit or credit depending on skew. Max profit at ATM strike at expiry.

  Max profit = wing_width - net_debit  (at middle strike)
  Max loss   = net_debit  (at or beyond outer strikes)
  Lower BE   = lower_strike + net_debit
  Upper BE   = upper_strike - net_debit

Usage:
  python options_strategies/butterfly_spread.py --token <TOKEN>
  python options_strategies/butterfly_spread.py --token <TOKEN> --query BANKNIFTY --wing 2
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import get_api_client, search_instrument, get_ltp


def fetch_ce(client, query, expiry, offset):
    resp = search_instrument(client, query, exchanges="NSE", segments="FO",
                             instrument_types="CE", expiry=expiry,
                             atm_offset=offset, records=1)
    opts = resp.data or []
    return opts[0] if opts else None


def main():
    parser = argparse.ArgumentParser(description="Butterfly spread pricer")
    parser.add_argument("--token", required=True, help="Upstox access token or analytics token")
    parser.add_argument("--query", default="NIFTY", help="Underlying symbol (default: NIFTY)")
    parser.add_argument("--expiry", default="current_month", help="Expiry (default: current_month)")
    parser.add_argument("--wing", type=int, default=1, help="Wing offset in strikes (default: 1)")
    args = parser.parse_args()

    client = get_api_client(args.token)

    print(f"Pricing butterfly spread for {args.query} ({args.expiry}), wing={args.wing}...\n")

    lower_leg  = fetch_ce(client, args.query, args.expiry, -args.wing)
    middle_leg = fetch_ce(client, args.query, args.expiry, 0)
    upper_leg  = fetch_ce(client, args.query, args.expiry, +args.wing)

    for name, leg in [("lower", lower_leg), ("middle", middle_leg), ("upper", upper_leg)]:
        if not leg:
            print(f"Could not find {name} leg. Try a smaller --wing value.")
            sys.exit(1)

    keys = [lower_leg["instrument_key"], middle_leg["instrument_key"], upper_leg["instrument_key"]]
    ltp_data = get_ltp(client, *keys)

    lower_prem  = ltp_data[lower_leg["instrument_key"]].last_price
    middle_prem = ltp_data[middle_leg["instrument_key"]].last_price
    upper_prem  = ltp_data[upper_leg["instrument_key"]].last_price

    lower_strike  = lower_leg.get("strike_price", 0)
    middle_strike = middle_leg.get("strike_price", 0)
    upper_strike  = upper_leg.get("strike_price", 0)
    lot_size = middle_leg.get("lot_size", 1)

    net_debit = lower_prem - 2 * middle_prem + upper_prem
    wing_width = upper_strike - middle_strike  # should equal middle_strike - lower_strike
    max_profit = wing_width - net_debit
    lower_be = lower_strike + net_debit
    upper_be = upper_strike - net_debit

    print(f"{'Action':<10} {'Qty':<5} {'Symbol':<30} {'Strike':>10} {'Premium':>10} {'Net':>10}")
    print("-" * 80)
    for action, qty, leg, prem in [
        ("BUY",  "+1", lower_leg,  lower_prem),
        ("SELL", "-2", middle_leg, middle_prem),
        ("BUY",  "+1", upper_leg,  upper_prem),
    ]:
        net = prem if "BUY" in action else -prem
        print(f"{action:<10} {qty:<5} {leg['trading_symbol']:<30} "
              f"{leg.get('strike_price',0):>10.2f} {prem:>10.2f} {net:>+10.2f}")
    print("-" * 80)

    label = "debit" if net_debit > 0 else "credit"
    print(f"\nNet {label}          : {abs(net_debit):>8.2f} per unit  "
          f"(₹{abs(net_debit) * lot_size:,.2f}/lot)")
    print(f"Wing width          : {wing_width:>8.2f} points")
    print(f"Max profit          : {max_profit:>8.2f} per unit  "
          f"(₹{max_profit * lot_size:,.2f}/lot)  at strike {middle_strike:,.0f}")
    print(f"Max loss            : {abs(net_debit):>8.2f} per unit  "
          f"(₹{abs(net_debit) * lot_size:,.2f}/lot)")
    print(f"\nLower breakeven     : {lower_be:,.2f}")
    print(f"Upper breakeven     : {upper_be:,.2f}")
    print(f"Profit zone         : {lower_be:,.0f} – {upper_be:,.0f}")


if __name__ == "__main__":
    main()
