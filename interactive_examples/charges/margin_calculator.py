"""
Margin Calculator — compute the margin required for one or more prospective orders.

Uses the Upstox Charge API (POST margin) to estimate the SPAN / exposure / total
margin required for a basket of orders WITHOUT placing them. Nothing is sent to
the exchange — this is a pure what-if calculation.

Usage:
  python charges/margin_calculator.py --token <TOKEN> --symbol RELIANCE --quantity 10 --price 1400
  python charges/margin_calculator.py --token <TOKEN> --symbol TCS --quantity 5 --price 3900 \
      --product D --transaction-type BUY
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import get_api_client, resolve_equity, index_instrument, as_dict, die
import upstox_client

BOLD  = "\033[1m"
GREEN = "\033[32m"
CYAN  = "\033[36m"
DIM   = "\033[2m"
RESET = "\033[0m"


def _fmt_amt(v):
    try:
        return f"{float(v):>16,.2f}"
    except (TypeError, ValueError):
        return f"{str(v) if v not in (None, '') else '—':>16}"


def main():
    parser = argparse.ArgumentParser(description="Required-margin estimator via Charge API")
    parser.add_argument("--token",  required=True, help="Upstox access or analytics token")
    parser.add_argument("--symbol", default="RELIANCE", help="Stock symbol (default: RELIANCE)")
    parser.add_argument("--quantity", type=int, default=10, help="Order quantity (default: 10)")
    parser.add_argument("--price", type=float, default=1400.0, help="Order price (default: 1400)")
    parser.add_argument("--product", default="D",
                        help="Product code: D=delivery, I=intraday (default: D)")
    parser.add_argument("--transaction-type", default="BUY", choices=("BUY", "SELL"),
                        help="BUY or SELL (default: BUY)")
    args = parser.parse_args()

    client = get_api_client(args.token)

    # Indices are not tradable — reject them instead of silently pricing a
    # look-alike ETF (e.g. NIFTY resolving to NIFTYBEES).
    idx = index_instrument(client, args.symbol)
    if idx:
        die(f"'{args.symbol.upper()}' is a market index and cannot be traded directly. "
            f"Enter a tradable stock or ETF symbol (e.g. RELIANCE, or NIFTYBEES for the NIFTY ETF).")

    inst = resolve_equity(client, args.symbol)
    if not inst:
        die(f"No NSE equity instrument found for '{args.symbol}'.")
    instrument_key = inst.get("instrument_key", "")
    resolved = inst.get("trading_symbol") or args.symbol.upper()

    print(f"\n{BOLD}Estimating required margin{RESET} for {args.transaction_type} "
          f"{args.quantity} × {resolved} @ {args.price:,.2f} "
          f"(product={args.product})...")
    print(f"  {DIM}Resolved '{args.symbol}' → {resolved} — {inst.get('name', '')} "
          f"[{instrument_key}]{RESET}\n")

    instrument = upstox_client.Instrument(
        instrument_key=instrument_key,
        quantity=args.quantity,
        product=args.product,
        transaction_type=args.transaction_type,
        price=args.price,
    )
    body = upstox_client.MarginRequest(instruments=[instrument])

    api = upstox_client.ChargeApi(client)
    try:
        response = api.post_margin(body)
    except Exception as e:
        die(f"API error: {e}")

    data = as_dict(response.data)
    if not data:
        die("No margin data returned.")

    print(f"  {BOLD}{'Field':<24} {'Amount (INR)':>16}{RESET}")
    print("  " + "─" * 44)
    print(f"  {'Required Margin':<24} {_fmt_amt(data.get('required_margin'))}")
    print(f"  {GREEN}{'Final Margin':<24}{RESET} {_fmt_amt(data.get('final_margin'))}")

    margins = data.get("margins") or []
    for i, m in enumerate(margins, start=1):
        m = as_dict(m)
        print(f"\n  {CYAN}Leg {i} breakdown{RESET}")
        for key in ("span_margin", "exposure_margin", "equity_margin",
                    "net_buy_premium", "additional_margin", "total_margin"):
            if key in m:
                print(f"    {key:<22} {_fmt_amt(m.get(key))}")

    print(f"\n  {DIM}Estimate only — no order was placed.{RESET}\n")


if __name__ == "__main__":
    main()
