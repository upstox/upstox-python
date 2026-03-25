"""
Bull Call Spread Pricer.

A bull call spread = Buy lower-strike Call + Sell higher-strike Call (same expiry).
Limited profit, limited risk. Suitable when moderately bullish.

  Max profit = (high_strike - low_strike) - net_debit
  Max loss   = net_debit (paid upfront)
  Breakeven  = low_strike + net_debit

Usage:
  python options_strategies/bull_call_spread.py --token <TOKEN>
  python options_strategies/bull_call_spread.py --token <TOKEN> --query BANKNIFTY --buy_offset 0 --sell_offset 2
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import get_api_client, search_instrument, get_ltp


def main():
    parser = argparse.ArgumentParser(description="Bull call spread pricer")
    parser.add_argument("--token", required=True, help="Upstox access token or analytics token")
    parser.add_argument("--query", default="NIFTY", help="Underlying symbol (default: NIFTY)")
    parser.add_argument("--expiry", default="current_month", help="Expiry (default: current_month)")
    parser.add_argument("--buy_offset", type=int, default=0, help="ATM offset for the leg to BUY (default: 0=ATM)")
    parser.add_argument("--sell_offset", type=int, default=2, help="ATM offset for the leg to SELL (default: 2=2 strikes OTM)")
    args = parser.parse_args()

    client = get_api_client(args.token)

    print(f"Pricing bull call spread for {args.query} ({args.expiry})...\n")

    buy_resp = search_instrument(client, args.query, exchanges="NSE", segments="FO",
                                 instrument_types="CE", expiry=args.expiry,
                                 atm_offset=args.buy_offset, records=1)
    sell_resp = search_instrument(client, args.query, exchanges="NSE", segments="FO",
                                  instrument_types="CE", expiry=args.expiry,
                                  atm_offset=args.sell_offset, records=1)

    buy_list = buy_resp.data or []
    sell_list = sell_resp.data or []

    if not buy_list or not sell_list:
        print("Could not find both legs. Try different offsets.")
        sys.exit(1)

    buy_leg = buy_list[0]
    sell_leg = sell_list[0]

    keys = [buy_leg["instrument_key"], sell_leg["instrument_key"]]
    ltp_data = get_ltp(client, *keys)

    buy_premium = ltp_data[buy_leg["instrument_key"]].last_price
    sell_premium = ltp_data[sell_leg["instrument_key"]].last_price

    buy_strike = buy_leg.get("strike_price", 0)
    sell_strike = sell_leg.get("strike_price", 0)
    lot_size = buy_leg.get("lot_size", 1)

    net_debit = buy_premium - sell_premium
    spread_width = sell_strike - buy_strike
    max_profit = spread_width - net_debit
    breakeven = buy_strike + net_debit
    risk_reward = max_profit / net_debit if net_debit > 0 else 0

    print(f"{'Action':<8} {'Symbol':<30} {'Strike':>10} {'Premium':>10}")
    print("-" * 65)
    print(f"{'BUY':<8} {buy_leg['trading_symbol']:<30} {buy_strike:>10.2f} {buy_premium:>10.2f}")
    print(f"{'SELL':<8} {sell_leg['trading_symbol']:<30} {sell_strike:>10.2f} {sell_premium:>10.2f}")
    print("-" * 65)

    print(f"\nNet debit (cost)   : {net_debit:>8.2f}  per unit")
    print(f"Net debit per lot  : ₹{net_debit * lot_size:>10,.2f}")
    print(f"Spread width       : {spread_width:>8.2f} points")
    print()
    print(f"Breakeven          : {breakeven:,.2f}")
    print(f"Max profit         : {max_profit:>8.2f}  per unit  (₹{max_profit * lot_size:,.2f}/lot)")
    print(f"Max loss           : {net_debit:>8.2f}  per unit  (₹{net_debit * lot_size:,.2f}/lot)")
    print(f"Risk/Reward        : 1 : {risk_reward:.2f}")

    print(f"\nBullish above {breakeven:,.0f}. Full profit if {args.query} closes above {sell_strike:,.0f} at expiry.")


if __name__ == "__main__":
    main()
