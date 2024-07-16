import upstox_client
from upstox_client.rest import ApiException
configuration = upstox_client.Configuration()
configuration.access_token = "your_access_token"
api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
body = upstox_client.PlaceOrderRequest(1, "D", "DAY", 0.0, "string", "NSE_EQ|INE528G01035", "MARKET", "BUY", 0, 0.0, True)
api_version = '2.0'
try:
    api_response = api_instance.place_order(body, api_version)
    print(api_response)
except ApiException as e:
    print("Exception when calling OrderApi->place_order: %s\n" % e)
