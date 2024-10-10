import upstox_client
import data_token
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = data_token.access_token
api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))

param = {
    'tag': "kg_python_sdk1"
}

try:
    api_response = api_instance.cancel_multi_order(**param)
    print(api_response)
except ApiException as e:
    print("Exception when calling OrderApi->place_order: %s\n" % e.body)