"""
MCX Live Depth (5-level) — WebSocket streaming using MarketDataStreamerV3.

Fetches current-month futures for well-known MCX commodities, ranks them by
today's traded volume, then subscribes the top N in FULL mode (5-level depth).

Instruments are displayed side by side (2 per row), updated live.
Runs until Ctrl-C (the test_runner aborts it after 5 seconds).

Usage:
  python market_data/live_depth_mcx.py --token <TOKEN>
  python market_data/live_depth_mcx.py --token <TOKEN> --top 6
"""

import argparse
import re
import sys
import os
import time
import threading

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import get_api_client, search_instrument, get_ltp
import upstox_client

BOLD  = "\033[1m"
GREEN = "\033[32m"
RED   = "\033[31m"
CYAN  = "\033[36m"
DIM   = "\033[2m"
RESET = "\033[0m"
CLEAR = "\033[2J\033[H"

# Well-known MCX commodity futures, checked in order
MCX_CANDIDATES = [
    "GOLD", "SILVER", "CRUDEOIL", "NATURALGAS",
    "COPPER", "ZINC", "ALUMINIUM", "NICKEL", "LEAD", "COTTON",
]

depth_store: dict = {}
lock = threading.Lock()

_ANSI = re.compile(r"\033\[[0-9;]*m")


def visible_len(s: str) -> int:
    return len(_ANSI.sub("", s))


def pad_to(s: str, width: int) -> str:
    return s + " " * max(0, width - visible_len(s))


# ── Instrument discovery ───────────────────────────────────────────────────────

def find_top_mcx(client, top_n: int) -> list[dict]:
    """Return up to top_n MCX current-month futures sorted by volume (desc)."""
    found = []
    for sym in MCX_CANDIDATES:
        resp = search_instrument(
            client, sym,
            exchanges="MCX",
            segments="COMM",
            instrument_types="FUT",
            expiry="current_month",
            records=5,
        )
        instruments = [i for i in (resp.data or [])
                       if isinstance(i, dict) and i.get("trading_symbol", "").upper().startswith(sym)]
        if instruments:
            instruments.sort(key=lambda x: x.get("expiry", ""))
            found.append(instruments[0])

    if not found:
        return []

    # Rank by today's traded volume
    keys = [i["instrument_key"] for i in found]
    try:
        ltp_data = get_ltp(client, *keys)
        def _vol(instr):
            entry = ltp_data.get(instr["instrument_key"], {})
            v = entry.get("volume") if isinstance(entry, dict) else getattr(entry, "volume", 0)
            return v or 0
        found.sort(key=_vol, reverse=True)
    except Exception:
        pass   # if quote call fails, keep discovery order

    return found[:top_n]


# ── Depth rendering ────────────────────────────────────────────────────────────

COL_WIDTH = 58   # visible width of each instrument column

def render_depth(symbol: str, market_ff: dict) -> list[str]:
    lines = [f"{BOLD}{CYAN}{symbol}{RESET}"]

    ltp = market_ff.get("ltpc", {}).get("ltp")
    lines.append(f"  LTP: {BOLD}{float(ltp):,.2f}{RESET}" if ltp else "  LTP: —")
    lines.append("")

    quotes = market_ff.get("marketLevel", {}).get("bidAskQuote", [])
    if not quotes:
        lines.append("  (depth not available)")
        return lines

    lines.append(f"  {'Qty':>10}  {'Bid':>12}  {'Ask':>12}  {'Qty':>10}")
    lines.append("  " + "─" * 50)

    for q in quotes[:5]:
        bid_p = f"{float(q.get('bidP', 0)):,.2f}"
        bid_q = f"{int(q.get('bidQ', 0)):,}"
        ask_p = f"{float(q.get('askP', 0)):,.2f}"
        ask_q = f"{int(q.get('askQ', 0)):,}"
        lines.append(f"  {GREEN}{bid_q:>10}{RESET}  {GREEN}{bid_p:>12}{RESET}  "
                     f"{RED}{ask_p:>12}{RESET}  {RED}{ask_q:>10}{RESET}")

    return lines


def redraw(instruments: list[dict]):
    """Clear terminal and print instruments 2-wide."""
    with lock:
        store = dict(depth_store)

    print(CLEAR, end="")
    print(f"{BOLD}MCX Live Depth — top {len(instruments)} by volume{RESET}  {DIM}(Ctrl-C to stop){RESET}\n")

    cols = []
    for instr in instruments:
        key = instr["instrument_key"]
        sym = instr["trading_symbol"]
        if key in store:
            cols.append(render_depth(sym, store[key]))
        else:
            cols.append([f"{DIM}{sym} — waiting...{RESET}"])

    # Print in pairs (2 columns per row)
    for i in range(0, len(cols), 2):
        left  = cols[i]
        right = cols[i + 1] if i + 1 < len(cols) else []
        n = max(len(left), len(right))
        left  += [""] * (n - len(left))
        right += [""] * (n - len(right))
        for l_line, r_line in zip(left, right):
            if right:
                print(pad_to(l_line, COL_WIDTH) + f"  {DIM}│{RESET}  " + r_line)
            else:
                print(l_line)
        print()


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="MCX live 5-level depth for top commodities by volume")
    parser.add_argument("--token", required=True, help="Upstox access or analytics token")
    parser.add_argument("--top",   type=int, default=4, help="Number of instruments to subscribe (default: 4)")
    args = parser.parse_args()

    client = get_api_client(args.token)

    print(f"Discovering top {args.top} MCX commodities by volume...")
    instruments = find_top_mcx(client, args.top)
    if not instruments:
        print("No MCX futures found.")
        sys.exit(1)

    for instr in instruments:
        print(f"  → {instr['trading_symbol']}  ({instr['instrument_key']})")
    print("\nConnecting to WebSocket...\n")

    keys   = [i["instrument_key"] for i in instruments]
    key_to_instr = {i["instrument_key"]: i for i in instruments}

    streamer = upstox_client.MarketDataStreamerV3(client)

    def on_open():
        streamer.subscribe(keys, "full")
        print("Subscribed (full / 5-level). Waiting for data...\n")

    def on_message(msg):
        feeds = msg.get("feeds", {}) if isinstance(msg, dict) else {}
        if not feeds:
            return

        updated = False
        for key, feed in feeds.items():
            if key not in key_to_instr:
                continue
            full_feed = feed.get("fullFeed", {}) if isinstance(feed, dict) else {}
            market_ff = full_feed.get("marketFF", {}) if isinstance(full_feed, dict) else {}
            if not market_ff:
                continue
            with lock:
                depth_store[key] = market_ff
            updated = True

        if updated:
            redraw(instruments)

    def on_error(err):
        print(f"\n{RED}WebSocket error:{RESET} {err}")

    def on_close():
        print("\nWebSocket connection closed.")

    streamer.on("open",    on_open)
    streamer.on("message", on_message)
    streamer.on("error",   on_error)
    streamer.on("close",   on_close)

    streamer.connect()

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nStopping...")
        streamer.disconnect()


if __name__ == "__main__":
    main()
