## Get US order book

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.UsStocksOrderApi(upstox_client.ApiClient(configuration))

try:
    # Today's orders in every state
    api_response = api_instance.get_us_order_book()
    for order in api_response.data:
        print(order.order_id, order.trading_symbol, order.status, order.filled_quantity)
except ApiException as e:
    print("Exception when calling UsStocksOrderApi->get_us_order_book: %s\n" % e)
```

## Get US order details by order id

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.UsStocksOrderApi(upstox_client.ApiClient(configuration))

try:
    api_response = api_instance.get_us_order_details('{us_order_id}')
    print(api_response.data.status, api_response.data.status_message)
except ApiException as e:
    print("Exception when calling UsStocksOrderApi->get_us_order_details: %s\n" % e)
```
