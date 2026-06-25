## Get payout history

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.UserApi(upstox_client.ApiClient(configuration))

try:
    api_response = api_instance.get_payout_history()
    print(api_response)
except ApiException as e:
    print("Exception when calling UserApi->get_payout_history: %s\n" % e)
```

## Get payout modes

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.UserApi(upstox_client.ApiClient(configuration))

try:
    api_response = api_instance.get_payout_modes()
    print(api_response)
except ApiException as e:
    print("Exception when calling UserApi->get_payout_modes: %s\n" % e)
```

## Initiate payout

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.UserApi(upstox_client.ApiClient(configuration))

# mode is one of the values returned by get_payout_modes (e.g. IMPS)
body = upstox_client.InitiatePayoutRequest(mode='IMPS', amount=1000.0)

try:
    api_response = api_instance.initiate_payout(body)
    print(api_response)
except ApiException as e:
    print("Exception when calling UserApi->initiate_payout: %s\n" % e)
```

## Modify payout

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.UserApi(upstox_client.ApiClient(configuration))

transaction_id = '{transaction_id}'
body = upstox_client.ModifyPayoutRequest(amount=2000.0)

try:
    api_response = api_instance.modify_payout(body, transaction_id)
    print(api_response)
except ApiException as e:
    print("Exception when calling UserApi->modify_payout: %s\n" % e)
```

## Cancel payout

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.UserApi(upstox_client.ApiClient(configuration))

transaction_id = '{transaction_id}'

try:
    api_response = api_instance.cancel_payout(transaction_id)
    print(api_response)
except ApiException as e:
    print("Exception when calling UserApi->cancel_payout: %s\n" % e)
```
