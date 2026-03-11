## Get market status for a particular exchange

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = "{your_access_token}"
api_instance = upstox_client.MarketHolidaysAndTimingsApi(upstox_client.ApiClient(configuration))

try:
    api_response = api_instance.get_market_status("NSE")
    print(api_response)
except ApiException as e:
    print("Exception when calling MarketHolidaysAndTimingsApi: %s\n" %e)
```
