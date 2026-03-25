"""
Strategy: Buy Call (Bullish)
Buys an ATM Nifty 50 call option for the next weekly expiry.
"""

from upstox_client import ApiClient, Configuration
from upstox_client import InstrumentsApi, OrderApiV3, PlaceOrderV3Request

# Replace with your access token
ACCESS_TOKEN = "your_access_token_here"

configuration = Configuration()
configuration.access_token = ACCESS_TOKEN

client = ApiClient(configuration)

try:
    # Step 1: Find the ATM call option
    instrument = InstrumentsApi(client).search_instrument(
        "Nifty 50", exchanges="NSE", segments="FO",
        instrument_types="CE", expiry="next_week", atm_offset=0
    ).data[0]
    print(f"Trading symbol : {instrument['trading_symbol']}")
    print(f"Instrument key : {instrument['instrument_key']}")

    # Step 2: Place a buy order
    response = OrderApiV3(client).place_order(PlaceOrderV3Request(
        instrument_token=instrument["instrument_key"],
        quantity=instrument["lot_size"],
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
    print(f"Order placed successfully. Order ID: {response}")

except Exception as e:
    print(f"API error: {e}")
