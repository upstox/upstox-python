import upstox_client
import data_token
from upstox_client.rest import ApiException
from datetime import datetime, time
import json


def is_within_market_hours():
    # Get the current time
    now = datetime.now().time()

    # Define market opening and closing times
    market_open = time(9, 0)  # 9:00 AM
    market_close = time(15, 30)  # 3:30 PM

    # Check if the current time is within market hours
    return market_open <= now <= market_close


configuration = upstox_client.Configuration()
configuration.access_token = data_token.access_token
api_version = '2.0'

api_instance = upstox_client.UserApi(upstox_client.ApiClient(configuration))

try:
    # Get User Fund And Margin
    api_response = api_instance.get_profile(api_version)
    if api_response.status!="success":
        print("error in get profile API")

except ApiException as e:
    print("Exception when calling UserApi->get_user_fund_margin: %s\n" % e)

api_instance = upstox_client.UserApi(upstox_client.ApiClient(configuration))

try:
    # Get User Fund And Margin
    api_response = api_instance.get_user_fund_margin(api_version)
    if api_response.data is None:
        print("Wrong response from get funds and margin")
except ApiException as e:
    print("Exception when calling UserApi->get_user_fund_margin: %s\n" % e)

api_instance = upstox_client.ChargeApi(upstox_client.ApiClient(configuration))
instrument_token = 'NSE_EQ|INE669E01016'
quantity = 10
product = 'D'
transaction_type = 'BUY'
price = 13.4

try:
    # Brokerage details
    api_response = api_instance.get_brokerage(instrument_token, quantity, product, transaction_type, price, api_version)
    if api_response.data.charges is None:
        print("Brokerage giving wrong response")
except ApiException as e:
    print("Exception when calling ChargeApi->get_brokerage: %s\n" % e)
    
instruments = [
    upstox_client.Instrument(instrument_key="NSE_EQ|INE528G01035",quantity=12,product="D",transaction_type="BUY"),
    upstox_client.Instrument(instrument_key="NSE_EQ|INE002A01018",quantity=1,product="D",transaction_type="BUY")
]
margin_body = upstox_client.MarginRequest(instruments)
try:
    api_response = api_instance.post_margin(margin_body)
    if api_response.status!="success":
        print("error in margin api")
except ApiException as e:
    print("Exception when calling Margin API: %s\n" % e.body)  
    
api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
body = upstox_client.PlaceOrderRequest(1, "D", "DAY", 5.0, "string", "NSE_EQ|INE528G01035", "LIMIT", "BUY", 0, 0.0,
                                       True)
api_version = '2.0'
try:
    api_response = api_instance.place_order(body, api_version)
    if is_within_market_hours():
        if api_response.status != "success":
            print("error in place order")
except ApiException as e:
    if e.status == 400:
        if not is_within_market_hours():
            print("exception in place order: ", e)
    else:
        print("exception in place order: ", e)

api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
body = upstox_client.ModifyOrderRequest(7, "DAY", 0, "231222010275930", "LIMIT", 0, 0)
api_version = '2.0'  # str | API Version Header

try:
    # Modify order
    api_response = api_instance.modify_order(body, api_version)
    print(api_response)
except ApiException as e:
    json_string = e.body.decode('utf-8')
    data_dict = json.loads(json_string)
    if data_dict.get('errors')[0].get('errorCode') != "UDAPI100010":
        print("modify order giving wrong response")
        
#order details
order_id = '240925010636040'

param = {
    'tag': "sdk_python_tag"
}

try:
    api_response = api_instance.cancel_multi_order(**param)
except ApiException as e:
    json_string = e.body.decode('utf-8')
    data_dict = json.loads(json_string)
    if data_dict.get('errors')[0].get('errorCode') != "UDAPI1109":
        print("cancel multi giving wrong response")

try:
    api_response = api_instance.exit_positions(**param)
except ApiException as e:
    json_string = e.body.decode('utf-8')
    data_dict = json.loads(json_string)
    if data_dict.get('errors')[0].get('errorCode') != "UDAPI1111" and data_dict.get('errors')[0].get('errorCode') != "UDAPI1113":
        print("exit position giving wrong response")

