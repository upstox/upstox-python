"""
IPO Orders — list your IPO applications, or fetch one by order ID.

Requires a full access token (read-only analytics tokens cannot read your order book).

Usage:
  python ipo/ipo_orders.py --token <TOKEN>
  python ipo/ipo_orders.py --token <TOKEN> --records 30
  python ipo/ipo_orders.py --token <TOKEN> --order-id <ORDER_ID>
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import get_api_client, die
import upstox_client

BOLD  = "\033[1m"
CYAN  = "\033[36m"
DIM   = "\033[2m"
RESET = "\033[0m"

DETAIL_FIELDS = [
    ("symbol",                "Symbol"),
    ("exchange",              "Exchange"),
    ("order_id",             "Order ID"),
    ("request_id",           "Request ID"),
    ("status",               "Status"),
    ("order_status",         "Order status"),
    ("payment_status",       "Payment status"),
    ("category",             "Category"),
    ("issue_type",           "Issue type"),
    ("upi",                  "UPI"),
    ("upi_amount_blocked",   "Amount blocked"),
    ("units_allotted",       "Units allotted"),
    ("reason",               "Reason"),
    ("nse_submitted_date",   "NSE submitted"),
    ("bse_submitted_date",   "BSE submitted"),
    ("mandate_approved_date", "Mandate approved"),
    ("mandate_rejection_date", "Mandate rejected"),
    ("rejection_date",       "Rejected"),
    ("cancel_requested_date", "Cancel requested"),
    ("cancel_accepted_date", "Cancel accepted"),
    ("created_at",           "Created"),
    ("last_updated_at",      "Last updated"),
]


def _as_dict(o):
    if o is None:
        return {}
    if isinstance(o, dict):
        return o
    if hasattr(o, "to_dict"):
        return o.to_dict()
    return vars(o) if hasattr(o, "__dict__") else {}


def _val(o, key):
    v = _as_dict(o).get(key)
    return "—" if v is None or v == "" else v


def _print_bids(order):
    bids = _as_dict(order).get("bids") or []
    if not bids:
        return
    print(f"{CYAN}{BOLD}Bids{RESET}")
    print(f"  {'Quantity':>10} {'Price':>12} {'Amount':>14}  Message")
    for bid in bids:
        b = _as_dict(bid)
        print(
            f"  {str(b.get('quantity', '—')):>10} "
            f"{str(b.get('price', '—')):>12} "
            f"{str(b.get('amount', '—')):>14}  "
            f"{b.get('message', '') or ''}"
        )
    print()


def _print_one(order):
    print(f"{CYAN}{BOLD}Order{RESET}")
    for attr, label in DETAIL_FIELDS:
        value = _as_dict(order).get(attr)
        if value is None or value == "":
            continue
        print(f"  {label:<22} {value}")
    print()
    _print_bids(order)


def main():
    parser = argparse.ArgumentParser(description="List Upstox IPO orders, or fetch one by ID")
    parser.add_argument("--token", required=True, help="Upstox access token (not analytics)")
    parser.add_argument("--order-id", dest="order_id",
                        help="Fetch a single order by ID instead of listing")
    parser.add_argument("--page-number", type=int, default=1, dest="page_number",
                        help="Page number (default: 1)")
    parser.add_argument("--records", type=int, default=20,
                        help="Records per page (default: 20)")
    args = parser.parse_args()

    client = get_api_client(args.token)
    api = upstox_client.IpoApi(client)

    if args.order_id:
        try:
            response = api.get_ipo_order_by_id(args.order_id)
        except Exception as e:
            die(f"API error: {e}")

        order = response.data
        if order is None:
            die(f"No IPO order found with ID '{args.order_id}'.")

        print(f"\n{BOLD}IPO Order — {args.order_id}{RESET}\n")
        _print_one(order)
        return

    try:
        response = api.get_ipo_orders(page_number=args.page_number, records=args.records)
    except Exception as e:
        die(f"API error: {e}")

    orders = response.data or []
    if not orders:
        print("No IPO orders found.")
        return

    print(f"\n{BOLD}IPO Orders{RESET}\n")
    print(f"{'Symbol':<14} {'Order ID':<22} {'Status':<12} {'Payment':<12} "
          f"{'Blocked':>14} {'Allotted':>10}")
    print("─" * 90)

    for order in orders:
        print(
            f"{str(_val(order, 'symbol')):<14.13} "
            f"{str(_val(order, 'order_id')):<22.21} "
            f"{str(_val(order, 'order_status')):<12.11} "
            f"{str(_val(order, 'payment_status')):<12.11} "
            f"{str(_val(order, 'upi_amount_blocked')):>14} "
            f"{str(_val(order, 'units_allotted')):>10}"
        )

    meta = getattr(response, "meta_data", None)
    page = getattr(meta, "page", None) if meta else None
    if page:
        print(
            f"\n{DIM}Page {getattr(page, 'page_number', '?')} of "
            f"{getattr(page, 'total_pages', '?')}  |  "
            f"{len(orders)} of {getattr(page, 'total_records', '?')} total{RESET}"
        )
    print()


if __name__ == "__main__":
    main()
