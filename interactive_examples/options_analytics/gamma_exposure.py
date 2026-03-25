"""
Dealer Gamma Exposure (GEX) Estimator.

GEX estimates how much market makers need to hedge as the underlying moves.
When GEX is positive (net long gamma), market makers are short options and
buy dips / sell rallies (dampening effect on volatility).
When GEX flips negative, market makers are long options and may amplify moves.

GEX at each strike K (simplified):
  GEX(K) = (CE_OI(K) - PE_OI(K)) * lot_size * spot * gamma

Since we don't have actual gamma from Upstox (no greeks in full quote),
this script uses a proxy: (CE_OI - PE_OI) * lot_size weighted by moneyness.
A more accurate version would use Black-Scholes gamma.

Usage:
  python options_analytics/gamma_exposure.py --token <TOKEN>
  python options_analytics/gamma_exposure.py --token <TOKEN> --query BANKNIFTY
"""

import argparse
import sys
import os
import math

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import get_api_client, search_instrument, get_full_quote, get_ltp


def fetch_options(client, query, expiry, itype, num_strikes):
    instruments = []
    for offset in range(-num_strikes, num_strikes + 1):
        resp = search_instrument(client, query, exchanges="NSE", segments="FO",
                                 instrument_types=itype, expiry=expiry,
                                 atm_offset=offset, records=1)
        data = resp.data or []
        if data:
            instruments.append(data[0])
    seen = set()
    unique = []
    for inst in instruments:
        k = inst.get("strike_price", 0)
        if k not in seen:
            seen.add(k)
            unique.append(inst)
    return unique


def bs_gamma_approx(spot, strike, dte_days, iv_approx=0.15):
    """Rough Black-Scholes gamma approximation for weighting."""
    t = max(dte_days / 365, 0.001)
    d1 = (math.log(spot / strike) + 0.5 * iv_approx ** 2 * t) / (iv_approx * math.sqrt(t))
    phi = math.exp(-0.5 * d1 ** 2) / math.sqrt(2 * math.pi)
    return phi / (spot * iv_approx * math.sqrt(t))


def main():
    parser = argparse.ArgumentParser(description="Dealer gamma exposure estimator")
    parser.add_argument("--token", required=True, help="Upstox access token or analytics token")
    parser.add_argument("--query", default="NIFTY", help="Underlying symbol (default: NIFTY)")
    parser.add_argument("--expiry", default="current_month", help="Expiry (default: current_month)")
    parser.add_argument("--strikes", type=int, default=8, help="Strikes each side of ATM (default: 8)")
    parser.add_argument("--dte", type=int, default=15, help="Days to expiry estimate (default: 15)")
    args = parser.parse_args()

    client = get_api_client(args.token)

    print(f"Estimating GEX for {args.query} ({args.expiry})...\n")

    ce_insts = fetch_options(client, args.query, args.expiry, "CE", args.strikes)
    pe_insts = fetch_options(client, args.query, args.expiry, "PE", args.strikes)

    all_keys = [i["instrument_key"] for i in ce_insts + pe_insts]
    quote_data = get_full_quote(client, *all_keys)

    ce_data = {}
    pe_data = {}
    lot_size = 50  # default NIFTY lot size

    for inst in ce_insts:
        k = inst.get("strike_price", 0)
        q = quote_data.get(inst["instrument_key"])
        ce_data[k] = {"oi": q.oi if q else 0, "ltp": q.last_price if q else 0}
        if inst.get("lot_size"):
            lot_size = inst["lot_size"]

    for inst in pe_insts:
        k = inst.get("strike_price", 0)
        q = quote_data.get(inst["instrument_key"])
        pe_data[k] = {"oi": q.oi if q else 0, "ltp": q.last_price if q else 0}

    # Get ATM spot
    atm_resp = search_instrument(client, args.query, exchanges="NSE", segments="FO",
                                 instrument_types="CE", expiry=args.expiry, atm_offset=0, records=1)
    atm_strike = (atm_resp.data or [{}])[0].get("strike_price", 0)

    all_strikes = sorted(set(list(ce_data.keys()) + list(pe_data.keys())))

    gex_by_strike = {}
    for strike in all_strikes:
        ce_oi = ce_data.get(strike, {}).get("oi", 0) or 0
        pe_oi = pe_data.get(strike, {}).get("oi", 0) or 0
        gamma = bs_gamma_approx(atm_strike, strike, args.dte)
        gex = (ce_oi - pe_oi) * lot_size * atm_strike * gamma
        gex_by_strike[strike] = gex

    total_gex = sum(gex_by_strike.values())
    max_abs = max(abs(v) for v in gex_by_strike.values()) or 1

    print(f"{'Strike':>10}  {'CE OI':>10}  {'PE OI':>10}  {'GEX':>14}  {'Bar':}")
    print("-" * 75)
    for strike in reversed(all_strikes):
        ce_oi = ce_data.get(strike, {}).get("oi", 0) or 0
        pe_oi = pe_data.get(strike, {}).get("oi", 0) or 0
        gex = gex_by_strike[strike]
        bar_len = int(abs(gex) / max_abs * 20)
        bar = ("+" if gex >= 0 else "-") * bar_len
        marker = " <<< ATM" if strike == atm_strike else ""
        print(f"{strike:>10.0f}  {ce_oi:>10,.0f}  {pe_oi:>10,.0f}  {gex:>14,.0f}  {bar}{marker}")

    print(f"\nTotal GEX         : {total_gex:,.0f}")
    print(f"ATM strike        : {atm_strike:,.0f}")
    if total_gex > 0:
        print("Positive GEX: Dealers short options → buy dips, sell rallies (stabilising).")
    else:
        print("Negative GEX: Dealers long options → may amplify directional moves.")


if __name__ == "__main__":
    main()
