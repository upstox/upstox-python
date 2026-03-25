"""
Strategy: Bear Butterfly (Bearish)
Buys an ATM put, sells two ATM-1 puts, and buys an ATM-2 put
for the next weekly expiry. Maximum profit is earned when Nifty closes
exactly at the middle strike (ATM-1) at expiry.
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

    # Step 1: Find all three strikes
    upper_long = instruments_api.search_instrument(
        "Nifty 50", exchanges="NSE", segments="FO",
        instrument_types="PE", expiry="next_week", atm_offset=0
    ).data[0]
    print(f"Upper long  (ATM)   - Trading symbol : {upper_long['trading_symbol']}")

    middle_short = instruments_api.search_instrument(
        "Nifty 50", exchanges="NSE", segments="FO",
        instrument_types="PE", expiry="next_week", atm_offset=-1
    ).data[0]
    print(f"Middle short (ATM-1) - Trading symbol : {middle_short['trading_symbol']}")

    lower_long = instruments_api.search_instrument(
        "Nifty 50", exchanges="NSE", segments="FO",
        instrument_types="PE", expiry="next_week", atm_offset=-2
    ).data[0]
    print(f"Lower long  (ATM-2) - Trading symbol : {lower_long['trading_symbol']}")

    # Step 2: Buy the upper put (ATM)
    response1 = order_api.place_order(PlaceOrderV3Request(
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
    print(f"Upper long put order placed successfully. Order ID: {response1}")

    # Step 3: Sell two middle puts (ATM-1)
    response2 = order_api.place_order(PlaceOrderV3Request(
        instrument_token=middle_short["instrument_key"],
        quantity=middle_short["lot_size"] * 2,
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
    print(f"Middle short put order placed successfully. Order ID: {response2}")

    # Step 4: Buy the lower put (ATM-2)
    response3 = order_api.place_order(PlaceOrderV3Request(
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
    print(f"Lower long put order placed successfully. Order ID: {response3}")

except Exception as e:
    print(f"API error: {e}")
