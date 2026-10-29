## Modify an open order

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.UsStocksOrderApi(upstox_client.ApiClient(configuration))

# Only whole-share orders can be modified
body = upstox_client.UsModifyOrderRequest(
    order_id='{us_order_id}',
    quantity=3,
    price=149.5,
    validity='DAY',
    instrument_key='{us_instrument_key}',
    transaction_type='BUY',
    order_type='LIMIT'
)

try:
    api_response = api_instance.modify_us_order(body)
    # The order is replaced, so use the new order id from here on
    print('new order id:', api_response.data.order_id)
except ApiException as e:
    print("Exception when calling UsStocksOrderApi->modify_us_order: %s\n" % e)
```
