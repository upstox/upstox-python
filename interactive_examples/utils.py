"""
Shared helpers for all Upstox API examples.

All examples accept a --token argument (access token or analytics token).
Analytics tokens are 1-year, read-only tokens that skip the OAuth flow — ideal
for data pipelines and dashboards.
"""

import sys
from datetime import date
import upstox_client


def get_api_client(token: str) -> upstox_client.ApiClient:
    """Build an authenticated SDK client from an access or analytics token."""
    config = upstox_client.Configuration()
    config.access_token = token
    return upstox_client.ApiClient(config)


def search_instrument(api_client: upstox_client.ApiClient, query: str, **kwargs):
    """
    Search instruments by name/keyword.

    Common kwargs:
      exchanges        - comma-separated: NSE, BSE, MCX  (default ALL)
      segments         - comma-separated: EQ, FO, CURR, COMM, INDEX  (default ALL)
      instrument_types - comma-separated: CE, PE, FUT, EQ, INDEX
      expiry           - 'current_week', 'current_month', or 'yyyy-MM-dd'
      atm_offset       - int, 0=ATM, +1=one strike above, -1=one below
      page_number      - int, starts at 1
      records          - int, max 30 per page

    Returns the SearchInstrumentResponse (response.data is a list of dicts).
    """
    api = upstox_client.InstrumentsApi(api_client)
    return api.search_instrument(query, **kwargs)


def _rekey_by_instrument_token(data: dict) -> dict:
    """
    The market-quote APIs return data keyed as 'EXCHANGE:SYMBOL'
    (e.g. 'NSE_EQ:RELIANCE') but callers always use 'EXCHANGE|ISIN'
    (e.g. 'NSE_EQ|INE002A01018').  Re-key by the instrument_token field
    that lives inside each entry so lookups work with the original key.
    """
    if not data:
        return {}
    result = {}
    for entry in data.values():
        # entry is either a dict or a model object
        token = entry.get("instrument_token") if isinstance(entry, dict) else getattr(entry, "instrument_token", None)
        if token:
            result[token] = entry
    return result


def get_ltp(api_client: upstox_client.ApiClient, *instrument_keys: str):
    """
    Fetch last traded price for one or more instruments (up to 500).

    Returns dict keyed by instrument_key (e.g. 'NSE_EQ|INE002A01018'),
    each value is a dict/object with last_price, volume, cp, ltq fields.
    """
    api = upstox_client.MarketQuoteV3Api(api_client)
    response = api.get_ltp(instrument_key=",".join(instrument_keys))
    return _rekey_by_instrument_token(response.data)


def get_full_quote(api_client: upstox_client.ApiClient, *instrument_keys: str):
    """
    Fetch full market quote for one or more instruments.

    Returns dict keyed by instrument_key (e.g. 'NSE_EQ|INE002A01018'),
    each value is a dict/object with last_price, ohlc, oi, volume,
    net_change, total_buy_quantity, total_sell_quantity.
    """
    api = upstox_client.MarketQuoteApi(api_client)
    response = api.get_full_market_quote(",".join(instrument_keys), "2.0")
    return _rekey_by_instrument_token(response.data)


def get_historical_candles(
    api_client: upstox_client.ApiClient,
    instrument_key: str,
    unit: str,
    interval: int,
    to_date: str,
    from_date: str = None,
):
    """
    Fetch historical OHLC candles.

    unit     - 'minutes', 'hours', 'days', 'weeks', 'months'
    interval - numeric interval (e.g. 1, 5, 15, 30)
    to_date  - 'yyyy-MM-dd'
    from_date- 'yyyy-MM-dd' (optional, uses get_historical_candle_data1)

    Returns list of candles, each candle is:
      [timestamp, open, high, low, close, volume, oi]
    """
    api = upstox_client.HistoryV3Api(api_client)
    if from_date:
        response = api.get_historical_candle_data1(
            instrument_key, unit, interval, to_date, from_date
        )
    else:
        response = api.get_historical_candle_data(
            instrument_key, unit, interval, to_date
        )
    return response.data.candles  # list[list[object]]


def get_futures_sorted(
    api_client: upstox_client.ApiClient,
    query: str,
    exchange: str = "NSE",
    exact_symbol: bool = False,
    segment: str = "FO",
):
    """
    Search for futures contracts and return them sorted by expiry (nearest first).

    If exact_symbol=True, only instruments whose underlying_symbol exactly
    matches *query* (case-insensitive) are returned — useful when searching
    'NIFTY' to avoid picking up NIFTYNXT50, BANKNIFTY, etc.

    Use segment="COMM" for MCX commodity futures (e.g. CRUDEOIL, NATURALGAS).
    Use segment="FO" (default) for NSE/BSE equity futures.

    Returns list of instrument dicts, each with keys like:
      instrument_key, trading_symbol, expiry, lot_size, underlying_symbol
    """
    response = search_instrument(
        api_client,
        query,
        exchanges=exchange,
        segments=segment,
        instrument_types="FUT",
        records=30,
    )
    instruments = response.data or []
    if exact_symbol:
        instruments = [
            inst for inst in instruments
            if inst.get("underlying_symbol", "").upper() == query.upper()
        ]
    # Sort by expiry date string (yyyy-MM-dd sorts lexicographically)
    return sorted(instruments, key=lambda x: x.get("expiry", ""))


def today_str() -> str:
    return date.today().isoformat()


def die(msg: str):
    print(f"Error: {msg}", file=sys.stderr)
    sys.exit(1)
