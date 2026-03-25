"""
Intraday Candlestick Chart — rendered in the terminal using plotext.

Fetches today's intraday OHLC candles for any instrument and draws a
colour-coded candlestick chart directly in your terminal window.

Usage:
  python market_data/intraday_chart.py --token <TOKEN>
  python market_data/intraday_chart.py --token <TOKEN> --query NIFTY --exchange NSE --interval 5
  python market_data/intraday_chart.py --token <TOKEN> --query RELIANCE --interval 15
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import get_api_client, search_instrument
import upstox_client
import plotext as plt


# ── Instrument resolution ─────────────────────────────────────────────────────

INDEX_KEYS = {
    "SENSEX": "BSE_INDEX|SENSEX",
    "NIFTY 50": "NSE_INDEX|Nifty 50",
    "NIFTY": "NSE_INDEX|Nifty 50",
    "BANKNIFTY": "NSE_INDEX|Nifty Bank",
    "NIFTY BANK": "NSE_INDEX|Nifty Bank",
}


def resolve_instrument(client, query, exchange):
    """Return (instrument_key, display_name) for the query."""
    upper = query.upper()
    if upper in INDEX_KEYS:
        key = INDEX_KEYS[upper]
        return key, query.upper()

    # Search equity
    resp = search_instrument(client, query, exchanges=exchange, segments="EQ", records=5)
    hits = resp.data or []
    if not hits:
        print(f"No instrument found for '{query}' on {exchange}.")
        sys.exit(1)
    inst = hits[0]
    return inst["instrument_key"], inst.get("trading_symbol", query)


# ── Chart ─────────────────────────────────────────────────────────────────────

def draw_chart(candles, title, interval):
    """Draw a candlestick chart from candle list [[ts, o, h, l, c, v, oi], ...]."""
    if not candles:
        print("No intraday candles available yet (market may be closed or not yet open).")
        sys.exit(0)

    date_str = candles[0][0][:10]                    # "YYYY-MM-DD"
    times  = [c[0][11:16] for c in candles]         # "HH:MM" tick labels
    opens  = [float(c[1]) for c in candles]
    highs  = [float(c[2]) for c in candles]
    lows   = [float(c[3]) for c in candles]
    closes = [float(c[4]) for c in candles]
    vols   = [int(c[5])   for c in candles]

    x    = list(range(len(candles)))
    step = max(1, len(x) // 10)
    has_volume = any(v > 0 for v in vols)

    ohlc = {"Open": opens, "High": highs, "Low": lows, "Close": closes}

    plt.clf()

    if has_volume:
        plt.subplots(2, 1)

    # ── Price panel — numeric x so plotext won't shift times ──
    plt.subplot(1, 1) if has_volume else None
    plt.title(f"{title}  |  {interval}-min intraday candles  ({date_str})")
    plt.candlestick(x, ohlc)          # numeric x, no date_form
    plt.xticks(x[::step], times[::step])
    plt.ylabel("Price")
    plt.theme("dark")

    # ── Volume panel (skipped for indices with no volume) ──
    if has_volume:
        bull_x = [i for i in x if closes[i] >= opens[i]]
        bull_v = [vols[i] for i in bull_x]
        bear_x = [i for i in x if closes[i] <  opens[i]]
        bear_v = [vols[i] for i in bear_x]
        plt.subplot(2, 1)
        if bull_x:
            plt.bar(bull_x, bull_v, color="green")
        if bear_x:
            plt.bar(bear_x, bear_v, color="red")
        plt.xticks(x[::step], times[::step])
        plt.ylabel("Volume")
        plt.theme("dark")

    plt.show()

    # Summary line
    day_open  = opens[0]
    day_close = closes[-1]
    day_high  = max(highs)
    day_low   = min(lows)
    chg       = day_close - day_open
    chg_pct   = (chg / day_open) * 100 if day_open else 0
    sign      = "▲" if chg >= 0 else "▼"
    print(f"\n  Open {day_open:,.2f}  High {day_high:,.2f}  Low {day_low:,.2f}  "
          f"Close {day_close:,.2f}  {sign} {chg:+.2f} ({chg_pct:+.2f}%)")
    print(f"  Candles: {len(candles)}  |  Interval: {interval} min  |  Date: {date_str}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Intraday candlestick chart in the terminal")
    parser.add_argument("--token",    required=True, help="Upstox access or analytics token")
    parser.add_argument("--query",    default="SENSEX", help="Instrument name (default: SENSEX)")
    parser.add_argument("--exchange", default="BSE",    help="Exchange: NSE or BSE (default: BSE)")
    parser.add_argument("--interval", type=int, default=5,
                        help="Candle interval in minutes: 1, 3, 5, 10, 15, 30 (default: 5)")
    args = parser.parse_args()

    client = get_api_client(args.token)
    instrument_key, display_name = resolve_instrument(client, args.query, args.exchange)

    print(f"Fetching {args.interval}-min intraday candles for {display_name} ({instrument_key})...\n")

    api = upstox_client.HistoryV3Api(client)
    resp = api.get_intra_day_candle_data(instrument_key, "minutes", args.interval)
    candles = resp.data.candles if resp.data else []
    # API returns newest-first; reverse for chronological order
    candles = list(reversed(candles))

    draw_chart(candles, display_name, args.interval)


if __name__ == "__main__":
    main()
