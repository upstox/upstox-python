## Get order details for an order number

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = "{your_access_token}"
api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))

try:
    api_response = api_instance.get_order_status(order_id="2410170106208487")
    print(api_response)
except ApiException as e:
    print("Exception when calling OrderApi->get order status: %s\n" % e.body)
```
