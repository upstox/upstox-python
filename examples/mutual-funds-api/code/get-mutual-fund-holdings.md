## Get mutual fund holdings

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.MutualFundApi(upstox_client.ApiClient(configuration))

try:
    api_response = api_instance.get_mutual_fund_holdings()
    print(api_response)
except ApiException as e:
    print("Exception when calling MutualFundApi->get_mutual_fund_holdings: %s\n" % e)
```
