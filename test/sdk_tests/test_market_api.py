import upstox_client
import data_token
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = data_token.access_token

api_instance = upstox_client.MarketApi(upstox_client.ApiClient(configuration))
instrument_key = 'NSE_INDEX|Nifty 50'
expiry = '2026-05-19'
date = '2026-05-05'

try:
    api_response = api_instance.get_oi_data(instrument_key, expiry, date)
    if api_response.status != "success":
        print("MarketApi->get_oi_data not returning success")
except ApiException as e:
    print("Exception when calling MarketApi->get_oi_data: %s\n" % e)

try:
    api_response = api_instance.get_change_oi_data(instrument_key, expiry, date, 3)
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

# Smartlist endpoints
try:
    api_response = api_instance.get_smartlist_options(asset_type="INDEX", category="TOP_TRADED", page_number=1, page_size=50)
    if api_response.status != "success":
        print("MarketApi->get_smartlist_options not returning success")
except ApiException as e:
    print("Exception when calling MarketApi->get_smartlist_options: %s\n" % e)

try:
    api_response = api_instance.get_smartlist_futures(asset_type="STOCK", category="MOST_ACTIVE", page_number=1, page_size=50)
    if api_response.status != "success":
        print("MarketApi->get_smartlist_futures not returning success")
except ApiException as e:
    print("Exception when calling MarketApi->get_smartlist_futures: %s\n" % e)

try:
    api_response = api_instance.get_smartlist_mtf(page_number=1, page_size=50)
    if api_response.status != "success":
        print("MarketApi->get_smartlist_mtf not returning success")
except ApiException as e:
    print("Exception when calling MarketApi->get_smartlist_mtf: %s\n" % e)

# Model instantiation tests (smartlist responses reuse AnalyticsResponse/AnalyticsData)
analytics_data = upstox_client.AnalyticsData(delta=0.5, iv=12.3)
if analytics_data.delta != 0.5:
    print("error: AnalyticsData fields not set correctly")

analytics_response = upstox_client.AnalyticsResponse(status="success", data=[analytics_data])
if analytics_response.status != "success":
    print("error: AnalyticsResponse status field not set correctly")
