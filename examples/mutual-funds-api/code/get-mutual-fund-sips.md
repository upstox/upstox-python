## Get all mutual fund SIPs

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.MutualFundApi(upstox_client.ApiClient(configuration))

try:
    api_response = api_instance.get_mutual_fund_sips()
    print(api_response)
except ApiException as e:
    print("Exception when calling MutualFundApi->get_mutual_fund_sips: %s\n" % e)
```

## Get mutual fund SIPs with pagination

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.MutualFundApi(upstox_client.ApiClient(configuration))

try:
    api_response = api_instance.get_mutual_fund_sips(
        page_number=1,
        records=10
    )
    print(api_response)
except ApiException as e:
    print("Exception when calling MutualFundApi->get_mutual_fund_sips: %s\n" % e)
```
