"""
Strategy: Put Ratio Spread
Buys one ATM put and sells two OTM puts (ATM-1) for the next weekly expiry.
Profits when Nifty falls moderately to the short strike. Can be entered at
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

    # Step 1: Find the ATM put (long leg)
    long_put = instruments_api.search_instrument(
        "Nifty 50", exchanges="NSE", segments="FO",
        instrument_types="PE", expiry="next_week", atm_offset=0
    ).data[0]
    print(f"Long put  (ATM)   - Trading symbol : {long_put['trading_symbol']}")

    # Step 2: Find the OTM put (short leg — 2x quantity)
    short_put = instruments_api.search_instrument(
        "Nifty 50", exchanges="NSE", segments="FO",
        instrument_types="PE", expiry="next_week", atm_offset=-1
    ).data[0]
    print(f"Short put (ATM-1) - Trading symbol : {short_put['trading_symbol']}")

    # Step 3: Buy 1x ATM put
    response1 = order_api.place_order(PlaceOrderV3Request(
        instrument_token=long_put["instrument_key"],
        quantity=long_put["lot_size"],
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
    print(f"Long put order placed successfully. Order ID: {response1}")

    # Step 4: Sell 2x OTM put
    response2 = order_api.place_order(PlaceOrderV3Request(
        instrument_token=short_put["instrument_key"],
        quantity=short_put["lot_size"] * 2,
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
    print(f"Short put order placed successfully. Order ID: {response2}")

except Exception as e:
    print(f"API error: {e}")
