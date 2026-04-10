## Get equity and commodity funds (v3)

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.UserApi(upstox_client.ApiClient(configuration))

try:
    # Get User Fund And Margin V3
    api_response = api_instance.get_user_fund_margin_v3()
    print(api_response)
except ApiException as e:
    print("Exception when calling UserApi->get_user_fund_margin_v3: %s\n" % e)
```
