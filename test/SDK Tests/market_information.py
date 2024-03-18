import upstox_client
from upstox_client.rest import ApiException
import const_file
configuration = upstox_client.Configuration()
configuration.access_token = const_file.access_token

api_instance = upstox_client.MarketHolidaysAndTimingsApi(upstox_client.ApiClient(configuration))

try:
    api_response = api_instance.get_holidays()
    print(api_response)
except ApiException as e:
    print("Exception when calling MarketHolidaysAndTimingsApi: %s\n" %e)

try:
    api_response = api_instance.get_holiday("2024-01-22")
    print(api_response)
except ApiException as e:
    print("Exception when calling MarketHolidaysAndTimingsApi: %s\n" %e)

try:
    api_response = api_instance.get_exchange_timings("2024-01-22")
    print(api_response)
except ApiException as e:
    print("Exception when calling MarketHolidaysAndTimingsApi: %s\n" %e)

try:
    api_response = api_instance.get_market_status("NSE")
    print(api_response)
except ApiException as e:
    print("Exception when calling MarketHolidaysAndTimingsApi: %s\n" %e)
