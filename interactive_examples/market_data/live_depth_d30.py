"""
Live Market Depth (30-level) — WebSocket streaming using MarketDataStreamerV3.

Requires Upstox Plus Pack (full_d30 subscription).

Subscribes two feeds in FULL_D30 mode (30-level bid/ask depth):
  • NIFTY near-month futures
  • RELIANCE equity

Displays both instruments side by side, updated live.
Runs until Ctrl-C (the test_runner aborts it after 5 seconds).

Usage:
  python market_data/live_depth_d30.py --token <TOKEN>
  python market_data/live_depth_d30.py --token <TOKEN> --future BANKNIFTY

For 5-level depth (no Plus Pack needed): use live_depth.py
"""

import argparse
import re
import sys
import os
import time
import threading

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import get_api_client, get_futures_sorted
import upstox_client

BOLD  = "\033[1m"
GREEN = "\033[32m"
RED   = "\033[31m"
CYAN  = "\033[36m"
DIM   = "\033[2m"
RESET = "\033[0m"
CLEAR = "\033[2J\033[H"

RELIANCE_KEY = "NSE_EQ|INE002A01018"

depth_store: dict = {}
lock = threading.Lock()

_ANSI = re.compile(r"\033\[[0-9;]*m")

def visible_len(s: str) -> int:
    return len(_ANSI.sub("", s))

def pad_to(s: str, width: int) -> str:
    return s + " " * max(0, width - visible_len(s))


# ── Depth rendering ───────────────────────────────────────────────────────────

COL_WIDTH = 60   # visible width of each instrument column (wider for level number)

def render_depth(symbol: str, market_ff: dict, max_levels: int = 30) -> list[str]:
    """Return a list of lines (no embedded newlines) for one instrument."""
    lines = [f"{BOLD}{CYAN}{symbol}{RESET}"]

    ltp = market_ff.get("ltpc", {}).get("ltp")
    lines.append(f"  LTP: {BOLD}{float(ltp):,.2f}{RESET}" if ltp else "  LTP: —")
    lines.append("")  # blank spacer

    quotes = market_ff.get("marketLevel", {}).get("bidAskQuote", [])
    if not quotes:
        lines.append("  (depth not available)")
        return lines

    lines.append(f"  {'#':>3}  {'Qty':>10}  {'Bid':>12}  {'Ask':>12}  {'Qty':>10}")
    lines.append("  " + "─" * 56)

    for i, q in enumerate(quotes[:max_levels]):
        bid_p = f"{float(q.get('bidP', 0)):,.2f}"
        bid_q = f"{int(q.get('bidQ', 0)):,}"
        ask_p = f"{float(q.get('askP', 0)):,.2f}"
        ask_q = f"{int(q.get('askQ', 0)):,}"
        lines.append(f"  {DIM}{i+1:>3}{RESET}  {GREEN}{bid_q:>10}{RESET}  {GREEN}{bid_p:>12}{RESET}  "
                     f"{RED}{ask_p:>12}{RESET}  {RED}{ask_q:>10}{RESET}")

    return lines


def redraw(symbols: list[str]):
    """Clear terminal and print both instruments side by side."""
    with lock:
        store = dict(depth_store)

    print(CLEAR, end="")
    print(f"{BOLD}Live Market Depth — 30 Level{RESET}  {DIM}(Plus Pack required · Ctrl-C to stop){RESET}\n")

    cols = []
    for sym in symbols:
        if sym in store:
            market_ff, levels = store[sym]
            cols.append(render_depth(sym, market_ff, levels))
        else:
            cols.append([f"{DIM}{sym} — waiting...{RESET}"])

    if len(cols) == 2:
        left, right = cols
        n = max(len(left), len(right))
        left  += [""] * (n - len(left))
        right += [""] * (n - len(right))
        for l, r in zip(left, right):
            print(pad_to(l, COL_WIDTH) + f"  {DIM}│{RESET}  " + r)
    else:
        for line in cols[0]:
            print(line)

    print()


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Live 30-level depth: NIFTY FUT + RELIANCE (full_d30, Plus Pack required)")
    parser.add_argument("--token",  required=True, help="Upstox access or analytics token")
    parser.add_argument("--future", default="NIFTY", help="Futures underlying (default: NIFTY)")
    args = parser.parse_args()

    client = get_api_client(args.token)

    print(f"Resolving {args.future} near-month futures...")
    futures = get_futures_sorted(client, args.future, exact_symbol=True)
    if not futures:
        print(f"No futures found for {args.future}.")
        sys.exit(1)
    nifty_fut_key = futures[0]["instrument_key"]
    nifty_sym     = futures[0]["trading_symbol"]
    print(f"  → {nifty_sym} ({nifty_fut_key})")
    print(f"  → RELIANCE ({RELIANCE_KEY})\n")
    print("Connecting to WebSocket...\n")

    symbols = [nifty_sym, "RELIANCE"]

    streamer = upstox_client.MarketDataStreamerV3(client)

    def on_open():
        streamer.subscribe([nifty_fut_key, RELIANCE_KEY], "full_d30")
        print("Subscribed (full_d30 / 30-level). Waiting for data...\n")

    def on_message(msg):
        feeds = msg.get("feeds", {}) if isinstance(msg, dict) else {}
        if not feeds:
            return

        updated = False
        for key, feed in feeds.items():
            full_feed = feed.get("fullFeed", {}) if isinstance(feed, dict) else {}
            market_ff = full_feed.get("marketFF", {}) if isinstance(full_feed, dict) else {}
            if not market_ff:
                continue
            symbol = nifty_sym if key == nifty_fut_key else "RELIANCE"
            with lock:
                depth_store[symbol] = (market_ff, 30)
            updated = True

        if updated:
            redraw(symbols)

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
