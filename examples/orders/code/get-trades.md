## Get all trades for the day

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))
api_version = '2.0'

try:
    # Get trades
    api_response = api_instance.get_trade_history(api_version)
    print(api_response)
except ApiException as e:
    print("Exception when calling OrderApi->get_trade_history: %s\n" % e)

```