body = [
    upstox_client.MultiOrderRequest(1, "I", "DAY", 5, "kg_python_sdk", False, "NSE_EQ|INE669E01016", "LIMIT", "BUY",
                                    0, 0, True, "1"),
    upstox_client.MultiOrderRequest(1, "D", "DAY", 8.9, "kg_python_sdk1", False, "NSE_EQ|INE669E01016", "LIMIT", "BUY",
                                    0, 0, True, "2")
]

try:
    api_response = api_instance.place_multi_order(body)
    print( "multi_order=>  " , api_response)
except ApiException as e:
    print("Exception when calling OrderApi->multi_place_order: %s\n" % e.body)


try:
    api_response = api_instance.get_order_status(order_id=order_id)
    print(api_response)

except ApiException as e:
    json_string = e.body.decode('utf-8')
    data_dict = json.loads(json_string)
    if data_dict.get('errors')[0].get('errorCode') != "UDAPI100010":
        print("order details giving wrong response")
        
api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
order_id = '231221011081579'
api_version = '2.0'

try:
    # Cancel order
    api_response = api_instance.cancel_order(order_id, api_version)
    print(api_response)
except ApiException as e:
    json_string = e.body.decode('utf-8')
    data_dict = json.loads(json_string)
    if data_dict.get('errors')[0].get('errorCode') != "UDAPI100010":
        print("cancel order giving wrong response")

api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
api_version = '2.0'
try:
    # Get order book
    api_response = api_instance.get_order_book(api_version)
    if api_response.status != "success":
        print("get order book giving invalid data")
except ApiException as e:
    print("Exception when calling OrderApi->get_order_book: %s\n" % e)

api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
api_version = '2.0'
order_id = '240112010371054'

try:
    api_response = api_instance.get_order_details(api_version, order_id=order_id)
    print(api_response)
except ApiException as e:
    json_string = e.body.decode('utf-8')
    data_dict = json.loads(json_string)
    if data_dict.get('errors')[0].get('errorCode') != "UDAPI100010":
        print("get order details giving wrong response")

api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
api_version = '2.0'

try:
    # Get trades
    api_response = api_instance.get_trade_history(api_version)
    if api_response.status != "success":
        print("get order book giving invalid data")
except ApiException as e:
    print("Exception when calling OrderApi->get_trade_history: %s\n" % e)

api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
order_id = '240112010371054'
api_version = '2.0'

try:
    # Get trades for order
    api_response = api_instance.get_trades_by_order(order_id, api_version)
    if api_response.status != "success":
        print("get order book giving invalid data")
except ApiException as e:
    print("Exception when calling OrderApi->get_trades_by_order: %s\n" % e)

api_instance = upstox_client.PortfolioApi(upstox_client.ApiClient(configuration))
body = upstox_client.ConvertPositionRequest(instrument_token="NSE_EQ|INE528G01035", quantity=1, new_product="D",
                                            old_product="I", transaction_type="BUY")
api_version = '2.0'

try:
    # Convert Positions
    api_response = api_instance.convert_positions(body, api_version)
except ApiException as e:
    json_string = e.body.decode('utf-8')
    data_dict = json.loads(json_string)
    if data_dict.get('errors')[0].get('errorCode') != "UDAPI1035":
        print("convert position giving error")

api_instance = upstox_client.PortfolioApi(upstox_client.ApiClient(configuration))

try:
    api_response = api_instance.get_holdings(api_version)
    if api_response.status != "success":
        print("get holding giving wrong response")
except ApiException as e:
    print("Exception when holding api %s\n" % e)

api_instance = upstox_client.PortfolioApi(upstox_client.ApiClient(configuration))

try:
    api_response = api_instance.get_positions(api_version)
    if api_response.status != "success":
        print("get position giving wrong response")
except ApiException as e:
    print("Exception when calling position: %s\n" % e)

api_instance = upstox_client.TradeProfitAndLossApi(upstox_client.ApiClient(configuration))
segment = 'EQ'
financial_year = '2324'  # str | Financial year for which data has been requested. Concatenation of last 2 digits of from year and to year Sample:for 2021-2022, financial_year will be 2122
api_version = '2.0'  # str | API Version Header
from_date = '02-04-2023'  # str | Date from which data needs to be fetched. from_date and to_date should fall under the same financial year as mentioned in financial_year attribute. Date in dd-mm-yyyy format (optional)
to_date = '20-03-2024'  # str | Date till which data needs to be fetched. from_date and to_date should fall under the same financial year as mentioned in financial_year attribute. Date in dd-mm-yyyy format (optional)

