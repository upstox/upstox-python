## Place a market order by quantity

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.UsStocksOrderApi(upstox_client.ApiClient(configuration))

# Fractional quantities are allowed only on fractionable stocks
body = upstox_client.UsPlaceOrderRequest(
    quantity=1.5,
    validity='DAY',
    instrument_key='US_EQ|AAPL',
    transaction_type='BUY',
    order_type='MARKET'
)

try:
    api_response = api_instance.place_us_order(body)
    print('order id:', api_response.data.order_id)
except ApiException as e:
    print("Exception when calling UsStocksOrderApi->place_us_order: %s\n" % e)
```

## Place a market order by USD amount

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.UsStocksOrderApi(upstox_client.ApiClient(configuration))

# Size the order by USD amount instead of quantity
body = upstox_client.UsPlaceOrderRequest(
    amount=50.0,
    validity='DAY',
    instrument_key='US_EQ|AAPL',
    transaction_type='BUY',
    order_type='MARKET'
)

try:
    api_response = api_instance.place_us_order(body)
    print('order id:', api_response.data.order_id)
except ApiException as e:
    print("Exception when calling UsStocksOrderApi->place_us_order: %s\n" % e)
```

## Place a limit order

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.UsStocksOrderApi(upstox_client.ApiClient(configuration))

body = upstox_client.UsPlaceOrderRequest(
    quantity=2,
    price=150.25,
    validity='DAY',
    tag='my-us-order',
    instrument_key='US_EQ|AAPL',
    transaction_type='BUY',
    order_type='LIMIT'
)

try:
    api_response = api_instance.place_us_order(body)
    print('order id:', api_response.data.order_id)
except ApiException as e:
    print("Exception when calling UsStocksOrderApi->place_us_order: %s\n" % e)
```
