"""
Strategy: Bull Condor (Bullish)
Buys an ATM call, sells ATM+1 and ATM+2 calls, and buys an ATM+3 call
for the next weekly expiry. Profits when Nifty rises moderately into the
middle zone between the two short strikes.
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

    # Step 1: Find all four strikes
    lower_long = instruments_api.search_instrument(
        "Nifty 50", exchanges="NSE", segments="FO",
        instrument_types="CE", expiry="next_week", atm_offset=0
    ).data[0]
    print(f"Lower long  (ATM)   - Trading symbol : {lower_long['trading_symbol']}")

    lower_short = instruments_api.search_instrument(
        "Nifty 50", exchanges="NSE", segments="FO",
        instrument_types="CE", expiry="next_week", atm_offset=1
    ).data[0]
    print(f"Lower short (ATM+1) - Trading symbol : {lower_short['trading_symbol']}")

    upper_short = instruments_api.search_instrument(
        "Nifty 50", exchanges="NSE", segments="FO",
        instrument_types="CE", expiry="next_week", atm_offset=2
    ).data[0]
    print(f"Upper short (ATM+2) - Trading symbol : {upper_short['trading_symbol']}")

    upper_long = instruments_api.search_instrument(
        "Nifty 50", exchanges="NSE", segments="FO",
        instrument_types="CE", expiry="next_week", atm_offset=3
    ).data[0]
    print(f"Upper long  (ATM+3) - Trading symbol : {upper_long['trading_symbol']}")

    # Step 2: Buy the lower long call (ATM)
    response1 = order_api.place_order(PlaceOrderV3Request(
        instrument_token=lower_long["instrument_key"],
        quantity=lower_long["lot_size"],
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
    print(f"Lower long call order placed successfully. Order ID: {response1}")

    # Step 3: Sell the lower short call (ATM+1)
    response2 = order_api.place_order(PlaceOrderV3Request(
        instrument_token=lower_short["instrument_key"],
        quantity=lower_short["lot_size"],
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
    print(f"Lower short call order placed successfully. Order ID: {response2}")

    # Step 4: Sell the upper short call (ATM+2)
    response3 = order_api.place_order(PlaceOrderV3Request(
        instrument_token=upper_short["instrument_key"],
        quantity=upper_short["lot_size"],
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
    print(f"Upper short call order placed successfully. Order ID: {response3}")

    # Step 5: Buy the upper long call (ATM+3)
    response4 = order_api.place_order(PlaceOrderV3Request(
        instrument_token=upper_long["instrument_key"],
        quantity=upper_long["lot_size"],
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
    print(f"Upper long call order placed successfully. Order ID: {response4}")

except Exception as e:
    print(f"API error: {e}")