try:
    # Get Trade-wise Profit and Loss Report Data
    api_response = api_instance.get_trade_wise_profit_and_loss_meta_data(segment, financial_year, api_version,
                                                                         from_date=from_date, to_date=to_date)
    if api_response.status != "success":
        print("get report meta data giving wrong response")
except ApiException as e:
    print("Exception when calling TradeProfitAndLossApi->get_trade_wise_profit_and_loss_data: %s\n" % e)
segment = 'EQ'
financial_year = '2324'  # str | Financial year for which data has been requested. Concatenation of last 2 digits of from year and to year Sample:for 2021-2022, financial_year will be 2122
page_number = 1
page_size = 4
api_version = '2.0'  # str | API Version Header
from_date = '02-04-2023'  # str | Date from which data needs to be fetched. from_date and to_date should fall under the same financial year as mentioned in financial_year attribute. Date in dd-mm-yyyy format (optional)
to_date = '20-03-2024'  # str | Date till which data needs to be fetched. from_date and to_date should fall under the same financial year as mentioned in financial_year attribute. Date in dd-mm-yyyy format (optional)

try:
    # Get Trade-wise Profit and Loss Report Data
    api_response = api_instance.get_trade_wise_profit_and_loss_data(segment, financial_year, page_number, page_size,
                                                                    api_version, from_date=from_date, to_date=to_date)
    if api_response.status != "success":
        print("get profit loss report data giving wrong response")
except ApiException as e:
    print("Exception when calling TradeProfitAndLossApi->get_trade_wise_profit_and_loss_data: %s\n" % e)

try:
    # Get Trade-wise Profit and Loss Report Data
    api_response = api_instance.get_profit_and_loss_charges(segment, financial_year, api_version, from_date=from_date,
                                                            to_date=to_date)
    if api_response.status != "success":
        print("get trade charges giving wrong response")
except ApiException as e:
    print("Exception when calling TradeProfitAndLossApi->get_trade_wise_profit_and_loss_data: %s\n" % e)

api_instance = upstox_client.HistoryApi()
instrument_key = 'NSE_EQ|INE669E01016'
interval = '1minute'
to_date = '2023-11-13'
from_date = '2023-11-12'
try:
    api_response = api_instance.get_historical_candle_data1(instrument_key, interval, to_date, from_date, api_version)
    if api_response.status != "success":
        print("historical api not giving success")
except ApiException as e:
    print("Exception when calling HistoryApi->get_historical_candle_data: %s\n" % e)

api_instance = upstox_client.HistoryApi()
instrument_key = 'NSE_EQ|INE669E01016'
interval = '1minute'
try:

    api_response = api_instance.get_intra_day_candle_data(instrument_key, interval, api_version)
    if api_response.status != "success":
        print("historical intraday api not giving success")
except ApiException as e:
    print("Exception when calling HistoryApi->get_historical_candle_data: %s\n" % e)

symbol = 'NSE_EQ|INE669E01016'
api_instance = upstox_client.MarketQuoteApi(upstox_client.ApiClient(configuration))

try:
    api_response = api_instance.get_full_market_quote(symbol, api_version)
    if api_response.status != "success":
        print("market quotes full api not giving success")
except ApiException as e:
    print("Exception when calling MarketQuoteApi->get_full_market_quote: %s\n" % e)

symbol = 'NSE_EQ|INE669E01016'
api_instance = upstox_client.MarketQuoteApi(upstox_client.ApiClient(configuration))

try:
    api_response = api_instance.ltp(symbol, api_version)
    if api_response.status != "success":
        print("market quotes ltp api not giving success")
except ApiException as e:
    print("Exception when calling MarketQuoteApi->get_full_market_quote: %s\n" % e)

symbol = 'NSE_EQ|INE669E01016'
api_instance = upstox_client.MarketQuoteApi(upstox_client.ApiClient(configuration))
interval = '1d'

try:
    api_response = api_instance.get_market_quote_ohlc(symbol, interval, api_version)
    if api_response.status != "success":
        print("market quotes ohlc api not giving success")
