"""
Live Market Depth (5-level) — WebSocket streaming using MarketDataStreamerV3.

Layout:
  ┌─ Banner ────────────────────────────────────────────────┐
  │  SENSEX index  │  NIFTY 50 index  │  NIFTY BANK index  │
  └─────────────────────────────────────────────────────────┘
  ┌─ Grid ──────────────────────────────────────────────────┐
  │  NIFTY FUT (5-level depth)  │  SENSEX FUT (5-level)    │
  ├─────────────────────────────┼───────────────────────────┤
  │  RELIANCE NSE (5-level)     │  RELIANCE BSE (5-level)  │
  └─────────────────────────────────────────────────────────┘

Runs until Ctrl-C (the test_runner aborts it after 5 seconds).

Usage:
  python market_data/live_depth.py --token <TOKEN>

For 30-level depth (requires Plus Pack): use live_depth_d30.py
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
YELLOW= "\033[33m"
DIM   = "\033[2m"
RESET = "\033[0m"
CLEAR = "\033[2J\033[H"

SENSEX_IDX_KEY    = "BSE_INDEX|SENSEX"
NIFTY_IDX_KEY     = "NSE_INDEX|Nifty 50"
NIFTYBANK_IDX_KEY = "NSE_INDEX|Nifty Bank"
RELIANCE_NSE_KEY  = "NSE_EQ|INE002A01018"
RELIANCE_BSE_KEY  = "BSE_EQ|INE002A01018"

INDEX_KEYS = [SENSEX_IDX_KEY, NIFTY_IDX_KEY, NIFTYBANK_IDX_KEY]
INDEX_NAMES = {
    SENSEX_IDX_KEY:    "SENSEX",
    NIFTY_IDX_KEY:     "NIFTY 50",
    NIFTYBANK_IDX_KEY: "NIFTY BANK",
}

depth_store: dict = {}
lock = threading.Lock()

_ANSI = re.compile(r"\033\[[0-9;]*m")

def visible_len(s: str) -> int:
    return len(_ANSI.sub("", s))

def pad_to(s: str, width: int) -> str:
    return s + " " * max(0, width - visible_len(s))


# ── Rendering ─────────────────────────────────────────────────────────────────

COL_WIDTH    = 56
BANNER_WIDTH = 30   # per index in the banner


def render_banner_cell(name: str, index_ff: dict) -> list[str]:
    """Compact 3-line cell for one index in the banner."""
    ltpc = index_ff.get("ltpc", {})
    ltp  = ltpc.get("ltp")
    cp   = ltpc.get("cp")

    ltp_str = f"{float(ltp):>12,.2f}" if ltp else f"{'—':>12}"
    lines = [f"{BOLD}{CYAN}{name}{RESET}"]
    lines.append(f"  LTP: {BOLD}{ltp_str}{RESET}")
    if ltp and cp:
        chg = float(ltp) - float(cp)
        pct = chg / float(cp) * 100
        col = GREEN if chg >= 0 else RED
        lines.append(f"  Chg: {col}{chg:+,.2f} ({pct:+.2f}%){RESET}")
    else:
        lines.append("")
    return lines


def render_depth(symbol: str, market_ff: dict, max_levels: int = 5) -> list[str]:
    lines = [f"{BOLD}{CYAN}{symbol}{RESET}"]

    ltpc = market_ff.get("ltpc", {})
    ltp  = ltpc.get("ltp")
    cp   = ltpc.get("cp")
    lines.append(f"  LTP: {BOLD}{float(ltp):,.2f}{RESET}" if ltp else "  LTP: —")
    if ltp and cp:
        chg = float(ltp) - float(cp)
        pct = chg / float(cp) * 100
        col = GREEN if chg >= 0 else RED
        lines.append(f"  Chg: {col}{chg:+,.2f} ({pct:+.2f}%){RESET}")
    lines.append("")

    quotes = market_ff.get("marketLevel", {}).get("bidAskQuote", [])
    if not quotes:
        lines.append("  (depth not available)")
        return lines

    lines.append(f"  {'Qty':>10}  {'Bid':>12}  {'Ask':>12}  {'Qty':>10}")
    lines.append("  " + "─" * 50)

    for q in quotes[:max_levels]:
        bid_p = f"{float(q.get('bidP', 0)):,.2f}"
        bid_q = f"{int(q.get('bidQ', 0)):,}"
        ask_p = f"{float(q.get('askP', 0)):,.2f}"
        ask_q = f"{int(q.get('askQ', 0)):,}"
        lines.append(f"  {GREEN}{bid_q:>10}{RESET}  {GREEN}{bid_p:>12}{RESET}  "
                     f"{RED}{ask_p:>12}{RESET}  {RED}{ask_q:>10}{RESET}")

    return lines


def print_banner(store: dict):
    """Print the 3-index banner side by side."""
    cells = []
    for key in INDEX_KEYS:
        name  = INDEX_NAMES[key]
        entry = store.get(name)
        if entry:
            _, ff, _ = entry
            cells.append(render_banner_cell(name, ff))
        else:
            cells.append([f"{DIM}{name} — waiting...{RESET}", "", ""])

    # Pad all cells to same height
    n = max(len(c) for c in cells)
    for c in cells:
        c += [""] * (n - len(c))

    sep = f"  {DIM}│{RESET}  "
    bw  = BANNER_WIDTH
    for row in zip(*cells):
        print(pad_to(row[0], bw) + sep + pad_to(row[1], bw) + sep + row[2])
    print(DIM + "─" * (bw * 3 + 12) + RESET)


def redraw(grid: list[list[str]], store: dict):
    print(CLEAR, end="")
    print(f"{BOLD}Live Market  {RESET}{DIM}(Ctrl-C to stop){RESET}\n")

    print_banner(store)
    print()

    sep = DIM + "─" * (COL_WIDTH * 2 + 6) + RESET

    for row_idx, row in enumerate(grid):
        if row_idx > 0:
            print(sep)

        cols = []
        for sym in row:
            entry = store.get(sym)
            if entry is None:
                cols.append([f"{DIM}{sym} — waiting...{RESET}"])
            else:
                feed_type, ff_data, levels = entry
                cols.append(render_depth(sym, ff_data, levels))

        left, right = cols[0], cols[1]
        n = max(len(left), len(right))
        left  += [""] * (n - len(left))
        right += [""] * (n - len(right))
        for l, r in zip(left, right):
            print(pad_to(l, COL_WIDTH) + f"  {DIM}│{RESET}  " + r)

    print()


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Live depth 2×2 + index banner")
    parser.add_argument("--token", required=True)
    args = parser.parse_args()

    client = get_api_client(args.token)

    print("Resolving NIFTY near-month futures (NSE)...")
    nifty_futures = get_futures_sorted(client, "NIFTY", exchange="NSE", exact_symbol=True)
    if not nifty_futures:
        print("No NIFTY futures found."); sys.exit(1)
    nifty_key = nifty_futures[0]["instrument_key"]
    nifty_sym = nifty_futures[0]["trading_symbol"]
    print(f"  → {nifty_sym}")

    print("Resolving SENSEX near-month futures (BSE)...")
    sensex_futures = get_futures_sorted(client, "SENSEX", exchange="BSE", exact_symbol=True)
    if not sensex_futures:
        print("No SENSEX futures found."); sys.exit(1)
    sensex_key = sensex_futures[0]["instrument_key"]
    sensex_sym = sensex_futures[0]["trading_symbol"]
    print(f"  → {sensex_sym}\n")

    # key → (display_symbol, feed_type, levels)
    key_map = {
        nifty_key:         (nifty_sym,     "market", 5),
        sensex_key:        (sensex_sym,    "market", 5),
        RELIANCE_NSE_KEY:  ("RELIANCE NSE","market", 5),
        RELIANCE_BSE_KEY:  ("RELIANCE BSE","market", 5),
        SENSEX_IDX_KEY:    ("SENSEX",      "index",  0),
        NIFTY_IDX_KEY:     ("NIFTY 50",    "index",  0),
        NIFTYBANK_IDX_KEY: ("NIFTY BANK",  "index",  0),
    }

    grid = [
        [nifty_sym,      sensex_sym],
        ["RELIANCE NSE", "RELIANCE BSE"],
    ]

    all_keys = [
        nifty_key, sensex_key,
        RELIANCE_NSE_KEY, RELIANCE_BSE_KEY,
        SENSEX_IDX_KEY, NIFTY_IDX_KEY, NIFTYBANK_IDX_KEY,
    ]

    streamer = upstox_client.MarketDataStreamerV3(client)

    def on_open():
        streamer.subscribe(all_keys, "full")
        print("Subscribed. Waiting for data...\n")

    def on_message(msg):
        feeds = msg.get("feeds", {}) if isinstance(msg, dict) else {}
        if not feeds:
            return

        updated = False
        for key, feed in feeds.items():
            info = key_map.get(key)
            if not info:
                continue
            symbol, feed_type, levels = info
            full_feed = feed.get("fullFeed", {}) if isinstance(feed, dict) else {}
            if feed_type == "index":
                ff = full_feed.get("indexFF", {}) if isinstance(full_feed, dict) else {}
            else:
                ff = full_feed.get("marketFF", {}) if isinstance(full_feed, dict) else {}
            if not ff:
                continue
            with lock:
                depth_store[symbol] = (feed_type, ff, levels)
            updated = True

        if updated:
            with lock:
                store = dict(depth_store)
            redraw(grid, store)

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
