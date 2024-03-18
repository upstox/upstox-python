import upstox_client
from upstox_client.rest import ApiException
import const_file
configuration = upstox_client.Configuration()
configuration.access_token = const_file.access_token

api_instance = upstox_client.OptionsApi(upstox_client.ApiClient(configuration))

try:
    api_response = api_instance.get_option_contracts("NSE_INDEX|Nifty 50")
    print(api_response)
except ApiException as e:
    print("Exception when calling MarketHolidaysAndTimingsApi: %s\n" %e)

try:
    api_response = api_instance.get_put_call_option_chain("NSE_INDEX|Nifty 50", "2024-03-21")
    print(api_response)
except ApiException as e:
    print("Exception when calling MarketHolidaysAndTimingsApi: %s\n" %e)
