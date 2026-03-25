## Get order history for an order number

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
api_version = '2.0'
order_id = '240112010371054'

try:
    api_response = api_instance.get_order_details(api_version, order_id=order_id)
    print(api_response)
except ApiException as e:
    print("Exception when calling OrderApi->get_order_details: %s\n" % e)

```
