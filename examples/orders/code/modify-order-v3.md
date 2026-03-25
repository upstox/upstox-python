## Modify a delivery order

```python
import upstox_client
from upstox_client.rest import ApiException
configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'
api_instance = upstox_client.OrderApiV3(upstox_client.ApiClient(configuration))
body = upstox_client.ModifyOrderRequest(1, "DAY", 9.12, "25030310405859", "LIMIT", 0, 0)

try:
    api_response = api_instance.modify_order(body)
    print(api_response)
except ApiException as e:
    print("Exception when calling OrderApiV3->modify_order: %s\n" % e)
```
