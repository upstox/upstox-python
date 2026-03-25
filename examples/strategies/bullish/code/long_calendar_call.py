"""
Strategy: Long Calendar with Calls (Bullish)
Sells a current-week ATM call and buys a next-week ATM call at the same strike.
Profits from the faster time decay of the near-term option while retaining
upside exposure through the longer-dated call.
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

    # Step 1: Find the near-term ATM call (current week — short leg)
    near_call = instruments_api.search_instrument(
        "Nifty 50", exchanges="NSE", segments="FO",
        instrument_types="CE", expiry="current_week", atm_offset=0
    ).data[0]
    print(f"Near-term call (current week) - Trading symbol : {near_call['trading_symbol']}")
    print(f"Near-term call (current week) - Instrument key : {near_call['instrument_key']}")

    # Step 2: Find the far-term ATM call (next week — long leg)
    far_call = instruments_api.search_instrument(
        "Nifty 50", exchanges="NSE", segments="FO",
        instrument_types="CE", expiry="next_week", atm_offset=0
    ).data[0]
    print(f"Far-term call  (next week)    - Trading symbol : {far_call['trading_symbol']}")
    print(f"Far-term call  (next week)    - Instrument key : {far_call['instrument_key']}")

    # Step 3: Sell the near-term call
    response1 = order_api.place_order(PlaceOrderV3Request(
        instrument_token=near_call["instrument_key"],
        quantity=near_call["lot_size"],
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
    print(f"Near-term call order placed successfully. Order ID: {response1}")

    # Step 4: Buy the far-term call
    response2 = order_api.place_order(PlaceOrderV3Request(
        instrument_token=far_call["instrument_key"],
        quantity=far_call["lot_size"],
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
    print(f"Far-term call order placed successfully. Order ID: {response2}")

except Exception as e:
    print(f"API error: {e}")
