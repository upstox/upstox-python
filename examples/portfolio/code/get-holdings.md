## Get user holdings

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'
api_version = '2.0'

api_instance = upstox_client.PortfolioApi(upstox_client.ApiClient(configuration))

try:
    api_response = api_instance.get_holdings(api_version)
    print(api_response)
except ApiException as e:
    print("Exception when calling ChargeApi->get_brokerage: %s\n" % e)
```
