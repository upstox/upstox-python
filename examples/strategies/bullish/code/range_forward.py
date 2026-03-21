"""
Strategy: Range Forward (Bullish)
Sells an OTM put (ATM-1) and buys an OTM call (ATM+1) for the next weekly expiry.
The premium collected from the sold put partially or fully finances the bought call.
Profits as Nifty rises; loses as Nifty falls below the put strike.
"""

from upstox_client import ApiClient, Configuration
from upstox_client import InstrumentsApi, OrderApiV3, PlaceOrderV3Request

# Replace with your access token
ACCESS_TOKEN = "your_access_token_here"

configuration = Configuration()
configuration.access_token = ACCESS_TOKEN

client = ApiClient(configuration)

try:
    instruments_api = InstrumentsApi(client)
    order_api = OrderApiV3(client)

    # Step 1: Find the OTM put (short leg)
    short_put = instruments_api.search_instrument(
        "Nifty 50", exchanges="NSE", segments="FO",
        instrument_types="PE", expiry="next_week", atm_offset=-1
    ).data[0]
    print(f"Short put  (ATM-1) - Trading symbol : {short_put['trading_symbol']}")
    print(f"Short put  (ATM-1) - Instrument key : {short_put['instrument_key']}")

    # Step 2: Find the OTM call (long leg)
    long_call = instruments_api.search_instrument(
        "Nifty 50", exchanges="NSE", segments="FO",
        instrument_types="CE", expiry="next_week", atm_offset=1
    ).data[0]
    print(f"Long call  (ATM+1) - Trading symbol : {long_call['trading_symbol']}")
    print(f"Long call  (ATM+1) - Instrument key : {long_call['instrument_key']}")

    # Step 3: Sell the OTM put
    response1 = order_api.place_order(PlaceOrderV3Request(
        instrument_token=short_put["instrument_key"],
        quantity=short_put["lot_size"],
        transaction_type="SELL",
        order_type="MARKET",
        product="D",
        validity="DAY",
        price=0,
        disclosed_quantity=0,
        trigger_price=0.0,
        market_protection=-1,
        is_amo=False,
    ))
    print(f"Short put order placed successfully. Order ID: {response1}")

    # Step 4: Buy the OTM call
    response2 = order_api.place_order(PlaceOrderV3Request(
        instrument_token=long_call["instrument_key"],
        quantity=long_call["lot_size"],
        transaction_type="BUY",
        order_type="MARKET",
        product="D",
        validity="DAY",
        price=0,
        disclosed_quantity=0,
        trigger_price=0.0,
        market_protection=-1,
        is_amo=False,
    ))
    print(f"Long call order placed successfully. Order ID: {response2}")

except Exception as e:
    print(f"API error: {e}")
