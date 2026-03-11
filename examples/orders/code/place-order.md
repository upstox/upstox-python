## Place a delivery market order

```python
import upstox_client
from upstox_client.rest import ApiException
configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'
api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
body = upstox_client.PlaceOrderRequest(1, "D", "DAY", 0.0, "string", "NSE_EQ|INE528G01035", "MARKET", "BUY", 0, 0.0, False)
api_version = '2.0'
try:
    api_response = api_instance.place_order(body, api_version)
    print(api_response)
except ApiException as e:
    print("Exception when calling OrderApi->place_order: %s\n" % e)
```

## Place a delivery limit order

```python
import upstox_client
from upstox_client.rest import ApiException
configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'
api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
body = upstox_client.PlaceOrderRequest(1, "D", "DAY", 20.0, "string", "NSE_EQ|INE528G01035", "LIMIT", "BUY", 0, 20.1, False)
api_version = '2.0'
try:
    api_response = api_instance.place_order(body, api_version)
    print(api_response)
except ApiException as e:
    print("Exception when calling OrderApi->place_order: %s\n" % e)
```

## Place a delivery stop-loss order

```python
import upstox_client
from upstox_client.rest import ApiException
configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'
api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
body = upstox_client.PlaceOrderRequest(1, "D", "DAY", 20, "string", "NSE_EQ|INE528G01035", "SL", "BUY", 0, 19.5, False)
api_version = '2.0'
try:
    api_response = api_instance.place_order(body, api_version)
    print(api_response)
except ApiException as e:
    print("Exception when calling OrderApi->place_order: %s\n" % e)

```

## Place a delivery stop-loss order market

```python
import upstox_client
from upstox_client.rest import ApiException
configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'
api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
body = upstox_client.PlaceOrderRequest(1, "D", "DAY", 0.0, "string", "NSE_EQ|INE528G01035", "SL-M", "BUY", 0, 21.5, False)
api_version = '2.0'
try:
    api_response = api_instance.place_order(body, api_version)
    print(api_response)
except ApiException as e:
    print("Exception when calling OrderApi->place_order: %s\n" % e)
```

## Place an intraday market order

```python
import upstox_client
from upstox_client.rest import ApiException
configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'
api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
body = upstox_client.PlaceOrderRequest(1, "I", "DAY", 0.0, "string", "NSE_EQ|INE528G01035", "MARKET", "BUY", 0, 0.0, False)
api_version = '2.0'
try:
    api_response = api_instance.place_order(body, api_version)
    print(api_response)
except ApiException as e:
    print("Exception when calling OrderApi->place_order: %s\n" % e)
```

## Place an intraday limit order

```python
import upstox_client
from upstox_client.rest import ApiException
configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'
api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
body = upstox_client.PlaceOrderRequest(1, "I", "DAY", 20.0, "string", "NSE_EQ|INE528G01035", "LIMIT", "BUY", 0, 20.1, False)
api_version = '2.0'
try:
    api_response = api_instance.place_order(body, api_version)
    print(api_response)
except ApiException as e:
    print("Exception when calling OrderApi->place_order: %s\n" % e)
```

## Place an intraday stop-loss order

```python
import upstox_client
from upstox_client.rest import ApiException
configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'
api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
body = upstox_client.PlaceOrderRequest(1, "I", "DAY", 20, "string", "NSE_EQ|INE528G01035", "SL", "BUY", 0, 19.5, False)
api_version = '2.0'
try:
    api_response = api_instance.place_order(body, api_version)
    print(api_response)
except ApiException as e:
    print("Exception when calling OrderApi->place_order: %s\n" % e)

```

## Place an intraday stop-loss market order

```python
import upstox_client
from upstox_client.rest import ApiException
configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'
api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
body = upstox_client.PlaceOrderRequest(1, "I", "DAY", 0.0, "string", "NSE_EQ|INE528G01035", "SL-M", "BUY", 0, 21.5, False)
api_version = '2.0'
try:
    api_response = api_instance.place_order(body, api_version)
    print(api_response)
except ApiException as e:
    print("Exception when calling OrderApi->place_order: %s\n" % e)
```

## Place a delivery market amo (after market order)

```python
import upstox_client
from upstox_client.rest import ApiException
configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'
api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
body = upstox_client.PlaceOrderRequest(1, "D", "DAY", 0.0, "string", "NSE_EQ|INE528G01035", "MARKET", "BUY", 0, 0.0, True)
api_version = '2.0'
try:
    api_response = api_instance.place_order(body, api_version)
    print(api_response)
except ApiException as e:
    print("Exception when calling OrderApi->place_order: %s\n" % e)
```
