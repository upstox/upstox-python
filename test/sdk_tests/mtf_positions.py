import upstox_client
import data_token

from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = data_token.access_token

apiInstance = upstox_client.PortfolioApi(upstox_client.ApiClient(configuration))

try:
    response = apiInstance.get_mtf_positions()
    print(response)
except ApiException as e:
    print("Exception when calling mtf positions: %s\n" % e)


apiInstance = upstox_client.HistoryV3Api(upstox_client.ApiClient(configuration))
try:
    response = apiInstance.get_historical_candle_data("NSE_EQ|INE669E01016", "minutes", "1", "2025-01-02")
    print(response)
except ApiException as e:
    print("Exception when calling historical v3 api: %s\n" % e)


try:
    response = apiInstance.get_historical_candle_data1("NSE_EQ|INE669E01016", "minutes", "1", "2025-01-02","2025-01-02")
    print(response)
except ApiException as e:
    print("Exception when calling historical v3 api: %s\n" % e)

try:
    response = apiInstance.get_intra_day_candle_data("NSE_EQ|INE669E01016", "minutes", "1")
    print(response)
except ApiException as e:
    print("Exception when calling historical v3 api: %s\n" % e)

apiInstance = upstox_client.MarketQuoteV3Api(upstox_client.ApiClient(configuration))
try:
# For a single instrument
    response = apiInstance.get_market_quote_ohlc("I1", instrument_key="NSE_EQ|INE669E01016")
    print(response)
except ApiException as e:
    print("Exception when calling market quote v3 api: %s\n" % e)

try:
    response = apiInstance.get_market_quote_option_greek(instrument_key="NSE_FO|38604,NSE_FO|49210")
    print(response)
except ApiException as e:
    print("Exception when calling market quote v3 api: %s\n" % e)

try:
    response = apiInstance.get_ltp(instrument_key="NSE_EQ|INE669E01016")
    print(response)
except ApiException as e:
    print("Exception when calling market quote v3 api: %s\n" % e)


apiInstance = upstox_client.ExpiredInstrumentApi(upstox_client.ApiClient(configuration))
try:
    response = apiInstance.get_expiries("NSE_INDEX|Nifty 50")
    print(response)
except ApiException as e:
    print("Exception when calling expired instrument v3 api: %s\n" % e)



try:
    response = apiInstance.get_expired_option_contracts("NSE_INDEX|Nifty 50", "2025-04-30")
    print(response)
except ApiException as e:
    print("Exception when calling expired instrument v3 api: %s\n" % e)


try:
    response = apiInstance.get_expired_future_contracts("NSE_INDEX|Nifty 50", "2025-04-24")
    print(response)
except ApiException as e:
    print("Exception when calling expired instrument v3 api: %s\n" % e)


try:
    response = apiInstance.get_expired_historical_candle_data("NSE_FO|54452|24-04-2025", "1minute", "2025-04-24", "2025-04-24")
    print(response)
except ApiException as e:
    print("Exception when calling expired instrument v3 api: %s\n" % e)

