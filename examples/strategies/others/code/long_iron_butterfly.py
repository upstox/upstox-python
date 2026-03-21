"""
Strategy: Long Iron Butterfly
Buys an ATM call and put, and sells an OTM call (ATM+2) and OTM put (ATM-2)
as wings for the next weekly expiry. Profits when Nifty moves significantly
away from the ATM strike in either direction.
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
    atm_call = instruments_api.search_instrument(
        "Nifty 50", exchanges="NSE", segments="FO",
        instrument_types="CE", expiry="next_week", atm_offset=0
    ).data[0]
    print(f"ATM call        - Trading symbol : {atm_call['trading_symbol']}")

    atm_put = instruments_api.search_instrument(
        "Nifty 50", exchanges="NSE", segments="FO",
        instrument_types="PE", expiry="next_week", atm_offset=0
    ).data[0]
    print(f"ATM put         - Trading symbol : {atm_put['trading_symbol']}")

    upper_wing_call = instruments_api.search_instrument(
        "Nifty 50", exchanges="NSE", segments="FO",
        instrument_types="CE", expiry="next_week", atm_offset=2
    ).data[0]
    print(f"Upper wing call (ATM+2) - Trading symbol : {upper_wing_call['trading_symbol']}")

    lower_wing_put = instruments_api.search_instrument(
        "Nifty 50", exchanges="NSE", segments="FO",
        instrument_types="PE", expiry="next_week", atm_offset=-2
    ).data[0]
    print(f"Lower wing put  (ATM-2) - Trading symbol : {lower_wing_put['trading_symbol']}")

    # Step 2: Buy the ATM call
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

    # Step 3: Buy the ATM put
    response2 = order_api.place_order(PlaceOrderV3Request(
        instrument_token=atm_put["instrument_key"],
        quantity=atm_put["lot_size"],
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

    # Step 4: Sell the upper wing call (ATM+2)
    response3 = order_api.place_order(PlaceOrderV3Request(
        instrument_token=upper_wing_call["instrument_key"],
        quantity=upper_wing_call["lot_size"],
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
    print(f"Upper wing call order placed successfully. Order ID: {response3}")

    # Step 5: Sell the lower wing put (ATM-2)
    response4 = order_api.place_order(PlaceOrderV3Request(
        instrument_token=lower_wing_put["instrument_key"],
        quantity=lower_wing_put["lot_size"],
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
    print(f"Lower wing put order placed successfully. Order ID: {response4}")

except Exception as e:
    print(f"API error: {e}")
