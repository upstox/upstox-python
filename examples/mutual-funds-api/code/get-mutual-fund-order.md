## Get mutual fund order by id

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.MutualFundApi(upstox_client.ApiClient(configuration))

order_id = '{your_mf_order_id}'

try:
    api_response = api_instance.get_mutual_fund_order(order_id=order_id)
    print(api_response)
except ApiException as e:
    print("Exception when calling MutualFundApi->get_mutual_fund_order: %s\n" % e)
```
