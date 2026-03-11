## Get GTT Order Details

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'
api_instance = upstox_client.OrderApiV3(upstox_client.ApiClient(configuration))

try:
    api_response = api_instance.get_gtt_order_details(gtt_order_id="GTT-C25030300128840")
    print("GTT order details:", api_response)
except ApiException as e:
    print("Exception when calling OrderApi->get_gtt_order_details: %s\n" % e)
```
