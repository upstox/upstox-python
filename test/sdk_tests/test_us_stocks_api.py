import upstox_client
import data_token
from upstox_client.rest import ApiException

# US stocks endpoints are only live on UAT for now; switch both hosts once they reach prod.
UAT_HOST = "https://uat-api.upstox.com"

configuration = upstox_client.Configuration()
configuration.access_token = getattr(data_token, "uat_access_token", data_token.access_token)
configuration.host = UAT_HOST
# place/modify/cancel paths are routed to order_host by ApiClient
configuration.order_host = UAT_HOST

api_client = upstox_client.ApiClient(configuration)

# Replace with a valid US instrument key before running
us_instrument_key = "{us_instrument_key}"

# ----------------------------------------------------------------------------
# UsMarketHolidaysAndTimingsApi
# ----------------------------------------------------------------------------
us_market_api = upstox_client.UsMarketHolidaysAndTimingsApi(api_client)

try:
    api_response = us_market_api.get_us_market_status()
    if api_response.status != "success":
        print("error in UsMarketHolidaysAndTimingsApi->get_us_market_status")
except ApiException as e:
    print("Exception when calling UsMarketHolidaysAndTimingsApi->get_us_market_status: %s\n" % e)

try:
    api_response = us_market_api.get_us_holidays()
    if api_response.status != "success":
        print("error in UsMarketHolidaysAndTimingsApi->get_us_holidays")
except ApiException as e:
    print("Exception when calling UsMarketHolidaysAndTimingsApi->get_us_holidays: %s\n" % e)

try:
    # Thanksgiving: expect one holiday entry
    api_response = us_market_api.get_us_holiday("2026-11-26")
    if api_response.status != "success":
        print("error in UsMarketHolidaysAndTimingsApi->get_us_holiday")
except ApiException as e:
    print("Exception when calling UsMarketHolidaysAndTimingsApi->get_us_holiday: %s\n" % e)

try:
    api_response = us_market_api.get_us_exchange_timings("2026-11-27")
    if api_response.status != "success":
        print("error in UsMarketHolidaysAndTimingsApi->get_us_exchange_timings")
except ApiException as e:
    print("Exception when calling UsMarketHolidaysAndTimingsApi->get_us_exchange_timings: %s\n" % e)

# ----------------------------------------------------------------------------
# UsStocksFundsApi / UsStocksPortfolioApi
# ----------------------------------------------------------------------------
try:
    api_response = upstox_client.UsStocksFundsApi(api_client).get_us_funds()
    if api_response.status != "success":
        print("error in UsStocksFundsApi->get_us_funds")
except ApiException as e:
    print("Exception when calling UsStocksFundsApi->get_us_funds: %s\n" % e)

try:
    api_response = upstox_client.UsStocksPortfolioApi(api_client).get_us_holdings()
    if api_response.status != "success":
        print("error in UsStocksPortfolioApi->get_us_holdings")
except ApiException as e:
    print("Exception when calling UsStocksPortfolioApi->get_us_holdings: %s\n" % e)

# ----------------------------------------------------------------------------
# UsStocksOrderApi (read-only) / UsStocksChargesApi
# ----------------------------------------------------------------------------
us_order_api = upstox_client.UsStocksOrderApi(api_client)

try:
    api_response = us_order_api.get_us_order_book()
    if api_response.status != "success":
        print("error in UsStocksOrderApi->get_us_order_book")
except ApiException as e:
    print("Exception when calling UsStocksOrderApi->get_us_order_book: %s\n" % e)

try:
    # In real usage, pass an order id from get_us_order_book
    api_response = us_order_api.get_us_order_details("sample-us-order-id")
    if api_response.status != "success":
        print("error in UsStocksOrderApi->get_us_order_details")
except ApiException as e:
    print("Exception when calling UsStocksOrderApi->get_us_order_details: %s\n" % e)

