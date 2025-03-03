import upstox_client
import data_token

from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = data_token.access_token
api_instance = upstox_client.OrderApiV3(upstox_client.ApiClient(configuration))
body = upstox_client.GttCancelOrderRequest(gtt_order_id="GTT-C250303008840")
try:
    api_response = api_instance.cancel_gtt_order(body=body)
    print(api_response)
except ApiException as e:
    print("Exception when calling OrderApi->place_order: %s\n" % e)