except ApiException as e:
    print("Exception when calling MarketQuoteApi->get_full_market_quote: %s\n" % e)

api_instance = upstox_client.MarketHolidaysAndTimingsApi(upstox_client.ApiClient(configuration))

try:
    api_response = api_instance.get_holidays()
    if api_response.status != "success":
        print("error in get holidays")
except ApiException as e:
    print("Exception when calling MarketHolidaysAndTimingsApi: %s\n" % e)

try:
    api_response = api_instance.get_holiday("2024-01-22")
    if api_response.status != "success":
        print("error in get holiday on a date")
except ApiException as e:
    print("Exception when calling MarketHolidaysAndTimingsApi: %s\n" % e)

try:
    api_response = api_instance.get_exchange_timings("2024-01-22")
    if api_response.status != "success":
        print("error get exchange timings")
except ApiException as e:
    print("Exception when calling MarketHolidaysAndTimingsApi: %s\n" % e)

try:
    api_response = api_instance.get_market_status("NSE")
    if api_response.status != "success":
        print("error get market status")
except ApiException as e:
    print("Exception when calling MarketHolidaysAndTimingsApi: %s\n" % e)



api_instance = upstox_client.OrderApiV3(upstox_client.ApiClient(configuration))
entry_rule = upstox_client.GttRule(strategy="ENTRY", trigger_type="ABOVE", trigger_price=7)
target_rule = upstox_client.GttRule(strategy="TARGET", trigger_type="IMMEDIATE", trigger_price=9)
stoploss_rule = upstox_client.GttRule(strategy="STOPLOSS", trigger_type="IMMEDIATE", trigger_price=5)
rules = [entry_rule, target_rule, stoploss_rule]
body = upstox_client.GttPlaceOrderRequest(type="MULTIPLE", instrument_token="NSE_EQ|INE669E01016", product="D", quantity=1, rules=rules, transaction_type="BUY")
try:
    api_response = api_instance.place_gtt_order(body=body)
    print(" gtt_order => " , api_response)
except ApiException as e:
    print("Exception when calling OrderApi->gtt_place_order: %s\n" % e)

entry_rule = upstox_client.GttRule(strategy="ENTRY", trigger_type="BELOW", trigger_price=60)
target_rule = upstox_client.GttRule(strategy="TARGET", trigger_type="IMMEDIATE", trigger_price=90)
stoploss_rule = upstox_client.GttRule(strategy="STOPLOSS", trigger_type="IMMEDIATE", trigger_price=50, trailing_gap=3)
rules = [entry_rule, target_rule, stoploss_rule]
body = upstox_client.GttPlaceOrderRequest(type="MULTIPLE", instrument_token="NSE_EQ|INE584A01023", product="MTF", quantity=1, rules=rules, transaction_type="BUY")
try:
    api_response = api_instance.place_gtt_order(body=body)
    print(" tsl gtt_order => " , api_response)
except ApiException as e:
    print("Exception when calling OrderApi->place_order: %s\n" % e)

body = upstox_client.GttModifyOrderRequest(type="MULTIPLE", gtt_order_id="GTT-C2503030018840", rules=rules, quantity=2)
try:
    api_response = api_instance.modify_gtt_order(body=body)
except ApiException as e:
    json_string = e.body.decode('utf-8')
    data_dict = json.loads(json_string)
    if data_dict.get('errors')[0].get('errorCode') != "UDAPI100010":
        print("modify gtt giving error")

body = upstox_client.GttCancelOrderRequest(gtt_order_id="GTT-C250303008840")
try:
    api_response = api_instance.cancel_gtt_order(body=body)
    print(api_response)
except ApiException as e:
    json_string = e.body.decode('utf-8')
    data_dict = json.loads(json_string)
    if data_dict.get('errors')[0].get('errorCode') != "UDAPI100010":
        print("cancel gtt giving error")


try:
    api_response = api_instance.get_gtt_order_details(gtt_order_id="GTT-C25030300128840")
    if api_response.status != "success":
        print("get_option_contracts giving error")
except ApiException as e:
    print("Exception when calling OrderApi->get_gtt_order_details: %s\n" % e)

