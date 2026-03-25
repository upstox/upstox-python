"""
Put-Call Parity Check.

Put-call parity: C - P = F - K * e^(-rT)

In practice, for Indian index options (European style):
  C - P ≈ F - K  (ignoring discounting for short T)

Where:
  C = Call premium
  P = Put premium
  F = Futures price (near-month)
  K = Strike price

A deviation signals a mispricing or arbitrage opportunity.

Synthetic long = Buy CE + Sell PE → should equal (F - K).
Synthetic short = Sell CE + Buy PE → reverse.

Usage:
  python options_strategies/put_call_parity.py --token <TOKEN>
  python options_strategies/put_call_parity.py --token <TOKEN> --query BANKNIFTY --strike 48000
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import get_api_client, search_instrument, get_futures_sorted, get_ltp


def get_atm_options(client, query: str, atm_offset: int = 0):
    """Fetch CE and PE at a given ATM offset for current month expiry."""
    ce_resp = search_instrument(
        client, query,
        exchanges="NSE", segments="FO",
        instrument_types="CE",
        expiry="current_month",
        atm_offset=atm_offset,
        records=1,
    )
    pe_resp = search_instrument(
        client, query,
        exchanges="NSE", segments="FO",
        instrument_types="PE",
        expiry="current_month",
        atm_offset=atm_offset,
        records=1,
    )
    ce_list = ce_resp.data or []
    pe_list = pe_resp.data or []
    return ce_list[0] if ce_list else None, pe_list[0] if pe_list else None


def main():
    parser = argparse.ArgumentParser(description="Put-call parity deviation checker")
    parser.add_argument("--token", required=True, help="Upstox access token or analytics token")
    parser.add_argument("--query", default="NIFTY", help="Underlying symbol (default: NIFTY)")
    parser.add_argument("--atm_offset", type=int, default=0, help="ATM offset (default: 0 = ATM)")
    args = parser.parse_args()

    client = get_api_client(args.token)

    print(f"Checking put-call parity for {args.query} (ATM offset: {args.atm_offset:+d})...\n")

    ce_inst, pe_inst = get_atm_options(client, args.query, args.atm_offset)
    if not ce_inst or not pe_inst:
        print("Could not find CE/PE pair. Try a different query or offset.")
        sys.exit(1)

    if ce_inst.get("strike_price") != pe_inst.get("strike_price"):
        print(f"Warning: CE strike {ce_inst.get('strike_price')} != PE strike {pe_inst.get('strike_price')}")

    strike = ce_inst.get("strike_price", 0)

    # Get near-month futures
    futures = get_futures_sorted(client, args.query, exchange="NSE")
    if not futures:
        print("Could not find futures contract.")
        sys.exit(1)
    near_fut = futures[0]

    keys = [ce_inst["instrument_key"], pe_inst["instrument_key"], near_fut["instrument_key"]]
    ltp_data = get_ltp(client, *keys)

    ce_price = ltp_data[ce_inst["instrument_key"]].last_price
    pe_price = ltp_data[pe_inst["instrument_key"]].last_price
    futures_price = ltp_data[near_fut["instrument_key"]].last_price

    synthetic = ce_price - pe_price          # C - P
    theoretical = futures_price - strike     # F - K
    deviation = synthetic - theoretical

    print(f"Strike          : {strike:,.2f}")
    print(f"Futures ({near_fut['trading_symbol']}) : {futures_price:,.2f}")
    print()
    print(f"Call ({ce_inst['trading_symbol']})  : {ce_price:,.2f}")
    print(f"Put  ({pe_inst['trading_symbol']})  : {pe_price:,.2f}")
    print()
    print(f"Synthetic (C - P)        : {synthetic:>+10.2f}")
    print(f"Theoretical (F - K)      : {theoretical:>+10.2f}")
    print(f"Parity Deviation         : {deviation:>+10.2f}")

    lot_size = near_fut.get("lot_size", 1)
    print(f"Deviation per lot (₹)    : {deviation * lot_size:>+10.2f}")

    if abs(deviation) < 5:
        print("\nParity holds within ₹5 — no significant mispricing.")
    elif deviation > 0:
        print(f"\nCall is relatively EXPENSIVE vs Put + Futures by {deviation:.2f} points.")
        print("Potential trade: Sell CE, Buy PE, Buy Futures (reverse conversion).")
    else:
        print(f"\nPut is relatively EXPENSIVE vs Call + Futures by {abs(deviation):.2f} points.")
        print("Potential trade: Buy CE, Sell PE, Sell Futures (conversion).")


if __name__ == "__main__":
    main()
