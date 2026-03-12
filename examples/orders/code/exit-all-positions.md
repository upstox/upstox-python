## Exit all the open positions

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = "{your_access_token}"
api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))

try:
    api_response = api_instance.exit_positions()
    print(api_response)
except ApiException as e:
    print("Exception when calling OrderApi->exit all positions: %s\n" % e.body)

```

## Exit all the open positions for a given segment

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
    api_response = api_instance.exit_positions(**param)
    print(api_response)
except ApiException as e:
    print("Exception when calling OrderApi->exit all position: %s\n" % e.body)

```

## Exit all the open positions for a given tag

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
    api_response = api_instance.exit_positions(**param)
    print(api_response)
except ApiException as e:
    print("Exception when calling OrderApi->exit all position: %s\n" % e.body)

```