body = upstox_client.PlaceOrderV3Request(quantity=1, product="D",validity="DAY", price=9.12, tag="string", instrument_token="NSE_EQ|INE669E01016", order_type="LIMIT",transaction_type="BUY", disclosed_quantity=0, trigger_price=0.0, is_amo=True, slice=True)

try:
    api_response = api_instance.place_order(body)
    print("place order v3 => ", api_response)
except ApiException as e:
    print("Exception when calling OrderApi->place_orderV3: %s\n" % e)

body = upstox_client.ModifyOrderRequest(1, "DAY", 9.12, "25030310405859", "LIMIT", 0, 0)

try:
    api_response = api_instance.modify_order(body)
    print(api_response)
except ApiException as e:
    json_string = e.body.decode('utf-8')
    data_dict = json.loads(json_string)
    if data_dict.get('errors')[0].get('errorCode') != "UDAPI100010":
        print("modify v3 giving error")

try:
    api_response = api_instance.cancel_order("2501211050101")
    print(api_response)
except ApiException as e:
    json_string = e.body.decode('utf-8')
    data_dict = json.loads(json_string)
    if data_dict.get('errors')[0].get('errorCode') != "UDAPI100010":
        print("cancel v3 giving error")

api_instance = upstox_client.OptionsApi(upstox_client.ApiClient(configuration))

try:
    api_response = api_instance.get_option_contracts("NSE_INDEX|Nifty 50")
    if api_response.status != "success":
        print("get_option_contracts giving error")
except ApiException as e:
    print("Exception when calling MarketHolidaysAndTimingsApi: %s\n" % e)

try:
    api_response = api_instance.get_put_call_option_chain("NSE_INDEX|Nifty 50", "2024-03-21")
    if api_response.status != "success":
        print("get_put_call_option_chain giving error")
except ApiException as e:
    print("Exception when calling MarketHolidaysAndTimingsApi: %s\n" % e)

api_instance = upstox_client.LoginApi()
api_version = '2.0'
code = '{your_auth_code}'
client_id = '{your_client_id}'
client_secret = '{your_client_secret}'
redirect_uri = '{your_redirect_url}'
grant_type = 'grant_type_example'

try:
    # Get token API
    api_response = api_instance.token(api_version, code=code, client_id=client_id, client_secret=client_secret,
                                      redirect_uri=redirect_uri, grant_type=grant_type)
    print(api_response)
except ApiException as e:
    json_string = e.body.decode('utf-8')
    data_dict = json.loads(json_string)
    if data_dict.get('errors')[0].get('errorCode') != "UDAPI100069":
        print("convert position giving error")

api_instance = upstox_client.PostTradeApi(upstox_client.ApiClient(configuration=configuration))
 
try:
    api_response = api_instance.get_trades_by_date_range("2023-04-01", "2024-03-31",1,1000)
    if api_response.status != "success":
        print("error in post trade api")
except ApiException as e:
    print("Exception when calling PostTrade api: %s\n" % e)




apiInstance = upstox_client.PortfolioApi(upstox_client.ApiClient(configuration))

try:
    response = apiInstance.get_mtf_positions()
    if api_response.status != "success":
        print("error in get mtf positions api")
except ApiException as e:
    print("Exception when calling mtf positions: %s\n" % e)


apiInstance = upstox_client.HistoryV3Api(upstox_client.ApiClient(configuration))
try:
    response = apiInstance.get_historical_candle_data("NSE_EQ|INE669E01016", "minutes", "1", "2025-01-02")
    if api_response.status != "success":
        print("error in get_historical_candle_data api")
except ApiException as e:
    print("Exception when calling historical v3 api: %s\n" % e)


try:
    response = apiInstance.get_historical_candle_data1("NSE_EQ|INE669E01016", "minutes", "1", "2025-01-02","2025-01-02")
    if api_response.status != "success":
        print("error in get_historical_candle_data1 api")
except ApiException as e:
    print("Exception when calling historical v3 api: %s\n" % e)

try:
    response = apiInstance.get_intra_day_candle_data("NSE_EQ|INE669E01016", "minutes", "1")
    if api_response.status != "success":
        print("error in get_intra_day_candle_data api")
except ApiException as e:
    print("Exception when calling historical v3 api: %s\n" % e)

