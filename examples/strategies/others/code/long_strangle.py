"""
Strategy: Long Strangle
Buys an OTM call (ATM+1) and an OTM put (ATM-1) for the next weekly expiry.
Profits when Nifty moves significantly in either direction beyond the bought strikes.
A cheaper alternative to the long straddle with a wider breakeven range.
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

    # Step 1: Find the OTM call (ATM+1)
    otm_call = instruments_api.search_instrument(
        "Nifty 50", exchanges="NSE", segments="FO",
        instrument_types="CE", expiry="next_week", atm_offset=1
    ).data[0]
    print(f"OTM call (ATM+1) - Trading symbol : {otm_call['trading_symbol']}")
    print(f"OTM call (ATM+1) - Instrument key : {otm_call['instrument_key']}")

    # Step 2: Find the OTM put (ATM-1)
    otm_put = instruments_api.search_instrument(
        "Nifty 50", exchanges="NSE", segments="FO",
        instrument_types="PE", expiry="next_week", atm_offset=-1
    ).data[0]
    print(f"OTM put  (ATM-1) - Trading symbol : {otm_put['trading_symbol']}")
    print(f"OTM put  (ATM-1) - Instrument key : {otm_put['instrument_key']}")

    # Step 3: Buy the OTM call
    response1 = order_api.place_order(PlaceOrderV3Request(
        instrument_token=otm_call["instrument_key"],
        quantity=otm_call["lot_size"],
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
    print(f"OTM call order placed successfully. Order ID: {response1}")

    # Step 4: Buy the OTM put
    response2 = order_api.place_order(PlaceOrderV3Request(
        instrument_token=otm_put["instrument_key"],
        quantity=otm_put["lot_size"],
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
    print(f"OTM put order placed successfully. Order ID: {response2}")

except Exception as e:
    print(f"API error: {e}")
