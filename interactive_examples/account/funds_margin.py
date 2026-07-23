"""
Funds & Margin — read-only view of available / unavailable funds (v3).

Fetches the authenticated user's funds and margin from the Upstox User API
(v3). Read-only: nothing about the account is modified.

Usage:
  python account/funds_margin.py --token <TOKEN>
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import get_api_client, as_dict, die
import upstox_client

BOLD  = "\033[1m"
GREEN = "\033[32m"
CYAN  = "\033[36m"
DIM   = "\033[2m"
RESET = "\033[0m"


def _fmt_amt(v):
    try:
        return f"{GREEN}{float(v):>16,.2f}{RESET}"
    except (TypeError, ValueError):
        return f"{str(v) if v not in (None, '') else '—':>16}"


def _print_block(title, node, indent=2):
    """Print a nested funds block; recurse one level into sub-dicts."""
    node = as_dict(node)
    if not node:
        return
    pad = " " * indent
    print(f"{pad}{BOLD}{CYAN}{title}{RESET}")
    for key, val in node.items():
        sub = as_dict(val)
        if sub:
            _print_block(key, sub, indent + 2)
        else:
            print(f"{pad}  {key:<28} {_fmt_amt(val)}")


def main():
    parser = argparse.ArgumentParser(description="Funds & Margin via User API v3 (read-only)")
    parser.add_argument("--token", required=True, help="Upstox access or analytics token")
    args = parser.parse_args()

    client = get_api_client(args.token)
    api = upstox_client.UserApi(client)

    print(f"\n{BOLD}Fetching funds & margin (v3)...{RESET}\n")

    try:
        response = api.get_user_fund_margin_v3()
    except Exception as e:
        die(f"API error: {e}")

    data = as_dict(response.data)
    if not data:
        die("No funds data returned.")

    _print_block("Available to Trade", data.get("available_to_trade"))
    print()
    _print_block("Unavailable to Trade", data.get("unavailable_to_trade"))

    print(f"\n  {DIM}Read-only — no funds were moved.{RESET}\n")


if __name__ == "__main__":
    main()
