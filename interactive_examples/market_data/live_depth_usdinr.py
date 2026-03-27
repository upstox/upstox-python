"""
USDINR Live Depth (5-level) — WebSocket streaming using MarketDataStreamerV3.

Resolves the near-month USDINR futures contract from both NSE (CDS) and BSE (BCD),
then subscribes both in FULL mode (5-level depth) and displays them side by side.

Runs until Ctrl-C (the test_runner aborts it after 5 seconds).

Usage:
  python market_data/live_depth_usdinr.py --token <TOKEN>
"""

import argparse
import re
import sys
import os
import time
import threading

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import get_api_client, search_instrument
import upstox_client

BOLD  = "\033[1m"
GREEN = "\033[32m"
RED   = "\033[31m"
CYAN  = "\033[36m"
DIM   = "\033[2m"
RESET = "\033[0m"
CLEAR = "\033[2J\033[H"

depth_store: dict = {}
lock = threading.Lock()

_ANSI = re.compile(r"\033\[[0-9;]*m")


def visible_len(s: str) -> int:
    return len(_ANSI.sub("", s))


def pad_to(s: str, width: int) -> str:
    return s + " " * max(0, width - visible_len(s))


# ── Instrument discovery ───────────────────────────────────────────────────────

def find_usdinr(client, exchange: str):
    """Return the nearest-expiry USDINR future for the given exchange (CDS or BCD)."""
    resp = search_instrument(
        client, "USDINR",
        exchanges="NSE" if exchange == "CDS" else "BSE",
        segments="CURR",
        instrument_types="FUT",
        records=10,
    )
    instruments = resp.data or []
    # Filter to exact USDINR symbol (not USDINR derivatives like options)
    futures = [i for i in instruments
               if isinstance(i, dict) and "USDINR" in i.get("trading_symbol", "").upper()]
    if not futures:
        return None
    # Sort by expiry (nearest first)
    futures.sort(key=lambda x: x.get("expiry", ""))
    return futures[0]


# ── Depth rendering ────────────────────────────────────────────────────────────

COL_WIDTH = 58


def render_depth(label: str, market_ff: dict) -> list[str]:
    lines = [f"{BOLD}{CYAN}{label}{RESET}"]

    ltp = market_ff.get("ltpc", {}).get("ltp")
    lines.append(f"  LTP: {BOLD}{float(ltp):,.4f}{RESET}" if ltp else "  LTP: —")
    lines.append("")

    quotes = market_ff.get("marketLevel", {}).get("bidAskQuote", [])
    if not quotes:
        lines.append("  (depth not available)")
        return lines

    lines.append(f"  {'Qty':>10}  {'Bid':>12}  {'Ask':>12}  {'Qty':>10}")
    lines.append("  " + "─" * 50)

    for q in quotes[:5]:
        bid_p = f"{float(q.get('bidP', 0)):,.4f}"
        bid_q = f"{int(q.get('bidQ', 0)):,}"
        ask_p = f"{float(q.get('askP', 0)):,.4f}"
        ask_q = f"{int(q.get('askQ', 0)):,}"
        lines.append(f"  {GREEN}{bid_q:>10}{RESET}  {GREEN}{bid_p:>12}{RESET}  "
                     f"{RED}{ask_p:>12}{RESET}  {RED}{ask_q:>10}{RESET}")

    return lines


def redraw(nse_instr: dict, bse_instr: dict):
    with lock:
        store = dict(depth_store)

    print(CLEAR, end="")
    print(f"{BOLD}USDINR Near-Month Futures — NSE (CDS) vs BSE (BCD){RESET}  {DIM}(Ctrl-C to stop){RESET}\n")

    nse_key = nse_instr["instrument_key"]
    bse_key = bse_instr["instrument_key"]

    left  = render_depth(f"NSE  {nse_instr['trading_symbol']}", store[nse_key]) if nse_key in store else [f"{DIM}NSE — waiting...{RESET}"]
    right = render_depth(f"BSE  {bse_instr['trading_symbol']}", store[bse_key]) if bse_key in store else [f"{DIM}BSE — waiting...{RESET}"]

    n = max(len(left), len(right))
    left  += [""] * (n - len(left))
    right += [""] * (n - len(right))

    for l_line, r_line in zip(left, right):
        print(pad_to(l_line, COL_WIDTH) + f"  {DIM}│{RESET}  " + r_line)
    print()


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="USDINR near-month futures depth: NSE CDS vs BSE BCD")
    parser.add_argument("--token", required=True, help="Upstox access or analytics token")
    args = parser.parse_args()

    client = get_api_client(args.token)

    print("Resolving USDINR near-month futures...")
    nse_instr = find_usdinr(client, "CDS")
    bse_instr = find_usdinr(client, "BCD")

    if not nse_instr:
        print("Could not find USDINR futures on NSE (CDS).")
        sys.exit(1)
    if not bse_instr:
        print("Could not find USDINR futures on BSE (BCD).")
        sys.exit(1)

    print(f"  → NSE: {nse_instr['trading_symbol']}  ({nse_instr['instrument_key']})")
    print(f"  → BSE: {bse_instr['trading_symbol']}  ({bse_instr['instrument_key']})")
    print("\nConnecting to WebSocket...\n")

    nse_key = nse_instr["instrument_key"]
    bse_key = bse_instr["instrument_key"]

    streamer = upstox_client.MarketDataStreamerV3(client)

    def on_open():
        streamer.subscribe([nse_key, bse_key], "full")
        print("Subscribed (full / 5-level). Waiting for data...\n")

    def on_message(msg):
        feeds = msg.get("feeds", {}) if isinstance(msg, dict) else {}
        if not feeds:
            return

        updated = False
        for key, feed in feeds.items():
            if key not in (nse_key, bse_key):
                continue
            full_feed = feed.get("fullFeed", {}) if isinstance(feed, dict) else {}
            market_ff = full_feed.get("marketFF", {}) if isinstance(full_feed, dict) else {}
            if not market_ff:
                continue
            with lock:
                depth_store[key] = market_ff
            updated = True

        if updated:
            redraw(nse_instr, bse_instr)

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
