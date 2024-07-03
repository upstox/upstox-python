import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = "your_access_token"
api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
order_id = '231221011081579'
api_version = '2.0'

try:
    # Cancel order
    api_response = api_instance.cancel_order(order_id, api_version)
    print(api_response)
except ApiException as e:
    print("Exception when calling OrderApi->cancel_order: %s\n" % e)
