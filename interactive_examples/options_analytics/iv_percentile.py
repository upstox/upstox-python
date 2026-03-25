"""
IV Percentile & IV Rank — where current implied volatility stands vs history.

Fetches 1-year daily close history to compute rolling historical volatility (HV),
then fetches the current ATM IV from the option chain.  Two metrics are reported:

  IV Percentile = % of trading days in the past year when HV was LOWER than current ATM IV
  IV Rank       = (current IV - min IV) / (max IV - min IV) × 100

High IV Percentile (>80%) → options are expensive → favour selling strategies
Low  IV Percentile (<20%) → options are cheap   → favour buying strategies

Usage:
  python options_analytics/iv_percentile.py --token <TOKEN>
  python options_analytics/iv_percentile.py --token <TOKEN> --query BANKNIFTY --days 252
"""

import argparse
import sys
import os
import math
from statistics import stdev
from datetime import date, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import get_api_client, search_instrument, get_historical_candles
import upstox_client

BOLD  = "\033[1m"
GREEN = "\033[32m"
RED   = "\033[31m"
CYAN  = "\033[36m"
RESET = "\033[0m"

INDEX_KEYS = {
    "NIFTY":      "NSE_INDEX|Nifty 50",
    "BANKNIFTY":  "NSE_INDEX|Nifty Bank",
    "FINNIFTY":   "NSE_INDEX|Nifty Fin Service",
    "MIDCPNIFTY": "NSE_INDEX|NIFTY MID SELECT",
    "SENSEX":     "BSE_INDEX|SENSEX",
}


def get_instrument_key(client, query: str) -> str:
    upper = query.upper()
    if upper in INDEX_KEYS:
        return INDEX_KEYS[upper]
    resp = search_instrument(client, query, exchanges="NSE", segments="INDEX", records=1)
    hits = resp.data or []
    if hits:
        return hits[0]["instrument_key"]
    resp = search_instrument(client, query, exchanges="NSE", segments="EQ", records=1)
    hits = resp.data or []
    if hits:
        return hits[0]["instrument_key"]
    print(f"Cannot resolve instrument for '{query}'.")
    sys.exit(1)


def get_nearest_expiry(client, query: str) -> str:
    resp = search_instrument(client, query, exchanges="NSE", segments="FO",
                             instrument_types="CE", expiry="current_month", records=1)
    hits = resp.data or []
    return hits[0].get("expiry", "") if hits else ""


def extract(obj, *keys, default=0):
    for key in keys:
        if obj is None:
            return default
        obj = obj.get(key) if isinstance(obj, dict) else getattr(obj, key, None)
    return obj if obj is not None else default


def rolling_hv(closes, window=20):
    """Compute annualised historical volatility for each rolling window."""
    hvs = []
    for i in range(window, len(closes)):
        seg = closes[i - window:i + 1]
        log_rets = [math.log(seg[j] / seg[j - 1]) for j in range(1, len(seg))]
        if len(log_rets) >= 2:
            hvs.append(stdev(log_rets) * math.sqrt(252) * 100)
    return hvs


def main():
    parser = argparse.ArgumentParser(description="IV Percentile & IV Rank")
    parser.add_argument("--token",  required=True, help="Upstox access or analytics token")
    parser.add_argument("--query",  default="NIFTY", help="Underlying (default: NIFTY)")
    parser.add_argument("--days",   type=int, default=252, help="Lookback trading days (default: 252)")
    parser.add_argument("--window", type=int, default=20, help="HV rolling window (default: 20)")
    args = parser.parse_args()

    client = get_api_client(args.token)

    print(f"\nComputing IV Percentile for {args.query.upper()}...\n")

    instrument_key = get_instrument_key(client, args.query)

    # Fetch historical daily closes
    to_date = date.today().isoformat()
    from_date = (date.today() - timedelta(days=int(args.days * 1.6))).isoformat()

    candles = get_historical_candles(client, instrument_key, "days", 1, to_date, from_date)
    if not candles:
        print("No historical candle data returned.")
        sys.exit(1)

    candles = list(reversed(candles))
    closes = [float(c[4]) for c in candles if len(c) > 4]

    if len(closes) < args.window + 10:
        print(f"Insufficient data: {len(closes)} closes, need at least {args.window + 10}.")
        sys.exit(1)

    # Compute rolling HV distribution
    hv_values = rolling_hv(closes, args.window)
    if not hv_values:
        print("Could not compute historical volatility.")
        sys.exit(1)

    # Fetch current ATM IV from option chain
    underlying_key = INDEX_KEYS.get(args.query.upper(), instrument_key)
    expiry = get_nearest_expiry(client, args.query)
    if not expiry:
        print("Could not determine expiry for ATM IV lookup.")
        sys.exit(1)

    api = upstox_client.OptionsApi(client)
    resp = api.get_put_call_option_chain(underlying_key, expiry)
    chain = resp.data if resp.data else []
    if not isinstance(chain, list):
        chain = [chain]

    # Find ATM strike and its IV
    spot = closes[-1]
    atm_entry = None
    min_diff = float("inf")
    for entry in chain:
        strike = extract(entry, "strike_price")
        if strike and abs(strike - spot) < min_diff:
            min_diff = abs(strike - spot)
            atm_entry = entry

    if not atm_entry:
        print("Could not find ATM strike in option chain.")
        sys.exit(1)

    ce_iv = extract(atm_entry, "call_options", "option_greeks", "iv")
    pe_iv = extract(atm_entry, "put_options", "option_greeks", "iv")
    atm_iv = ((ce_iv or 0) + (pe_iv or 0)) / 2 * 100  # as percentage
    atm_strike = extract(atm_entry, "strike_price")

    if atm_iv <= 0:
        print("ATM IV is zero or unavailable.")
        sys.exit(1)

    # Compute percentile and rank
    hv_min = min(hv_values)
    hv_max = max(hv_values)
    days_below = sum(1 for hv in hv_values if hv < atm_iv)
    iv_percentile = days_below / len(hv_values) * 100
    iv_rank = (atm_iv - hv_min) / (hv_max - hv_min) * 100 if hv_max > hv_min else 50

    # Display
    print(f"  Underlying     : {args.query.upper()}")
    print(f"  Spot price     : {spot:,.2f}")
    print(f"  ATM strike     : {atm_strike:,.0f}")
    print(f"  Expiry         : {expiry}")
    print(f"  ATM IV (avg)   : {BOLD}{atm_iv:.1f}%{RESET}")
    print()
    print(f"  HV distribution ({args.window}-day rolling, {len(hv_values)} samples):")
    print(f"    Min HV       : {hv_min:.1f}%")
    print(f"    Max HV       : {hv_max:.1f}%")
    print(f"    Current HV   : {hv_values[-1]:.1f}%")
    print()
    print(f"  {BOLD}IV Percentile  : {iv_percentile:.0f}%{RESET}")
    print(f"  {BOLD}IV Rank        : {iv_rank:.0f}%{RESET}")
    print()

    if iv_percentile > 80:
        print(f"  {RED}IV is HIGH{RESET} — options are expensive relative to history.")
        print(f"  Consider: short straddles, iron condors, credit spreads.")
    elif iv_percentile < 20:
        print(f"  {GREEN}IV is LOW{RESET} — options are cheap relative to history.")
        print(f"  Consider: long straddles, long strangles, debit spreads.")
    else:
        print(f"  {CYAN}IV is NORMAL{RESET} — no extreme relative to history.")
    print()


if __name__ == "__main__":
    main()
