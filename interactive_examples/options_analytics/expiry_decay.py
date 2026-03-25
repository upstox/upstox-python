"""
Expiry Day Premium Decay Tracker — visualise theta decay near expiry.

Fetches ATM ± N CE and PE premiums for the current/nearest weekly expiry and
shows the premium as a percentage of the underlying spot price.  Near expiry,
ATM options lose value rapidly (theta acceleration) — this script helps
quantify how much premium remains.

Usage:
  python options_analytics/expiry_decay.py --token <TOKEN>
  python options_analytics/expiry_decay.py --token <TOKEN> --query BANKNIFTY --strikes 4
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import get_api_client, search_instrument, get_ltp

BOLD  = "\033[1m"
GREEN = "\033[32m"
RED   = "\033[31m"
CYAN  = "\033[36m"
DIM   = "\033[2m"
RESET = "\033[0m"

INDEX_LTP_KEYS = {
    "NIFTY":      "NSE_INDEX|Nifty 50",
    "BANKNIFTY":  "NSE_INDEX|Nifty Bank",
    "FINNIFTY":   "NSE_INDEX|Nifty Fin Service",
    "MIDCPNIFTY": "NSE_INDEX|NIFTY MID SELECT",
    "SENSEX":     "BSE_INDEX|SENSEX",
}


def main():
    parser = argparse.ArgumentParser(description="Expiry premium decay tracker")
    parser.add_argument("--token",   required=True, help="Upstox access or analytics token")
    parser.add_argument("--query",   default="NIFTY", help="Underlying (default: NIFTY)")
    parser.add_argument("--expiry",  default="current_week",
                        help="Expiry filter (default: current_week)")
    parser.add_argument("--strikes", type=int, default=3,
                        help="Strikes each side of ATM (default: 3)")
    args = parser.parse_args()

    client = get_api_client(args.token)
    query_upper = args.query.upper()

    print(f"\nFetching expiry premiums for {query_upper} ({args.expiry}), "
          f"ATM ± {args.strikes}...\n")

    # Get spot price
    spot_key = INDEX_LTP_KEYS.get(query_upper)
    spot = 0
    if spot_key:
        ltp_data = get_ltp(client, spot_key)
        entry = ltp_data.get(spot_key, {})
        spot = entry.get("last_price") if isinstance(entry, dict) else getattr(entry, "last_price", 0)

    if not spot:
        resp = search_instrument(client, args.query, exchanges="NSE", segments="EQ", records=1)
        hits = resp.data or []
        if hits:
            eq_key = hits[0]["instrument_key"]
            ltp_data = get_ltp(client, eq_key)
            entry = ltp_data.get(eq_key, {})
            spot = entry.get("last_price") if isinstance(entry, dict) else getattr(entry, "last_price", 0)

    if not spot:
        print("Could not fetch spot price.")
        sys.exit(1)

    # Fetch CE and PE instruments across ATM ± N
    ce_instruments = []
    pe_instruments = []
    for offset in range(-args.strikes, args.strikes + 1):
        for itype, dest in [("CE", ce_instruments), ("PE", pe_instruments)]:
            resp = search_instrument(client, args.query, exchanges="NSE", segments="FO",
                                     instrument_types=itype, expiry=args.expiry,
                                     atm_offset=offset, records=1)
            hits = resp.data or []
            if hits:
                dest.append(hits[0])

    if not ce_instruments and not pe_instruments:
        print("No options found. Try a different --expiry.")
        sys.exit(1)

    # Deduplicate by strike
    def dedup(instruments):
        seen = set()
        result = []
        for inst in instruments:
            s = inst.get("strike_price", 0)
            if s not in seen:
                seen.add(s)
                result.append(inst)
        return sorted(result, key=lambda x: x.get("strike_price", 0))

    ce_instruments = dedup(ce_instruments)
    pe_instruments = dedup(pe_instruments)

    # Fetch LTPs
    all_keys = [i["instrument_key"] for i in ce_instruments + pe_instruments]
    ltp_data = get_ltp(client, *all_keys) if all_keys else {}

    def get_price(key):
        entry = ltp_data.get(key, {})
        return entry.get("last_price") if isinstance(entry, dict) else getattr(entry, "last_price", 0)

    # Build strike → (ce_premium, pe_premium) map
    ce_map = {}
    for inst in ce_instruments:
        s = inst.get("strike_price", 0)
        ce_map[s] = get_price(inst["instrument_key"]) or 0

    pe_map = {}
    for inst in pe_instruments:
        s = inst.get("strike_price", 0)
        pe_map[s] = get_price(inst["instrument_key"]) or 0

    all_strikes = sorted(set(list(ce_map.keys()) + list(pe_map.keys())))
    atm_strike = min(all_strikes, key=lambda s: abs(s - spot)) if all_strikes else 0

    expiry_label = ce_instruments[0].get("expiry", args.expiry) if ce_instruments else args.expiry

    # Display
    print(f"  Spot: {spot:,.2f}  |  ATM: {atm_strike:,.0f}  |  Expiry: {expiry_label}\n")

    print(f"  {'Strike':>10}  {'CE Prem':>10}  {'CE %Spot':>10}  "
          f"{'PE Prem':>10}  {'PE %Spot':>10}  {'Straddle':>10}  {'Strd %':>8}")
    print("  " + "-" * 80)

    for strike in all_strikes:
        ce_p = ce_map.get(strike, 0)
        pe_p = pe_map.get(strike, 0)
        ce_pct = ce_p / spot * 100 if spot else 0
        pe_pct = pe_p / spot * 100 if spot else 0
        straddle = ce_p + pe_p
        strd_pct = straddle / spot * 100 if spot else 0

        is_atm = strike == atm_strike
        marker = f"{CYAN}→{RESET}" if is_atm else " "
        bold = BOLD if is_atm else ""

        print(f" {marker}{bold}{strike:>10,.0f}{RESET}  "
              f"{GREEN}{ce_p:>10,.2f}{RESET}  {ce_pct:>9.2f}%  "
              f"{RED}{pe_p:>10,.2f}{RESET}  {pe_pct:>9.2f}%  "
              f"{bold}{straddle:>10,.2f}{RESET}  {strd_pct:>7.2f}%")

    print("  " + "-" * 80)

    atm_ce = ce_map.get(atm_strike, 0)
    atm_pe = pe_map.get(atm_strike, 0)
    atm_total = atm_ce + atm_pe
    atm_pct = atm_total / spot * 100 if spot else 0

    print(f"\n  {BOLD}ATM straddle premium: {atm_total:,.2f} ({atm_pct:.2f}% of spot){RESET}")
    if atm_pct < 0.5:
        print(f"  {DIM}Very low premium — theta decay is nearly complete.{RESET}")
    elif atm_pct < 1.5:
        print(f"  {CYAN}Moderate premium — significant decay expected if near expiry.{RESET}")
    else:
        print(f"  {GREEN}Substantial premium remaining — time value still meaningful.{RESET}")
    print()


if __name__ == "__main__":
    main()
