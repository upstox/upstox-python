import upstox_client
import data_token
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = data_token.access_token
api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
body = [
    upstox_client.MultiOrderRequest(1, "I", "DAY", 0, "kg_python_sdk", False, "NSE_EQ|INE669E01016", "MARKET", "BUY",
                                    0, 0, True, "1"),
    upstox_client.MultiOrderRequest(1, "D", "DAY", 8.9, "kg_python_sdk1", False, "NSE_EQ|INE669E01016", "LIMIT", "BUY",
                                    0, 0, True, "2")
]

try:
    api_response = api_instance.place_multi_order(body)
    print(api_response)
except ApiException as e:
    print("Exception when calling OrderApi->place_order: %s\n" % e.body)