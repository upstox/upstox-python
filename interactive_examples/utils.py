"""
Shared helpers for all Upstox API examples.

All examples accept a --token argument (access token or analytics token).
Analytics tokens are 1-year, read-only tokens that skip the OAuth flow — ideal
for data pipelines and dashboards.
"""

import json
import sys
from datetime import date
import upstox_client
from upstox_client.rest import ApiException


def get_api_client(token: str) -> upstox_client.ApiClient:
    """Build an authenticated SDK client from an access or analytics token."""
    config = upstox_client.Configuration()
    config.access_token = token
    return upstox_client.ApiClient(config)


def parse_api_error(exc: ApiException):
    """
    Pull the useful bits out of an Upstox ApiException.

    The SDK raises ApiException with a JSON body like:
      {"status":"error","errors":[{"errorCode":"UDAPI100050",
                                    "message":"Invalid token used to access API"}]}

    Returns (status, error_code, message) — any of which may be None if the
    body could not be parsed.
    """
    status = getattr(exc, "status", None)
    code = message = None
    body = getattr(exc, "body", None)
    if body:
        try:
            errors = json.loads(body).get("errors") or []
            if errors:
                err = errors[0]
                code = err.get("errorCode") or err.get("error_code")
                message = err.get("message")
        except (ValueError, TypeError, AttributeError):
            pass
    return status, code, message


def is_invalid_token_error(exc: ApiException) -> bool:
    """True if the exception indicates an invalid/expired access token."""
    status, code, _ = parse_api_error(exc)
    return status == 401 or code == "UDAPI100050"


def check_token(api_client: upstox_client.ApiClient) -> None:
    """
    Verify the token by pinging a lightweight authenticated endpoint.

    Uses instrument search — the same call every example relies on, so it is
    guaranteed to be in-scope for both daily access and analytics tokens.
    Raises ApiException on failure (e.g. 401 for an invalid token).
    """
    upstox_client.InstrumentsApi(api_client).search_instrument("RELIANCE", records=1)


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
    segment: str = None,
):
    """
    Search for futures contracts and return them sorted by expiry (nearest first).

    If exact_symbol=True, only instruments whose underlying_symbol exactly
    matches *query* (case-insensitive) are returned — useful when searching
    'NIFTY' to avoid picking up NIFTYNXT50, BANKNIFTY, etc.

    The segment is derived from *exchange* when not given explicitly:
    MCX commodities (e.g. CRUDEOIL, NATURALGAS) use "COMM"; NSE/BSE equity
    futures use "FO". Pass segment explicitly to override (e.g. "CURR" for
    currency futures on NSE/BSE).

    Returns list of instrument dicts, each with keys like:
      instrument_key, trading_symbol, expiry, lot_size, underlying_symbol
    """
    if segment is None:
        segment = "COMM" if exchange.upper() == "MCX" else "FO"
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
