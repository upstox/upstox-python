"""
Market Timings — show exchange session windows (pre-open, normal, closing, post-close)
for a given date and highlight the currently active session based on IST time.

Usage:
  python market_data/market_timings.py --token <TOKEN>
  python market_data/market_timings.py --token <TOKEN> --date 2026-03-28
"""

import argparse
import sys
import os
from datetime import datetime, timezone, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import get_api_client, today_str
import upstox_client

BOLD   = "\033[1m"
GREEN  = "\033[32m"
YELLOW = "\033[33m"
DIM    = "\033[2m"
RESET  = "\033[0m"

IST = timezone(timedelta(hours=5, minutes=30))


def ist_now() -> str:
    """Return current IST time as HH:MM."""
    return datetime.now(IST).strftime("%H:%M")


def is_active(start: str, end: str, now: str) -> bool:
    """True if now falls within [start, end] (all HH:MM strings)."""
    try:
        return start <= now <= end
    except Exception:
        return False


def main():
    parser = argparse.ArgumentParser(description="Exchange session timings for a date")
    parser.add_argument("--token", required=True, help="Upstox access or analytics token")
    parser.add_argument("--date",  default=today_str(),
                        help="Date in YYYY-MM-DD format (default: today)")
    args = parser.parse_args()

    client = get_api_client(args.token)
    api    = upstox_client.MarketHolidaysAndTimingsApi(client)

    resp    = api.get_exchange_timings(args.date)
    timings = resp.data if resp.data else []
    if not isinstance(timings, list):
        timings = [timings]

    now_ist = ist_now()
    print(f"\n{BOLD}Exchange Timings — {args.date}  (IST now: {now_ist}){RESET}\n")
    print(f"{'Exchange':<12} {'Segment':<20} {'Session':<18} {'Start':>7}  {'End':>7}  {'Active'}")
    print("─" * 80)

    for t in timings:
        exchange   = getattr(t, "exchange",   "") or ""
        start_ms   = getattr(t, "start_time", 0)  or 0
        end_ms     = getattr(t, "end_time",   0)  or 0

        # Convert ms epoch → IST HH:MM
        def ms_to_ist_hm(ms):
            if not ms:
                return "—"
            return datetime.fromtimestamp(ms / 1000, tz=IST).strftime("%H:%M")

        start_hm = ms_to_ist_hm(start_ms)
        end_hm   = ms_to_ist_hm(end_ms)

        active = is_active(start_hm, end_hm, now_ist) if start_hm != "—" else False
        marker = f"{GREEN}◉ ACTIVE{RESET}" if active else f"{DIM}○{RESET}"

        print(f"{exchange:<12} {'Trading Hours':<20} {'Normal':<18} {start_hm:>7}  {end_hm:>7}  {marker}")

    print()


if __name__ == "__main__":
    main()