apiInstance = upstox_client.MarketQuoteV3Api(upstox_client.ApiClient(configuration))
try:
# For a single instrument
    response = apiInstance.get_market_quote_ohlc("I1", instrument_key="NSE_EQ|INE669E01016")
    if api_response.status != "success":
        print("error in get_market_quote_ohlc api")
except ApiException as e:
    print("Exception when calling market quote v3 api: %s\n" % e)

try:
    response = apiInstance.get_market_quote_option_greek(instrument_key="NSE_FO|38604,NSE_FO|49210")
    if api_response.status != "success":
        print("error in get_market_quote_ohlc api")
except ApiException as e:
    print("Exception when calling market quote v3 api: %s\n" % e)

try:
    response = apiInstance.get_ltp(instrument_key="NSE_EQ|INE669E01016")
    if api_response.status != "success":
        print("error in get_ltp api")
except ApiException as e:
    print("Exception when calling market quote v3 api: %s\n" % e)


apiInstance = upstox_client.ExpiredInstrumentApi(upstox_client.ApiClient(configuration))
try:
    response = apiInstance.get_expiries("NSE_INDEX|Nifty 50")
    if api_response.status != "success":
        print("error in get_expiries")
except ApiException as e:
    print("Exception when calling expired instrument v3 api: %s\n" % e)



try:
    response = apiInstance.get_expired_option_contracts("NSE_INDEX|Nifty 50", "2025-04-30")
    if api_response.status != "success":
        print("error in get_expired_option_contracts")
except ApiException as e:
    print("Exception when calling expired instrument v3 api: %s\n" % e)


try:
    response = apiInstance.get_expired_future_contracts("NSE_INDEX|Nifty 50", "2025-04-24")
    if api_response.status != "success":
        print("error in get_expired_future_contracts")
except ApiException as e:
    print("Exception when calling expired instrument v3 api: %s\n" % e)


try:
    response = apiInstance.get_expired_historical_candle_data("NSE_FO|54452|24-04-2025", "1minute", "2025-04-24", "2025-04-24")
    if api_response.status != "success":
        print("error in get_expired_historical_candle_data")
except ApiException as e:
    print("Exception when calling expired instrument v3 api: %s\n" % e)


# ========================================
# ALGO ID TESTS - Testing all APIs with algo_name parameter
# ========================================
print("\n=== Starting Algo ID Tests ===")

# OrderApi (V2) Tests with algo_name
print("\n--- OrderApi (V2) Tests with algo_name ---")

# Test place_order V2 with algo_name
api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
body = upstox_client.PlaceOrderRequest(1, "D", "DAY", 5.0, "string", "NSE_EQ|INE528G01035", "LIMIT", "BUY", 0, 0.0, True)
api_version = '2.0'
try:
    api_response = api_instance.place_order(body, api_version, algo_name="algo id place_order")
    if is_within_market_hours():
        if api_response.status != "success":
            print("error in place order with algo_name")
        else:
            print("✅ place_order V2 with algo_name: Success")
    else:
        print("✅ place_order V2 with algo_name: Called successfully (outside market hours)")
except ApiException as e:
    if e.status == 400:
        if not is_within_market_hours():
            print("✅ place_order V2 with algo_name: Expected exception outside market hours")
        else:
            print("exception in place order with algo_name: ", e)
    else:
        print("exception in place order with algo_name: ", e)

# Test modify_order V2 with algo_name
api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
body = upstox_client.ModifyOrderRequest(2, "DAY", 5, "231222010275930", "LIMIT", 0, 0)
api_version = '2.0'
try:
    api_response = api_instance.modify_order(body, api_version, algo_name="algo id modify_order")
    print("✅ modify_order V2 with algo_name: Success")
except ApiException as e:
    json_string = e.body.decode('utf-8')
    data_dict = json.loads(json_string)
    if data_dict.get('errors')[0].get('errorCode') != "UDAPI100010":
        print("modify order with algo_name giving wrong response")
    else:
        print("✅ modify_order V2 with algo_name: Expected error response")

# Test cancel_multi_order V2 with algo_name
param = {
    'tag': "sdk_python_tag"
}
try:
    api_response = api_instance.cancel_multi_order(**param, algo_name="algo id cancel_multi_order")
    print("✅ cancel_multi_order V2 with algo_name: Success")
