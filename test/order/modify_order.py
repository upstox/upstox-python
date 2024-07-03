import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = "your_access_token"

api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
body = upstox_client.ModifyOrderRequest(2, "DAY", 0, "231222010275930", "MARKET", 0, 0)
api_version = '2.0'  # str | API Version Header

try:
    # Modify order
    api_response = api_instance.modify_order(body, api_version)
    print(api_response)
except ApiException as e:
    print("Exception when calling OrderApi->modify_order: %s\n" % e)
