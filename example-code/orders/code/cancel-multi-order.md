## Cancel all the open orders

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = "{your_access_token}"
api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))

try:
    api_response = api_instance.cancel_multi_order()
    print(api_response)
except ApiException as e:
    print("Exception when calling OrderApi->cancel all: %s\n" % e.body)

```

## Cancel all the open orders for a given segment

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = "{your_access_token}"
api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))

param = {
    'segment': "NSE_FO"
}

try:
    api_response = api_instance.cancel_multi_order(**param)
    print(api_response)
except ApiException as e:
    print("Exception when calling OrderApi->cancel all: %s\n" % e.body)

```

## Cancel all the open orders for a given tag

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = "{your_access_token}"
api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))

param = {
    'tag': "xyz"
}

try:
    api_response = api_instance.cancel_multi_order(**param)
    print(api_response)
except ApiException as e:
    print("Exception when calling OrderApi->cancel all: %s\n" % e.body)

```
