"""
Market News — latest news articles for one or more instruments.

Uses the Upstox News API. The default category `instrument_keys` fetches news
for specific instruments (resolved from --query); `positions`/`holdings` fetch
news for the account's current positions/holdings (require those to exist).

Usage:
  python market_data/market_news.py --token <TOKEN>
  python market_data/market_news.py --token <TOKEN> --query TCS
  python market_data/market_news.py --token <TOKEN> --category holdings
"""

import argparse
import sys
import os
import textwrap

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import get_api_client, resolve_equity, as_dict, die
import upstox_client

BOLD  = "\033[1m"
CYAN  = "\033[36m"
DIM   = "\033[2m"
RESET = "\033[0m"


def _fmt_time(v):
    """Format an epoch-millisecond timestamp as YYYY-MM-DD HH:MM (IST); passthrough otherwise."""
    if v in (None, ""):
        return ""
    try:
        from datetime import datetime, timezone, timedelta
        ist = timezone(timedelta(hours=5, minutes=30))
        return datetime.fromtimestamp(int(v) / 1000, tz=ist).strftime("%Y-%m-%d %H:%M")
    except (TypeError, ValueError):
        return str(v)


def main():
    parser = argparse.ArgumentParser(description="Market news via News API")
    parser.add_argument("--token", required=True, help="Upstox access or analytics token")
    parser.add_argument("--category", default="instrument_keys",
                        choices=("instrument_keys", "positions", "holdings"),
                        help="News category (default: instrument_keys)")
    parser.add_argument("--query", default="RELIANCE",
                        help="Symbol to resolve when category=instrument_keys (default: RELIANCE)")
    parser.add_argument("--page-size", type=int, default=10, help="Records per page (default: 10)")
    args = parser.parse_args()

    client = get_api_client(args.token)
    api = upstox_client.NewsApi(client)

    kwargs = {"page_number": 1, "page_size": args.page_size}
    if args.category == "instrument_keys":
        inst = resolve_equity(client, args.query)
        if not inst:
            die(f"No NSE equity instrument found for '{args.query}'.")
        kwargs["instrument_keys"] = inst.get("instrument_key", "")
        subject = args.query.upper()
    else:
        subject = args.category

    print(f"\n{BOLD}Fetching news{RESET} (category={args.category}, {subject})...\n")

    try:
        response = api.get_news(args.category, **kwargs)
    except Exception as e:
        die(f"API error: {e}")

    # The News API returns data either as a dict keyed by instrument_key
    # (each value a list of articles) or, for positions/holdings, a flat list.
    data = response.data
    articles = []
    if isinstance(data, dict):
        if isinstance(data.get("news"), list):
            articles = data["news"]
        else:
            for v in data.values():
                if isinstance(v, list):
                    articles.extend(v)
                elif isinstance(v, dict):
                    articles.append(v)
    elif isinstance(data, list):
        articles = data
    if not articles:
        die("No news articles returned.")

    for i, art in enumerate(articles, start=1):
        a = as_dict(art)
        headline = a.get("heading") or a.get("headline") or a.get("title") or "—"
        link     = a.get("article_link") or a.get("link") or ""
        when     = _fmt_time(a.get("published_time") or a.get("published_at") or a.get("timestamp"))
        print(f"  {CYAN}{i:>2}. {BOLD}{headline}{RESET}")
        if when:
            print(f"      {DIM}{when}{RESET}")
        summary = a.get("summary") or a.get("description") or ""
        if summary:
            for line in textwrap.wrap(str(summary), width=88)[:3]:
                print(f"      {line}")
        if link:
            print(f"      {DIM}{link}{RESET}")
        print()

    print(f"  {DIM}Articles: {len(articles)}{RESET}\n")


if __name__ == "__main__":
    main()
