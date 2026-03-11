## Example

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.LoginApi(upstox_client.ApiClient(configuration))
api_version = '2.0'

try:
    # Logout
    api_response = api_instance.logout(api_version)
    print(api_response)
except ApiException as e:
    print("Exception when calling LoginApi->logout: %s\n" % e)
```
