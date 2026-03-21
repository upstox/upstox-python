"""
Strategy: Long Synthetic Future (Bullish)
Buys an ATM call and sells an ATM put at the same strike for the next weekly expiry.
Replicates the payoff of a long futures position using options.
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

    # Step 1: Find the ATM call option (long leg)
    atm_call = instruments_api.search_instrument(
        "Nifty 50", exchanges="NSE", segments="FO",
        instrument_types="CE", expiry="next_week", atm_offset=0
    ).data[0]
    print(f"ATM call - Trading symbol : {atm_call['trading_symbol']}")
    print(f"ATM call - Instrument key : {atm_call['instrument_key']}")

    # Step 2: Find the ATM put option (short leg)
    atm_put = instruments_api.search_instrument(
        "Nifty 50", exchanges="NSE", segments="FO",
        instrument_types="PE", expiry="next_week", atm_offset=0
    ).data[0]
    print(f"ATM put  - Trading symbol : {atm_put['trading_symbol']}")
    print(f"ATM put  - Instrument key : {atm_put['instrument_key']}")

    # Step 3: Buy the ATM call
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

    # Step 4: Sell the ATM put
    response2 = order_api.place_order(PlaceOrderV3Request(
        instrument_token=atm_put["instrument_key"],
        quantity=atm_put["lot_size"],
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
    print(f"ATM put order placed successfully. Order ID: {response2}")

except Exception as e:
    print(f"API error: {e}")
