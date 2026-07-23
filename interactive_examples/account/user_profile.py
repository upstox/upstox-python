"""
User Profile — read-only account profile (name, email, broker, exchanges, products).

Fetches the authenticated user's profile from the Upstox User API. Read-only:
nothing about the account is modified.

Usage:
  python account/user_profile.py --token <TOKEN>
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import get_api_client, as_dict, die
import upstox_client

BOLD  = "\033[1m"
CYAN  = "\033[36m"
DIM   = "\033[2m"
RESET = "\033[0m"


def _fmt_list(v):
    if isinstance(v, (list, tuple)):
        return ", ".join(str(x) for x in v) if v else "—"
    return str(v) if v not in (None, "") else "—"


def main():
    parser = argparse.ArgumentParser(description="User Profile via User API (read-only)")
    parser.add_argument("--token", required=True, help="Upstox access or analytics token")
    args = parser.parse_args()

    client = get_api_client(args.token)
    api = upstox_client.UserApi(client)

    print(f"\n{BOLD}Fetching user profile...{RESET}\n")

    try:
        response = api.get_profile("2.0")
    except Exception as e:
        die(f"API error: {e}")

    data = as_dict(response.data)
    if not data:
        die("No profile data returned.")

    fields = [
        ("User ID",         data.get("user_id")),
        ("User Name",       data.get("user_name")),
        ("Email",           data.get("email")),
        ("User Type",       data.get("user_type")),
        ("Broker",          data.get("broker")),
        ("Active",          data.get("is_active")),
        ("POA",             data.get("poa")),
        ("DDPI",            data.get("ddpi")),
        ("Exchanges",       _fmt_list(data.get("exchanges"))),
        ("Products",        _fmt_list(data.get("products"))),
        ("Order Types",     _fmt_list(data.get("order_types"))),
    ]

    print(f"  {BOLD}{'Field':<16} Value{RESET}")
    print("  " + "─" * 60)
    for label, value in fields:
        shown = "—" if value in (None, "") else value
        print(f"  {CYAN}{label:<16}{RESET} {shown}")

    print(f"\n  {DIM}Read-only profile — no account settings were changed.{RESET}\n")


if __name__ == "__main__":
    main()
