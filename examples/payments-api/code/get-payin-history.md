## Get Payin History

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.UserApi(upstox_client.ApiClient(configuration))

try:
    api_response = api_instance.get_payin_history()
    print(api_response)
except ApiException as e:
    print("Exception when calling UserApi->get_payin_history: %s\n" % e)
```
