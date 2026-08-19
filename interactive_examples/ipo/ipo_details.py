"""
IPO Details — full profile for a single IPO: price band, timeline, registrar and subscription.

With no --id, the most recent IPO from the listing endpoint is used.

Usage:
  python ipo/ipo_details.py --token <TOKEN>
  python ipo/ipo_details.py --token <TOKEN> --id <IPO_SLUG_ID>
  python ipo/ipo_details.py --token <TOKEN> --status upcoming
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

# (attribute on IpoDetailsData, display label)
PROFILE_FIELDS = [
    ("name",              "Name"),
    ("symbol",            "Symbol"),
    ("isin",              "ISIN"),
    ("status",            "Status"),
    ("issue_type",        "Issue type"),
    ("industry",          "Industry"),
    ("issue_size",        "Issue size"),
    ("face_value",        "Face value"),
    ("tick_size",         "Tick size"),
    ("lot_size",          "Lot size"),
    ("minimum_quantity",  "Min quantity"),
    ("cut_off_price",     "Cut-off price"),
    ("listing_price",     "Listing price"),
    ("listing_exchange",  "Listing exchange"),
    ("total_subscription", "Total subscription"),
]

TIMELINE_FIELDS = [
    ("pre_apply_start_date",   "Pre-apply start"),
    ("application_start_date", "Application start"),
    ("application_end_date",   "Application end"),
    ("allotment_start_date",   "Allotment start"),
    ("allotment_date",         "Allotment"),
    ("refund_initiation_date", "Refund initiation"),
    ("mandate_end_date",       "Mandate end"),
    ("listing_date",           "Listing"),
]

REGISTRAR_FIELDS = [
    ("name",           "Registrar"),
    ("registrar",      "Registrar code"),
    ("contact_name",   "Contact"),
    ("contact_number", "Phone"),
    ("email",          "Email"),
    ("website",        "Website"),
]


def _get(obj, key):
    """Attribute or key lookup that tolerates None, models and plain dicts."""
    if obj is None:
        return None
    if isinstance(obj, dict):
        return obj.get(key)
    return getattr(obj, key, None)


def _show(obj, fields, heading):
    rows = [(label, _get(obj, attr)) for attr, label in fields]
    rows = [(label, v) for label, v in rows if v is not None and v != ""]
    if not rows:
        return
    print(f"{CYAN}{BOLD}{heading}{RESET}")
    for label, value in rows:
        print(f"  {label:<22} {value}")
    print()


def _resolve_id(api, status):
    """Pick an IPO slug from the listing endpoint when the user did not supply one."""
    kwargs = {"page_number": 1, "records": 1}
    if status:
        kwargs["status"] = status
    try:
        listing = api.get_ipo_listing(**kwargs)
    except Exception as e:
        die(f"API error while resolving an IPO id: {e}")

    rows = listing.data or []
    if not rows:
        die("No IPOs available to resolve an id from. Pass --id explicitly.")

    row = rows[0]
    ipo_id = row.get("id") if isinstance(row, dict) else getattr(row, "id", None)
    if not ipo_id:
        die("Listing returned an IPO without an id. Pass --id explicitly.")
    return ipo_id


def main():
    parser = argparse.ArgumentParser(description="Full details for a single Upstox IPO")
    parser.add_argument("--token", required=True, help="Upstox access token or analytics token")
    parser.add_argument("--id", help="IPO slug ID (default: first IPO from the listing)")
    parser.add_argument("--status", choices=["open", "closed", "listed", "upcoming"],
                        help="When --id is omitted, resolve the id from this status")
    args = parser.parse_args()

    client = get_api_client(args.token)
    api = upstox_client.IpoApi(client)

    ipo_id = args.id or _resolve_id(api, args.status)
    if not args.id:
        print(f"{DIM}No --id given; using '{ipo_id}' from the listing.{RESET}")

    try:
        response = api.get_ipo_details(ipo_id)
    except Exception as e:
        die(f"API error: {e}")

    data = response.data
    if data is None:
        die(f"No IPO found with id '{ipo_id}'.")

    print(f"\n{BOLD}IPO Details — {ipo_id}{RESET}\n")

    _show(data, PROFILE_FIELDS, "Profile")

    lo, hi = _get(data, "minimum_price"), _get(data, "maximum_price")
    if lo is not None or hi is not None:
        band = f"{lo} – {hi}" if lo != hi and hi is not None else f"{lo if lo is not None else hi}"
        print(f"{CYAN}{BOLD}Price band{RESET}\n  {band}\n")

    bid_start, bid_end = _get(data, "bidding_start_date"), _get(data, "bidding_end_date")
    if bid_start or bid_end:
        print(f"{CYAN}{BOLD}Bidding window{RESET}")
        print(f"  {'Start':<22} {bid_start or '—'}")
        print(f"  {'End':<22} {bid_end or '—'}")
        daily_start, daily_end = _get(data, "daily_start_time"), _get(data, "daily_end_time")
        if daily_start or daily_end:
            print(f"  {'Daily window':<22} {daily_start or '—'} – {daily_end or '—'}")
        print()

    _show(_get(data, "timeline"), TIMELINE_FIELDS, "Timeline")
    _show(_get(data, "registrar_info"), REGISTRAR_FIELDS, "Registrar")

    investors = _get(data, "investors") or []
    if investors:
        print(f"{CYAN}{BOLD}Investor categories{RESET}")
        for inv in investors:
            category = _get(inv, "category") or "—"
            description = _get(inv, "description") or ""
            print(f"  {str(category):<22} {description}")
        print()

    for attr, label in (("rhp_url", "RHP"), ("drhp_url", "DRHP")):
        url = _get(data, attr)
        if url:
            print(f"{DIM}{label}: {url}{RESET}")
    print()


if __name__ == "__main__":
    main()
