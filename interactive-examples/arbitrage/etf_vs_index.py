"""
ETF vs Index NAV Arbitrage.

Compares the Nifty BeES (or BankBees) ETF market price against the
underlying index value to detect a premium or discount.

ETF Premium  = ETF price > implied NAV → ETF is expensive, potential to sell ETF / buy basket.
ETF Discount = ETF price < implied NAV → ETF is cheap, potential to buy ETF / short basket.

Implied NAV = Index LTP / ETF divisor
  (Nifty BeES NAV ≈ Nifty Index / 100 at inception; the exact ratio drifts over time)

This script fetches both the ETF price and the index LTP and reports the premium/discount.

Usage:
  python arbitrage/etf_vs_index.py --token <TOKEN>
  python arbitrage/etf_vs_index.py --token <TOKEN> --etf BANKBEES --index BANKNIFTY
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import get_api_client, search_instrument, get_ltp


def find_instrument(client, query, exchanges, segments, instrument_types=None):
    kwargs = dict(exchanges=exchanges, segments=segments, records=5)
    if instrument_types:
        kwargs["instrument_types"] = instrument_types
    resp = search_instrument(client, query, **kwargs)
    data = resp.data or []
    return data[0] if data else None


def main():
    parser = argparse.ArgumentParser(description="ETF vs index NAV premium/discount")
    parser.add_argument("--token", required=True, help="Upstox access token or analytics token")
    parser.add_argument("--etf", default="NIFTYBEES", help="ETF symbol on NSE (default: NIFTYBEES)")
    parser.add_argument("--index", default="NIFTY 50", help="Underlying index (default: NIFTY 50)")
    parser.add_argument(
        "--divisor", type=float, default=100.0,
        help="ETF units per index point (default: 100 for NiftyBees)"
    )
    args = parser.parse_args()

    client = get_api_client(args.token)

    print(f"Fetching {args.etf} ETF vs {args.index} index...\n")

    etf_inst = find_instrument(client, args.etf, "NSE", "EQ")
    index_inst = find_instrument(client, args.index, "NSE", "INDEX", "INDEX")

    if not etf_inst:
        print(f"ETF '{args.etf}' not found on NSE.")
        sys.exit(1)
    if not index_inst:
        print(f"Index '{args.index}' not found.")
        sys.exit(1)

    etf_key = etf_inst["instrument_key"]
    index_key = index_inst["instrument_key"]

    ltp_data = get_ltp(client, etf_key, index_key)

    etf_price = ltp_data[etf_key].last_price
    index_price = ltp_data[index_key].last_price

    implied_nav = index_price / args.divisor
    premium = etf_price - implied_nav
    premium_pct = (premium / implied_nav * 100) if implied_nav else 0

    print(f"{'Instrument':<25} {'LTP':>12}")
    print("-" * 40)
    print(f"{index_inst.get('trading_symbol','Index'):<25} {index_price:>12.2f}")
    print(f"{etf_inst.get('trading_symbol','ETF'):<25} {etf_price:>12.2f}")
    print(f"{'Implied NAV (index/divisor)':<25} {implied_nav:>12.2f}")
    print("-" * 40)

    print(f"\nDivisor used       : {args.divisor}")
    print(f"ETF Premium/Disc.  : {premium:>+8.4f}  ({premium_pct:+.4f}%)")

    if abs(premium_pct) < 0.1:
        print("ETF trades near NAV — no significant premium or discount.")
    elif premium > 0:
        print(f"\nETF at {premium_pct:.3f}% PREMIUM to NAV.")
        print("Arbitrage: Buy index basket (or futures), Sell ETF.")
    else:
        print(f"\nETF at {abs(premium_pct):.3f}% DISCOUNT to NAV.")
        print("Arbitrage: Buy ETF, Sell index basket (or futures).")


if __name__ == "__main__":
    main()
