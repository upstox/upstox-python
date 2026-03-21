"""
Strategy: Batman (Neutral)
A double-butterfly strategy combining a call butterfly and a put butterfly around ATM.
Legs: BUY 1x ATM CE, SELL 2x ATM+1 CE, BUY 1x ATM+2 CE,
      BUY 1x ATM PE, SELL 2x ATM-1 PE, BUY 1x ATM-2 PE.
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

    # Step 1: Fetch all required instruments
    atm_call = instruments_api.search_instrument(
        "Nifty 50", exchanges="NSE", segments="FO",
        instrument_types="CE", expiry="next_week", atm_offset=0
    ).data[0]
    print(f"ATM call      - Trading symbol : {atm_call['trading_symbol']}")

    otm1_call = instruments_api.search_instrument(
        "Nifty 50", exchanges="NSE", segments="FO",
        instrument_types="CE", expiry="next_week", atm_offset=1
    ).data[0]
    print(f"ATM+1 call    - Trading symbol : {otm1_call['trading_symbol']}")

    otm2_call = instruments_api.search_instrument(
        "Nifty 50", exchanges="NSE", segments="FO",
        instrument_types="CE", expiry="next_week", atm_offset=2
    ).data[0]
    print(f"ATM+2 call    - Trading symbol : {otm2_call['trading_symbol']}")

    atm_put = instruments_api.search_instrument(
        "Nifty 50", exchanges="NSE", segments="FO",
        instrument_types="PE", expiry="next_week", atm_offset=0
    ).data[0]
    print(f"ATM put       - Trading symbol : {atm_put['trading_symbol']}")

    otm1_put = instruments_api.search_instrument(
        "Nifty 50", exchanges="NSE", segments="FO",
        instrument_types="PE", expiry="next_week", atm_offset=-1
    ).data[0]
    print(f"ATM-1 put     - Trading symbol : {otm1_put['trading_symbol']}")

    otm2_put = instruments_api.search_instrument(
        "Nifty 50", exchanges="NSE", segments="FO",
        instrument_types="PE", expiry="next_week", atm_offset=-2
    ).data[0]
    print(f"ATM-2 put     - Trading symbol : {otm2_put['trading_symbol']}")

    # Step 2: Place all legs
    # Leg 1: Buy ATM call (1x)
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

    # Leg 2: Sell ATM+1 call (2x)
    response2 = order_api.place_order(PlaceOrderV3Request(
        instrument_token=otm1_call["instrument_key"],
        quantity=otm1_call["lot_size"] * 2,
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
    print(f"ATM+1 call order placed successfully. Order ID: {response2}")

    # Leg 3: Buy ATM+2 call (1x)
    response3 = order_api.place_order(PlaceOrderV3Request(
        instrument_token=otm2_call["instrument_key"],
        quantity=otm2_call["lot_size"],
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
    print(f"ATM+2 call order placed successfully. Order ID: {response3}")

    # Leg 4: Buy ATM put (1x)
    response4 = order_api.place_order(PlaceOrderV3Request(
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
    print(f"ATM put order placed successfully. Order ID: {response4}")

    # Leg 5: Sell ATM-1 put (2x)
    response5 = order_api.place_order(PlaceOrderV3Request(
        instrument_token=otm1_put["instrument_key"],
        quantity=otm1_put["lot_size"] * 2,
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
    print(f"ATM-1 put order placed successfully. Order ID: {response5}")

    # Leg 6: Buy ATM-2 put (1x)
    response6 = order_api.place_order(PlaceOrderV3Request(
        instrument_token=otm2_put["instrument_key"],
        quantity=otm2_put["lot_size"],
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
    print(f"ATM-2 put order placed successfully. Order ID: {response6}")

except Exception as e:
    print(f"API error: {e}")
