"""
Strategy: Call Ratio Spread
Buys one ATM call and sells two OTM calls (ATM+1) for the next weekly expiry.
Profits when Nifty rises moderately to the short strike. Can be entered at
low cost or even a net credit.
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

    # Step 1: Find the ATM call (long leg)
    long_call = instruments_api.search_instrument(
        "Nifty 50", exchanges="NSE", segments="FO",
        instrument_types="CE", expiry="next_week", atm_offset=0
    ).data[0]
    print(f"Long call  (ATM)   - Trading symbol : {long_call['trading_symbol']}")

    # Step 2: Find the OTM call (short leg — 2x quantity)
    short_call = instruments_api.search_instrument(
        "Nifty 50", exchanges="NSE", segments="FO",
        instrument_types="CE", expiry="next_week", atm_offset=1
    ).data[0]
    print(f"Short call (ATM+1) - Trading symbol : {short_call['trading_symbol']}")

    # Step 3: Buy 1x ATM call
    response1 = order_api.place_order(PlaceOrderV3Request(
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
    print(f"Long call order placed successfully. Order ID: {response1}")

    # Step 4: Sell 2x OTM call
    response2 = order_api.place_order(PlaceOrderV3Request(
        instrument_token=short_call["instrument_key"],
        quantity=short_call["lot_size"] * 2,
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
    print(f"Short call order placed successfully. Order ID: {response2}")

except Exception as e:
    print(f"API error: {e}")
