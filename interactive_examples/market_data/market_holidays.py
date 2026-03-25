"""
Market Holidays — split the exchange holiday calendar into past and upcoming,
displayed as two formatted tables.

Usage:
  python market_data/market_holidays.py --token <TOKEN>
"""

import argparse
import sys
import os
from datetime import date, datetime, timezone, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import get_api_client
import upstox_client

BOLD    = "\033[1m"
GREEN   = "\033[32m"
YELLOW  = "\033[33m"
DIM     = "\033[2m"
RESET   = "\033[0m"
BLACK   = "\033[30m"
BG_ALT  = "\033[47m"   # light grey stripe
FG_RST  = "\033[39m"   # reset foreground only (keeps background)
DIM_RST = "\033[22m"   # reset bold/dim only (keeps background)

IST = timezone(timedelta(hours=5, minutes=30))


def fmt_days(delta: int) -> str:
    if delta == 0:
        return "today"
    if delta == 1:
        return "tomorrow"
    if delta == -1:
        return "yesterday"
    return f"{abs(delta)}d {'ago' if delta < 0 else 'ahead'}"


def ms_to_ist(ms: int) -> str:
    return datetime.fromtimestamp(ms / 1000, tz=IST).strftime("%H:%M")


def session_label(exchange: str, start_hm: str, end_hm: str) -> str:
    """Classify a partial session into a human-readable label."""
    start_min = int(start_hm[:2]) * 60 + int(start_hm[3:])
    end_min   = int(end_hm[:2])   * 60 + int(end_hm[3:])
    duration  = end_min - start_min

    if exchange in ("MCX", "NSCOM"):
        if start_min >= 17 * 60 and duration <= 90:
            return "Muhurat trading"
        elif start_min >= 17 * 60:
            return "evening session open"
        elif end_min <= 17 * 60:
            return "morning session open"
        else:
            return "both sessions open"
    else:
        return "normal trading"


def main():
    parser = argparse.ArgumentParser(description="Exchange holiday calendar — past vs upcoming")
    parser.add_argument("--token", required=True, help="Upstox access or analytics token")
    args = parser.parse_args()

    client = get_api_client(args.token)
    api    = upstox_client.MarketHolidaysAndTimingsApi(client)

    resp     = api.get_holidays()
    holidays = resp.data if resp.data else []
    if not isinstance(holidays, list):
        holidays = [holidays]

    # Collect full exchange universe from all holidays
    all_exchanges: set = set()
    for h in holidays:
        for e in (getattr(h, "closed_exchanges", None) or []):
            all_exchanges.add(e)
        for entry in (getattr(h, "_open_exchanges", None) or []):
            exch = getattr(entry, "exchange", "") or (entry.get("exchange", "") if isinstance(entry, dict) else "")
            if exch:
                all_exchanges.add(exch)

    today = date.today()
    past, upcoming = [], []

    for h in holidays:
        raw_date    = getattr(h, "_date", None) or getattr(h, "date", None) or ""
        description = getattr(h, "description", None) or getattr(h, "holiday_name", "") or ""
        closed_exch = set(getattr(h, "closed_exchanges", None) or [])
        open_exch   = getattr(h, "_open_exchanges", None) or []

        partial_exch = set()
        normal_exch  = set()
        label_map: dict = {}
        for entry in open_exch:
            exch  = getattr(entry, "exchange",   "") or (entry.get("exchange",   "") if isinstance(entry, dict) else "")
            start = getattr(entry, "start_time", 0)  or (entry.get("start_time", 0)  if isinstance(entry, dict) else 0)
            end   = getattr(entry, "end_time",   0)  or (entry.get("end_time",   0)  if isinstance(entry, dict) else 0)
            if exch and start and end:
                label = session_label(exch, ms_to_ist(start), ms_to_ist(end))
                if label in ("normal trading", "both sessions open"):
                    normal_exch.add(exch)
                else:
                    partial_exch.add(exch)
                    label_map.setdefault(label, []).append(exch)

        # Fully open = not closed, not partial (normal trading from open_exchanges counts as open)
        fully_open = sorted(all_exchanges - closed_exch - partial_exch)

        closed_str  = ",".join(sorted(closed_exch)) if closed_exch else "—"
        open_str    = ",".join(fully_open)          if fully_open  else "—"
        partial_parts = [f"{','.join(exchs)}: {lbl}" for lbl, exchs in label_map.items()]
        partial_note  = "  |  ".join(partial_parts)

        try:
            if hasattr(raw_date, "date"):
                hdate = raw_date.date()
            else:
                hdate = date.fromisoformat(str(raw_date)[:10])
        except Exception:
            continue

        delta = (hdate - today).days
        date_str = f"{hdate}  {hdate.strftime('%a')}"
        row = (date_str, description, open_str, closed_str, partial_note, delta)
        if delta < 0:
            past.append(row)
        else:
            upcoming.append(row)

    past.sort(key=lambda r: r[0], reverse=True)
    upcoming.sort(key=lambda r: r[0])

    def print_table(title, rows, colour):
        print(f"\n{BOLD}{colour}{title}{RESET}")
        print(f"{'Date':<18} {'Holiday':<28} {'Open':<30} {'Closed':<38} {'When'}")
        print("─" * 120)
        if not rows:
            print("  (none)")
            return
        for i, (date_str, desc, open_s, closed, partial, delta) in enumerate(rows):
            bg   = BG_ALT if i % 2 == 0 else ""
            when = fmt_days(delta)
            print(f"{bg}{date_str:<18} {desc[:27]:<28} {GREEN}{open_s:<30}{FG_RST}{bg} {closed:<38} {BLACK}{when}{FG_RST}\033[K{RESET}")
            if partial:
                print(f"{bg}{'':18} {YELLOW}partial: {partial}{FG_RST}\033[K{RESET}")

    print_table("Past Holidays (this year)", past,     "\033[2m")
    print_table("Upcoming Holidays",         upcoming, GREEN)
    print()


if __name__ == "__main__":
    main()
