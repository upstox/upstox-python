## Get equity and commodity funds

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'
api_version = '2.0'

api_instance = upstox_client.UserApi(upstox_client.ApiClient(configuration))

try:
    # Get User Fund And Margin
    api_response = api_instance.get_user_fund_margin(api_version)
    print(api_response)
except ApiException as e:
    print("Exception when calling UserApi->get_user_fund_margin: %s\n" % e)
```

## Get equity funds

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'
api_version = '2.0'

api_instance = upstox_client.UserApi(upstox_client.ApiClient(configuration))
segment = 'SEC'
try:
    # Get User Fund And Margin
    api_response = api_instance.get_user_fund_margin(api_version, segment=segment)
    print(api_response)
except ApiException as e:
    print("Exception when calling UserApi->get_user_fund_margin: %s\n" % e)

```

## Get commodity funds

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'
api_version = '2.0'

api_instance = upstox_client.UserApi(upstox_client.ApiClient(configuration))
segment = 'COM'
try:
    # Get User Fund And Margin
    api_response = api_instance.get_user_fund_margin(api_version, segment=segment)
    print(api_response)
except ApiException as e:
    print("Exception when calling UserApi->get_user_fund_margin: %s\n" % e)

```
