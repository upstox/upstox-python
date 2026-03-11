## Get Expired Future Contracts for given instrument with expiry date

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'
apiInstance = upstox_client.ExpiredInstrumentApi(upstox_client.ApiClient(configuration))
try:
    response = apiInstance.get_expired_future_contracts("NSE_INDEX|Nifty 50", "2024-11-27")
    print(response)
except ApiException as e:
    print("Exception when calling expired instrument api: %s\n" % e)
```
