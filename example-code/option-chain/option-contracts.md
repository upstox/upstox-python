## Get option contracts of an instrument key

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = "{your_access_token}"

api_instance = upstox_client.OptionsApi(upstox_client.ApiClient(configuration))

try:
    api_response = api_instance.get_option_contracts("NSE_INDEX|Nifty 50")
    print(api_response)
except ApiException as e:
    print("Exception when calling OrderApi->options apis: %s\n" % e.body)

```

## Get option contracts of an instrument key with expiry date 

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = "{your_access_token}"

api_instance = upstox_client.OptionsApi(upstox_client.ApiClient(configuration))

param = {
    'expiry_date': "2024-10-31"
}
try:
    api_response = api_instance.get_option_contracts("NSE_INDEX|Nifty 50", **param)
    print(api_response)
except ApiException as e:
    print("Exception when calling OrderApi->options apis: %s\n" % e.body)

```