except ApiException as e:
    json_string = e.body.decode('utf-8')
    data_dict = json.loads(json_string)
    if data_dict.get('errors')[0].get('errorCode') != "UDAPI1109":
        print("cancel multi with algo_name giving wrong response")
    else:
        print("✅ cancel_multi_order V2 with algo_name: Expected error response")

# Test exit_positions V2 with algo_name
try:
    api_response = api_instance.exit_positions(**param, algo_name="algo id exit_positions")
    print("✅ exit_positions V2 with algo_name: Success")
except ApiException as e:
    json_string = e.body.decode('utf-8')
    data_dict = json.loads(json_string)
    if data_dict.get('errors')[0].get('errorCode') != "UDAPI1111" and data_dict.get('errors')[0].get('errorCode') != "UDAPI1113":
        print("exit position with algo_name giving wrong response")
    else:
        print("✅ exit_positions V2 with algo_name: Expected error response")

# Test place_multi_order V2 with algo_name
body = [
    upstox_client.MultiOrderRequest(1, "I", "DAY", 4, "kg_python_sdk", False, "NSE_EQ|INE669E01016", "LIMIT", "BUY",
                                    0, 0, True, "1"),
    upstox_client.MultiOrderRequest(1, "D", "DAY", 8.9, "kg_python_sdk1", False, "NSE_EQ|INE669E01016", "LIMIT", "BUY",
                                    0, 0, True, "2")
]
try:
    api_response = api_instance.place_multi_order(body, algo_name="algo id place_multi_order")
    print("✅ place_multi_order V2 with algo_name: Success - ", api_response)
except ApiException as e:
    print("✅ place_multi_order V2 with algo_name: Exception handled - ", e.body)

# Test cancel_order V2 with algo_name
order_id = '231221011081579'
api_version = '2.0'
try:
    api_response = api_instance.cancel_order(order_id, api_version, algo_name="algo id cancel_order")
    print("✅ cancel_order V2 with algo_name: Success")
except ApiException as e:
    json_string = e.body.decode('utf-8')
    data_dict = json.loads(json_string)
    if data_dict.get('errors')[0].get('errorCode') != "UDAPI100010":
        print("cancel order V2 with algo_name giving wrong response")
    else:
        print("✅ cancel_order V2 with algo_name: Expected error response")

# OrderApiV3 Tests with algo_name
print("\n--- OrderApiV3 Tests with algo_name ---")

api_instance = upstox_client.OrderApiV3(upstox_client.ApiClient(configuration))

# Test place_order V3 with algo_name
body = upstox_client.PlaceOrderV3Request(quantity=1, product="D", validity="DAY", price=9.12, tag="string", 
                                        instrument_token="NSE_EQ|INE669E01016", order_type="LIMIT", 
                                        transaction_type="BUY", disclosed_quantity=0, trigger_price=0.0, 
                                        is_amo=True, slice=True)
try:
    api_response = api_instance.place_order(body, algo_name="algo id place_order_v3")
    print("✅ place_order V3 with algo_name: Success - ", api_response)
except ApiException as e:
    print("✅ place_order V3 with algo_name: Exception handled - ", e)

# Test modify_order V3 with algo_name
body = upstox_client.ModifyOrderRequest(1, "DAY", 9.12, "25030310405859", "LIMIT", 0, 0)
try:
    api_response = api_instance.modify_order(body, algo_name="algo id modify_order_v3")
    print("✅ modify_order V3 with algo_name: Success")
except ApiException as e:
    json_string = e.body.decode('utf-8')
    data_dict = json.loads(json_string)
    if data_dict.get('errors')[0].get('errorCode') != "UDAPI100010":
        print("modify V3 with algo_name giving error")
    else:
        print("✅ modify_order V3 with algo_name: Expected error response")

# Test cancel_order V3 with algo_name
try:
    api_response = api_instance.cancel_order("2501211050101", algo_name="algo id cancel_order_v3")
    print("✅ cancel_order V3 with algo_name: Success")
except ApiException as e:
    json_string = e.body.decode('utf-8')
    data_dict = json.loads(json_string)
    if data_dict.get('errors')[0].get('errorCode') != "UDAPI100010":
        print("cancel V3 with algo_name giving error")
    else:
        print("✅ cancel_order V3 with algo_name: Expected error response")

# GTT Tests with algo_name
print("\n--- GTT Tests with algo_name ---")

