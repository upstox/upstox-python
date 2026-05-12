import upstox_client
import data_token
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = data_token.access_token

api_instance = upstox_client.MarketApi(upstox_client.ApiClient(configuration))
instrument_key = 'NSE_INDEX|Nifty 50'
expiry = '2025-06-26'
date = '2025-06-12'

try:
    api_response = api_instance.get_oi_data(instrument_key, expiry, date)
    if api_response.status != "success":
        print("MarketApi->get_oi_data not returning success")
except ApiException as e:
    print("Exception when calling MarketApi->get_oi_data: %s\n" % e)

try:
    api_response = api_instance.get_change_oi_data(instrument_key, expiry, date, 5)
    if api_response.status != "success":
        print("MarketApi->get_change_oi_data not returning success")
except ApiException as e:
    print("Exception when calling MarketApi->get_change_oi_data: %s\n" % e)

try:
    api_response = api_instance.get_pcr_data(instrument_key, expiry, date, 30)
    if api_response.status != "success":
        print("MarketApi->get_pcr_data not returning success")
except ApiException as e:
    print("Exception when calling MarketApi->get_pcr_data: %s\n" % e)

try:
    api_response = api_instance.get_max_pain_data(instrument_key, expiry, date, 30)
    if api_response.status != "success":
        print("MarketApi->get_max_pain_data not returning success")
except ApiException as e:
    print("Exception when calling MarketApi->get_max_pain_data: %s\n" % e)

try:
    api_response = api_instance.get_fii_data('NSE_EQ|CASH', '1D')
    if api_response.status != "success":
        print("MarketApi->get_fii_data not returning success")
except ApiException as e:
    print("Exception when calling MarketApi->get_fii_data: %s\n" % e)

try:
    api_response = api_instance.get_dii_data('NSE_EQ|CASH', '1D')
    if api_response.status != "success":
        print("MarketApi->get_dii_data not returning success")
except ApiException as e:
    print("Exception when calling MarketApi->get_dii_data: %s\n" % e)
