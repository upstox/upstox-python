## Place a multi order

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'
api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
body = [
    upstox_client.MultiOrderRequest(25, "D", "DAY", 0, "string", False, "NSE_FO|44166", "MARKET", "BUY",
                                    0, 0, True, "1")
]

try:
    api_response = api_instance.place_multi_order(body)
    print(api_response)
except ApiException as e:
    print("Exception when calling OrderApi->place_order: %s\n" % e.body)

```

## Place Multiple BUY and SELL Orders

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'
api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
body = [
    upstox_client.MultiOrderRequest(25, "D", "DAY", 0, "string", False, "NSE_FO|44166", "MARKET", "BUY",
                                    0, 0, True, "1"),
    upstox_client.MultiOrderRequest(25, "D", "DAY", 0, "string", False, "NSE_FO|44122", "MARKET", "SELL",
                                    0, 0, True, "2")
]

try:
    api_response = api_instance.place_multi_order(body)
    print(api_response)
except ApiException as e:
    print("Exception when calling OrderApi->place_order: %s\n" % e.body)

```

## Place Multiple Orders with Auto Slicing enabled

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'
api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
body = [
    upstox_client.MultiOrderRequest(25, "D", "DAY", 0, "string", True, "NSE_FO|44166", "MARKET", "BUY",
                                    0, 0, True, "1")
]

try:
    api_response = api_instance.place_multi_order(body)
    print(api_response)
except ApiException as e:
    print("Exception when calling OrderApi->place_order: %s\n" % e.body)

```
