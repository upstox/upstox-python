"""
IPO Listing — list IPOs by status and issue type.

Usage:
  python ipo/ipo_listing.py --token <TOKEN>
  python ipo/ipo_listing.py --token <TOKEN> --status open
  python ipo/ipo_listing.py --token <TOKEN> --status upcoming --issue-type sme --records 30
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import get_api_client, die
import upstox_client

BOLD  = "\033[1m"
DIM   = "\033[2m"
RESET = "\033[0m"

STATUSES    = ["open", "closed", "listed", "upcoming"]
ISSUE_TYPES = ["regular", "sme"]


def _as_dict(o):
    if o is None:
        return {}
    if isinstance(o, dict):
        return o
    if hasattr(o, "to_dict"):
        return o.to_dict()
    return vars(o) if hasattr(o, "__dict__") else {}


def _val(o, key):
    d = _as_dict(o)
    v = d.get(key)
    return "—" if v is None or v == "" else v


def _band(row):
    """Render the price band as 'min – max', collapsing to a single value when equal."""
    lo, hi = _as_dict(row).get("minimum_price"), _as_dict(row).get("maximum_price")
    if lo is None and hi is None:
        return "—"
    if lo == hi or hi is None:
        return f"{lo}"
    if lo is None:
        return f"{hi}"
    return f"{lo} – {hi}"


def main():
    parser = argparse.ArgumentParser(description="List Upstox IPOs by status and issue type")
    parser.add_argument("--token", required=True, help="Upstox access token or analytics token")
    parser.add_argument("--status", choices=STATUSES, help="Filter by IPO status")
    parser.add_argument("--issue-type", choices=ISSUE_TYPES, dest="issue_type",
                        help="Filter by issue type")
    parser.add_argument("--page-number", type=int, default=1, dest="page_number",
                        help="Page number (default: 1)")
    parser.add_argument("--records", type=int, default=20,
                        help="Records per page (default: 20, max: 30)")
    args = parser.parse_args()

    client = get_api_client(args.token)
    api = upstox_client.IpoApi(client)

    kwargs = {"page_number": args.page_number, "records": args.records}
    if args.status:
        kwargs["status"] = args.status
    if args.issue_type:
        kwargs["issue_type"] = args.issue_type

    try:
        response = api.get_ipo_listing(**kwargs)
    except Exception as e:
        die(f"API error: {e}")

    rows = response.data or []
    if not rows:
        print("No IPOs found for the given filters.")
        return

    label = args.status or "all"
    print(f"\n{BOLD}IPO Listing — {label}{RESET}\n")
    print(f"{'Symbol':<14} {'Name':<30} {'Status':<10} {'Type':<9} "
          f"{'Price Band':>16} {'Bid End':>12} {'Subs':>8}")
    print("─" * 104)

    for row in rows:
        print(
            f"{str(_val(row, 'symbol')):<14.13} "
            f"{str(_val(row, 'name')):<30.29} "
            f"{str(_val(row, 'status')):<10.9} "
            f"{str(_val(row, 'issue_type')):<9.8} "
            f"{_band(row):>16} "
            f"{str(_val(row, 'bidding_end_date')):>12.11} "
            f"{str(_val(row, 'total_subscription')):>8.7}"
        )

    meta = getattr(response, "meta_data", None)
    page = getattr(meta, "page", None) if meta else None
    if page:
        print(
            f"\n{DIM}Page {getattr(page, 'page_number', '?')} of "
            f"{getattr(page, 'total_pages', '?')}  |  "
            f"{len(rows)} of {getattr(page, 'total_records', '?')} total{RESET}"
        )
    print()


if __name__ == "__main__":
    main()
