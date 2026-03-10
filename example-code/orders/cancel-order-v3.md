## Cancel an open order

```python
import upstox_client
from upstox_client.rest import ApiException
configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'
api_instance = upstox_client.OrderApiV3(upstox_client.ApiClient(configuration))

try:
    api_response = api_instance.cancel_order("2501211050101")
    print(api_response)
except ApiException as e:
    print("Exception when calling OrderApiV3->cancel_order: %s\n" % e)
```
