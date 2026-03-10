## Get user MTF positions

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'
apiInstance = upstox_client.PortfolioApi(upstox_client.ApiClient(configuration))

try:
    response = apiInstance.get_mtf_positions()
    print("MTF positions:", response)
except ApiException as e:
    print("Exception when calling PortfolioApi->get_mtf_positions: %s\n" % e)
```
