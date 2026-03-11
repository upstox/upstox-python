## Get put/call option chain

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = "{your_access_token}"

api_instance = upstox_client.OptionsApi(upstox_client.ApiClient(configuration))

try:
    api_response = api_instance.get_put_call_option_chain("NSE_INDEX|Nifty 50", "2024-10-31")
    print(api_response)
except ApiException as e:
    print("Exception when calling OrderApi->options apis: %s\n" % e.body)

```
