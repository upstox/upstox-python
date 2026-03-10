## Place an order with slicing enabled

```python
import upstox_client
from upstox_client.rest import ApiException
configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'
api_instance = upstox_client.OrderApiV3(upstox_client.ApiClient(configuration))
body = upstox_client.PlaceOrderV3Request(quantity=4000, product="D", validity="DAY", 
    price=0, tag="string", instrument_token="NSE_FO|43919", 
    order_type="MARKET", transaction_type="BUY", disclosed_quantity=0, 
    trigger_price=0.0, is_amo=False, slice=True)

try:
    api_response = api_instance.place_order(body)
    print(api_response)
except ApiException as e:
    print("Exception when calling OrderApiV3->place_order: %s\n" % e)
```

## Place an order with slicing disabled

```python
import upstox_client
from upstox_client.rest import ApiException
configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'
api_instance = upstox_client.OrderApiV3(upstox_client.ApiClient(configuration))
body = upstox_client.PlaceOrderV3Request(quantity=75, product="D", validity="DAY", 
    price=0, tag="string", instrument_token="NSE_FO|43919", 
    order_type="MARKET", transaction_type="BUY", disclosed_quantity=0, 
    trigger_price=0.0, is_amo=False, slice=False)

try:
    api_response = api_instance.place_order(body)
    print(api_response)
except ApiException as e:
    print("Exception when calling OrderApiV3->place_order: %s\n" % e)
```
