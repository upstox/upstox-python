"""
Brokerage Calculator — compute brokerage & statutory charges for a prospective order.

Uses the Upstox Charge API to estimate brokerage, taxes and total charges for an
order WITHOUT placing it. Nothing is sent to the exchange — this is a pure
what-if calculation.

Usage:
  python charges/brokerage_calculator.py --token <TOKEN> --symbol RELIANCE --quantity 10 --price 1400
  python charges/brokerage_calculator.py --token <TOKEN> --symbol TCS --quantity 5 --price 3900 \
      --product D --transaction-type BUY
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import get_api_client, resolve_equity, as_dict, die
import upstox_client

BOLD  = "\033[1m"
GREEN = "\033[32m"
CYAN  = "\033[36m"
DIM   = "\033[2m"
RESET = "\033[0m"


def _fmt_amt(v):
    try:
        return f"{float(v):>14,.2f}"
    except (TypeError, ValueError):
        return f"{str(v) if v not in (None, '') else '—':>14}"


def _flatten_charges(node, prefix=""):
    """Flatten the nested charges tree into (label, amount) rows."""
    node = as_dict(node)
    rows = []
    for key, val in node.items():
        sub = as_dict(val)
        label = f"{prefix}{key}"
        if sub:
            rows.extend(_flatten_charges(sub, prefix=f"{label}."))
        else:
            rows.append((label, val))
    return rows


def main():
    parser = argparse.ArgumentParser(description="Brokerage & charges estimator via Charge API")
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

    inst = resolve_equity(client, args.symbol)
    if not inst:
        die(f"No NSE equity instrument found for '{args.symbol}'.")
    instrument_token = inst.get("instrument_key", "")

    print(f"\n{BOLD}Estimating charges{RESET} for {args.transaction_type} "
          f"{args.quantity} × {args.symbol.upper()} @ {args.price:,.2f} "
          f"(product={args.product})...\n")

    api = upstox_client.ChargeApi(client)
    try:
        response = api.get_brokerage(
            instrument_token, args.quantity, args.product,
            args.transaction_type, args.price, "2.0",
        )
    except Exception as e:
        die(f"API error: {e}")

    data = as_dict(response.data)
    if not data:
        die("No charge data returned.")

    charges = as_dict(data.get("charges"))
    rows = _flatten_charges(charges) if charges else _flatten_charges(data)
    if not rows:
        die("No charge breakdown returned.")

    print(f"  {BOLD}{'Charge':<32} {'Amount (INR)':>14}{RESET}")
    print("  " + "─" * 50)
    for label, amount in rows:
        highlight = "total" in label.lower()
        colour = GREEN if highlight else ""
        print(f"  {colour}{label:<32}{RESET} {_fmt_amt(amount)}")

    print(f"\n  {DIM}Estimate only — no order was placed.{RESET}\n")


if __name__ == "__main__":
    main()
