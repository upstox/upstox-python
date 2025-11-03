import upstox_client
import data_token
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = data_token.access_token
api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
body = upstox_client.PlaceOrderRequest(1, "D", "DAY", 0.0, "string", "NSE_EQ|INE669E01016", "MARKET", "BUY", 0, 0.0, True)
api_version = '2.0'
algo_name = 'Name'
try:
    api_response = api_instance.place_order(body, api_version, algo_id=algo_name)
    print(api_response)
except ApiException as e:
    print("Exception when calling OrderApi->place_order: %s\n" % e)