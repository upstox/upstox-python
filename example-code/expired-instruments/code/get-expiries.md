## Get Expiries for given instrument

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'
apiInstance = upstox_client.ExpiredInstrumentApi(upstox_client.ApiClient(configuration))
try:
    response = apiInstance.get_expiries("NSE_INDEX|Nifty 50")
    print(response)
except ApiException as e:
    print("Exception when calling expired instrument v3 api: %s\n" % e)
```
