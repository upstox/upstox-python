"""
Strategy: Short Iron Condor (Neutral)
Sells an OTM call (ATM+1) and an OTM put (ATM-1), and buys a further OTM
call (ATM+2) and put (ATM-2) as wings for the next weekly expiry.
Profits when Nifty stays between the two short strikes.
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

    # Step 1: Find all four legs
    short_call = instruments_api.search_instrument(
        "Nifty 50", exchanges="NSE", segments="FO",
        instrument_types="CE", expiry="next_week", atm_offset=1
    ).data[0]
    print(f"Short call  (ATM+1) - Trading symbol : {short_call['trading_symbol']}")

    long_call = instruments_api.search_instrument(
        "Nifty 50", exchanges="NSE", segments="FO",
        instrument_types="CE", expiry="next_week", atm_offset=2
    ).data[0]
    print(f"Long call   (ATM+2) - Trading symbol : {long_call['trading_symbol']}")

    short_put = instruments_api.search_instrument(
        "Nifty 50", exchanges="NSE", segments="FO",
        instrument_types="PE", expiry="next_week", atm_offset=-1
    ).data[0]
    print(f"Short put   (ATM-1) - Trading symbol : {short_put['trading_symbol']}")

    long_put = instruments_api.search_instrument(
        "Nifty 50", exchanges="NSE", segments="FO",
        instrument_types="PE", expiry="next_week", atm_offset=-2
    ).data[0]
    print(f"Long put    (ATM-2) - Trading symbol : {long_put['trading_symbol']}")

    # Step 2: Sell the OTM call (ATM+1)
    response1 = order_api.place_order(PlaceOrderV3Request(
        instrument_token=short_call["instrument_key"],
        quantity=short_call["lot_size"],
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
    print(f"Short call order placed successfully. Order ID: {response1}")

    # Step 3: Buy the further OTM call wing (ATM+2)
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

    # Step 4: Sell the OTM put (ATM-1)
    response3 = order_api.place_order(PlaceOrderV3Request(
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
    print(f"Short put order placed successfully. Order ID: {response3}")

    # Step 5: Buy the further OTM put wing (ATM-2)
    response4 = order_api.place_order(PlaceOrderV3Request(
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
    print(f"Long put order placed successfully. Order ID: {response4}")

except Exception as e:
    print(f"API error: {e}")
