## Get all orders for the day

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
api_version = '2.0'
try:
    # Get order book
    api_response = api_instance.get_order_book(api_version)
    print(api_response)
except ApiException as e:
    print("Exception when calling OrderApi->get_order_book: %s\n" % e)
```
