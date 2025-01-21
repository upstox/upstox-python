import upstox_client
import data_token


from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = data_token.access_token

api_instance = upstox_client.OrderApiV3(upstox_client.ApiClient(configuration))

try:
    api_response = api_instance.cancel_order("250121010502101")
    print(api_response)
except ApiException as e:
    print("Exception when calling v3 cancel: %s\n" % e)