try:
    # Estimate charges for a market buy; nothing is placed
    body = upstox_client.UsOrderEstimateRequest(quantity=1, instrument_key=us_instrument_key, transaction_type="BUY", order_type="MARKET")
    api_response = us_order_api.estimate_us_order(body)
    if api_response.status != "success":
        print("error in UsStocksOrderApi->estimate_us_order")
except ApiException as e:
    print("Exception when calling UsStocksOrderApi->estimate_us_order: %s\n" % e)

try:
    # Estimate charges for a limit sell of a fractional quantity
    body = upstox_client.UsOrderEstimateRequest(quantity=0.5, price=150.0, instrument_key=us_instrument_key, transaction_type="SELL", order_type="LIMIT")
    api_response = us_order_api.estimate_us_order(body)
    if api_response.status != "success":
        print("error in UsStocksOrderApi->estimate_us_order with limit")
except ApiException as e:
    print("Exception when calling UsStocksOrderApi->estimate_us_order with limit: %s\n" % e)

try:
    # Margin check for multiple orders; nothing is placed
    body = upstox_client.UsMarginRequest(instruments=[
        upstox_client.UsOrderEstimateRequest(quantity=1, instrument_key=us_instrument_key, transaction_type="BUY", order_type="MARKET"),
        upstox_client.UsOrderEstimateRequest(quantity=2, price=100.0, instrument_key=us_instrument_key, transaction_type="BUY", order_type="LIMIT"),
    ])
    api_response = upstox_client.UsStocksChargesApi(api_client).calculate_us_margin(body)
    if api_response.status != "success":
        print("error in UsStocksChargesApi->calculate_us_margin")
except ApiException as e:
    print("Exception when calling UsStocksChargesApi->calculate_us_margin: %s\n" % e)

# place/modify/cancel create real US orders. Disabled by default; set
# RUN_DESTRUCTIVE_US_ORDER_TESTS = True to exercise them against a real account.
RUN_DESTRUCTIVE_US_ORDER_TESTS = False
if RUN_DESTRUCTIVE_US_ORDER_TESTS:
    try:
        # Place a limit buy far from market so it stays open
        body = upstox_client.UsPlaceOrderRequest(quantity=1, price=1.0, validity="DAY", tag="sdk-test", instrument_key=us_instrument_key, transaction_type="BUY", order_type="LIMIT")
        api_response = us_order_api.place_us_order(body)
        us_order_id = api_response.data.order_id

        # Modify replaces the order, so use the new order id afterwards
        modify_body = upstox_client.UsModifyOrderRequest(quantity=1, price=1.5, validity="DAY", order_id=us_order_id, instrument_key=us_instrument_key, transaction_type="BUY", order_type="LIMIT")
        api_response = us_order_api.modify_us_order(modify_body)
        us_order_id = api_response.data.order_id

        api_response = us_order_api.cancel_us_order(us_order_id)
        print("us order place/modify/cancel cycle:", api_response.status)
    except ApiException as e:
        print("Exception when calling UsStocksOrderApi order write ops: %s\n" % e)

# ----------------------------------------------------------------------------
# Model instantiation tests
# ----------------------------------------------------------------------------
us_place_order_request = upstox_client.UsPlaceOrderRequest(amount=25.0, validity="DAY", instrument_key="K", transaction_type="BUY", order_type="MARKET")
if us_place_order_request.amount != 25.0 or us_place_order_request.quantity is not None:
    print("error: UsPlaceOrderRequest fields not set correctly")

us_modify_order_request = upstox_client.UsModifyOrderRequest(quantity=2, price=10.5, validity="DAY", order_id="O1", instrument_key="K", transaction_type="SELL", order_type="LIMIT")
if us_modify_order_request.order_id != "O1" or us_modify_order_request.price != 10.5:
    print("error: UsModifyOrderRequest fields not set correctly")

