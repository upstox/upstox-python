"""
Strategy: Strip
Buys one ATM call and two ATM puts at the same strike for the next weekly expiry.
Profits from a big move in either direction, but earns twice as much on a downward move.
A bearish-leaning volatility strategy.
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

    # Step 1: Find the ATM call
    atm_call = instruments_api.search_instrument(
        "Nifty 50", exchanges="NSE", segments="FO",
        instrument_types="CE", expiry="next_week", atm_offset=0
    ).data[0]
    print(f"ATM call - Trading symbol : {atm_call['trading_symbol']}")
    print(f"ATM call - Instrument key : {atm_call['instrument_key']}")

    # Step 2: Find the ATM put
    atm_put = instruments_api.search_instrument(
        "Nifty 50", exchanges="NSE", segments="FO",
        instrument_types="PE", expiry="next_week", atm_offset=0
    ).data[0]
    print(f"ATM put  - Trading symbol : {atm_put['trading_symbol']}")
    print(f"ATM put  - Instrument key : {atm_put['instrument_key']}")

    # Step 3: Buy 1x ATM call
    response1 = order_api.place_order(PlaceOrderV3Request(
        instrument_token=atm_call["instrument_key"],
        quantity=atm_call["lot_size"],
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
    print(f"ATM call order placed successfully. Order ID: {response1}")

    # Step 4: Buy 2x ATM put
    response2 = order_api.place_order(PlaceOrderV3Request(
        instrument_token=atm_put["instrument_key"],
        quantity=atm_put["lot_size"] * 2,
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
    print(f"ATM put order placed successfully. Order ID: {response2}")

except Exception as e:
    print(f"API error: {e}")