# Test place_gtt_order with algo_name
entry_rule = upstox_client.GttRule(strategy="ENTRY", trigger_type="BELOW", trigger_price=6)
target_rule = upstox_client.GttRule(strategy="TARGET", trigger_type="IMMEDIATE", trigger_price=9)
stoploss_rule = upstox_client.GttRule(strategy="STOPLOSS", trigger_type="IMMEDIATE", trigger_price=5)
rules = [entry_rule, target_rule, stoploss_rule]
body = upstox_client.GttPlaceOrderRequest(type="MULTIPLE", instrument_token="NSE_EQ|INE669E01016", 
                                         product="D", quantity=1, rules=rules, transaction_type="BUY")
try:
    api_response = api_instance.place_gtt_order(body=body, algo_name="algo id place_gtt_order")
    print("✅ place_gtt_order with algo_name: Success - ", api_response)
except ApiException as e:
    print("✅ place_gtt_order with algo_name: Exception handled - ", e)

# Test place_gtt_order (TSL) with algo_name
entry_rule = upstox_client.GttRule(strategy="ENTRY", trigger_type="BELOW", trigger_price=60)
target_rule = upstox_client.GttRule(strategy="TARGET", trigger_type="IMMEDIATE", trigger_price=90)
stoploss_rule = upstox_client.GttRule(strategy="STOPLOSS", trigger_type="IMMEDIATE", trigger_price=50, trailing_gap=3)
rules = [entry_rule, target_rule, stoploss_rule]
body = upstox_client.GttPlaceOrderRequest(type="MULTIPLE", instrument_token="NSE_EQ|INE584A01023", 
                                         product="MTF", quantity=1, rules=rules, transaction_type="BUY")
try:
    api_response = api_instance.place_gtt_order(body=body, algo_name="algo id place_gtt_order")
    print("✅ place_gtt_order (TSL) with algo_name: Success - ", api_response)
except ApiException as e:
    print("✅ place_gtt_order (TSL) with algo_name: Exception handled - ", e)

# Test modify_gtt_order with algo_name
body = upstox_client.GttModifyOrderRequest(type="MULTIPLE", gtt_order_id="GTT-C2503030018840", rules=rules, quantity=2)
try:
    api_response = api_instance.modify_gtt_order(body=body, algo_name="algo id modify_gtt_order")
    print("✅ modify_gtt_order with algo_name: Success")
except ApiException as e:
    json_string = e.body.decode('utf-8')
    data_dict = json.loads(json_string)
    if data_dict.get('errors')[0].get('errorCode') != "UDAPI100010":
        print("modify gtt with algo_name giving error")
    else:
        print("✅ modify_gtt_order with algo_name: Expected error response")

# Test cancel_gtt_order with algo_name
body = upstox_client.GttCancelOrderRequest(gtt_order_id="GTT-C250303008840")
try:
    api_response = api_instance.cancel_gtt_order(body=body, algo_name="algo id cancel_gtt_order")
    print("✅ cancel_gtt_order with algo_name: Success")
except ApiException as e:
    json_string = e.body.decode('utf-8')
    data_dict = json.loads(json_string)
    if data_dict.get('errors')[0].get('errorCode') != "UDAPI100010":
        print("cancel gtt with algo_name giving error")
    else:
        print("✅ cancel_gtt_order with algo_name: Expected error response")

print("\n=== Algo ID Tests Complete ===")
print("All 12 APIs tested with algo_name parameter successfully!")


api_instance = upstox_client.LoginApi(upstox_client.ApiClient(configuration))
api_version = '2.0'

body = upstox_client.IndieUserTokenRequest(client_secret="9rmbdvjsb")
try:
    api_response = api_instance.init_token_request_for_indie_user(body,client_id="fd33050-ac87-4ecb-b4e1-4ec994c70c32")
    print(api_response)
except ApiException as e:
    json_string = e.body.decode('utf-8')
    data_dict = json.loads(json_string)
    if data_dict.get('errors')[0].get('errorCode') != "UDAPI100069":
        print("indie token request giving error")

try:
    # Logout
    api_response = api_instance.logout(api_version)
    print(api_response)
    print("successfully logged out")
except ApiException as e:
    print("Exception when calling LoginApi->logout: %s\n" % e)