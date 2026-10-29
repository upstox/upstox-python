## Estimate charges for a market order

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.UsStocksOrderApi(upstox_client.ApiClient(configuration))

# Nothing is placed
body = upstox_client.UsOrderEstimateRequest(
    quantity=1,
    instrument_key='US_EQ|AAPL',
    transaction_type='BUY',
    order_type='MARKET'
)

try:
    api_response = api_instance.estimate_us_order(body)
    print('total charges:', api_response.data.total_charges)
    print('estimated total:', api_response.data.estimated_total)
except ApiException as e:
    print("Exception when calling UsStocksOrderApi->estimate_us_order: %s\n" % e)
```

## Estimate charges for a limit order

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.UsStocksOrderApi(upstox_client.ApiClient(configuration))

body = upstox_client.UsOrderEstimateRequest(
    quantity=0.5,
    price=150.0,
    instrument_key='US_EQ|AAPL',
    transaction_type='SELL',
    order_type='LIMIT'
)

try:
    api_response = api_instance.estimate_us_order(body)
    print(api_response.data)
except ApiException as e:
    print("Exception when calling UsStocksOrderApi->estimate_us_order: %s\n" % e)
```

## Calculate margin for multiple orders

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.UsStocksChargesApi(upstox_client.ApiClient(configuration))

# Up to 20 orders; nothing is placed
body = upstox_client.UsMarginRequest(instruments=[
    upstox_client.UsOrderEstimateRequest(quantity=1, instrument_key='US_EQ|AAPL', transaction_type='BUY', order_type='MARKET'),
    upstox_client.UsOrderEstimateRequest(quantity=2, price=100.0, instrument_key='US_EQ|MSFT', transaction_type='BUY', order_type='LIMIT'),
])

try:
    api_response = api_instance.calculate_us_margin(body)
    print('required margin:', api_response.data.required_margin)
    print('sufficient:', api_response.data.sufficient, 'shortfall:', api_response.data.shortfall)
except ApiException as e:
    print("Exception when calling UsStocksChargesApi->calculate_us_margin: %s\n" % e)
```
