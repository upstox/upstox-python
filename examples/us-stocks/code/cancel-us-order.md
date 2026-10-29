## Cancel an open order

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.UsStocksOrderApi(upstox_client.ApiClient(configuration))

try:
    api_response = api_instance.cancel_us_order('{us_order_id}')
    print('cancelled order id:', api_response.data.order_id)
except ApiException as e:
    print("Exception when calling UsStocksOrderApi->cancel_us_order: %s\n" % e)
```