us_order_estimate_request = upstox_client.UsOrderEstimateRequest(quantity=1.25, instrument_key="K", transaction_type="BUY", order_type="MARKET")
if us_order_estimate_request.quantity != 1.25:
    print("error: UsOrderEstimateRequest fields not set correctly")

us_margin_request = upstox_client.UsMarginRequest(instruments=[us_order_estimate_request])
if len(us_margin_request.instruments) != 1:
    print("error: UsMarginRequest fields not set correctly")

us_order_data = upstox_client.UsOrderData(order_id="O1")
us_order_response = upstox_client.UsOrderResponse(status="success", data=us_order_data)
if us_order_response.data.order_id != "O1":
    print("error: UsOrderResponse fields not set correctly")

us_order_estimate_data = upstox_client.UsOrderEstimateData(brokerage=1.0, gst=0.18, total_charges=1.5, estimated_total=101.5)
us_order_estimate_response = upstox_client.UsOrderEstimateResponse(status="success", data=us_order_estimate_data)
if us_order_estimate_response.data.estimated_total != 101.5:
    print("error: UsOrderEstimateResponse fields not set correctly")

us_order_book_data = upstox_client.UsOrderBookData(order_id="O1", status="open", quantity=1.5, fractionable=True, order_type="LIMIT", is_amo=False)
if us_order_book_data.status != "open" or not us_order_book_data.fractionable:
    print("error: UsOrderBookData fields not set correctly")

us_order_book_response = upstox_client.UsOrderBookResponse(status="success", data=[us_order_book_data])
if us_order_book_response.data[0].order_id != "O1":
    print("error: UsOrderBookResponse fields not set correctly")

us_order_details_response = upstox_client.UsOrderDetailsResponse(status="success", data=us_order_book_data)
if us_order_details_response.data.quantity != 1.5:
    print("error: UsOrderDetailsResponse fields not set correctly")

us_order_margin = upstox_client.UsOrderMargin(instrument_key="K", transaction_type="BUY", trade_value=100.0, required_margin=101.2)
us_margin_data = upstox_client.UsMarginData(margins=[us_order_margin], shortfall=0.0, sufficient=True, required_margin=101.2, available_to_invest=500.0)
us_margin_response = upstox_client.UsMarginResponse(status="success", data=us_margin_data)
if not us_margin_response.data.sufficient or us_margin_response.data.margins[0].required_margin != 101.2:
    print("error: UsMarginResponse fields not set correctly")

us_funds_data = upstox_client.UsFundsData(cash=100.0, available_to_trade=90.0, exchange_rate=88.5, cash_inr=8850.0)
us_funds_response = upstox_client.UsFundsResponse(status="success", data=us_funds_data)
if us_funds_response.data.exchange_rate != 88.5:
    print("error: UsFundsResponse fields not set correctly")

us_holding_data = upstox_client.UsHoldingData(instrument_key="K", trading_symbol="AAPL", quantity=2.5, average_price=150.0, pnl=12.5)
us_holdings_response = upstox_client.UsHoldingsResponse(status="success", data=[us_holding_data])
if us_holdings_response.data[0].quantity != 2.5:
    print("error: UsHoldingsResponse fields not set correctly")

us_holiday_data = upstox_client.UsHolidayData(_date="2026-11-26", description="Thanksgiving Day", holiday_type="TRADING_HOLIDAY")
get_us_holiday_response = upstox_client.GetUsHolidayResponse(status="success", data=[us_holiday_data])
if get_us_holiday_response.data[0]._date != "2026-11-26":
    print("error: GetUsHolidayResponse fields not set correctly")

us_exchange_timing_data = upstox_client.UsExchangeTimingData(exchange="US", start_time=1, end_time=2, overnight_start_time=3, overnight_end_time=4)
get_us_exchange_timing_response = upstox_client.GetUsExchangeTimingResponse(status="success", data=[us_exchange_timing_data])
if get_us_exchange_timing_response.data[0].overnight_end_time != 4:
    print("error: GetUsExchangeTimingResponse fields not set correctly")
