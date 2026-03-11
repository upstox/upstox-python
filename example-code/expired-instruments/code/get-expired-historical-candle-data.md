## Get Historical Candle Data for Expired Instruments

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'
apiInstance = upstox_client.ExpiredInstrumentApi(upstox_client.ApiClient(configuration))
try:
    response = apiInstance.get_expired_historical_candle_data("NSE_FO|54452|24-04-2025", "1minute", "2025-04-24", "2025-04-24")
    print(response)
except ApiException as e:
    print("Exception when calling expired instrument api: %s\n" % e)
```
