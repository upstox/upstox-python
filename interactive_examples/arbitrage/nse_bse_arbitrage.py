"""
NSE vs BSE Cash Equity Arbitrage Scanner.

Searches for the same stock on both NSE and BSE, fetches live LTPs,
and prints the price discrepancy.

In practice, NSE-BSE spreads are very tight (milliseconds to arbitrage).
A persistent spread may indicate illiquidity or trading halt on one exchange.

Usage:
  python arbitrage/nse_bse_arbitrage.py --token <TOKEN> --query RELIANCE
  python arbitrage/nse_bse_arbitrage.py --token <TOKEN> --query INFY
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import get_api_client, search_instrument, get_ltp


def find_equity(client, query, exchange):
    """Find the first equity instrument on a given exchange."""
    resp = search_instrument(
        client, query,
        exchanges=exchange,
        segments="EQ",
        records=5,
    )
    instruments = resp.data or []
    # Prefer exact symbol match
    for inst in instruments:
        sym = inst.get("trading_symbol", "")
        if query.upper() == sym.upper() or query.upper() == sym.upper().split("-")[0]:
            return inst
    return instruments[0] if instruments else None


def main():
    parser = argparse.ArgumentParser(description="NSE vs BSE price arbitrage scanner")
    parser.add_argument("--token", required=True, help="Upstox access token or analytics token")
    parser.add_argument("--query", default="RELIANCE", help="Stock symbol (default: RELIANCE)")
    args = parser.parse_args()

    client = get_api_client(args.token)

    print(f"Scanning NSE vs BSE price for '{args.query}'...\n")

    nse_inst = find_equity(client, args.query, "NSE")
    bse_inst = find_equity(client, args.query, "BSE")

    if not nse_inst:
        print(f"'{args.query}' not found on NSE.")
        sys.exit(1)
    if not bse_inst:
        print(f"'{args.query}' not found on BSE.")
        sys.exit(1)

    nse_key = nse_inst["instrument_key"]
    bse_key = bse_inst["instrument_key"]

    ltp_data = get_ltp(client, nse_key, bse_key)

    nse_ltp = ltp_data[nse_key].last_price
    bse_ltp = ltp_data[bse_key].last_price
    nse_vol = ltp_data[nse_key].volume
    bse_vol = ltp_data[bse_key].volume

    spread = nse_ltp - bse_ltp
    spread_pct = (spread / bse_ltp * 100) if bse_ltp else 0

    print(f"{'Exchange':<10} {'Symbol':<20} {'LTP':>10} {'Volume':>15}")
    print("-" * 60)
    print(f"{'NSE':<10} {nse_inst.get('trading_symbol',''):<20} {nse_ltp:>10.2f} {nse_vol:>15,}")
    print(f"{'BSE':<10} {bse_inst.get('trading_symbol',''):<20} {bse_ltp:>10.2f} {bse_vol:>15,}")
    print("-" * 60)

    print(f"\nSpread (NSE - BSE) : {spread:>+8.2f}  ({spread_pct:+.4f}%)")

    if abs(spread) < 0.05:
        print("Prices are at parity — no arbitrage opportunity.")
    elif spread > 0:
        print(f"\nNSE trades at a premium of ₹{spread:.2f}.")
        print("Theoretical arbitrage: Buy on BSE, Sell on NSE.")
        print("(Ensure transaction costs < spread before trading)")
    else:
        print(f"\nBSE trades at a premium of ₹{abs(spread):.2f}.")
        print("Theoretical arbitrage: Buy on NSE, Sell on BSE.")

    lot_size = nse_inst.get("lot_size", 1)
    print(f"\nLot size / board lot : {lot_size}")
    print(f"Spread per lot (₹)   : {spread * lot_size:>+.2f}")


if __name__ == "__main__":
    main()
