## Get user IPs

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.UserApi(upstox_client.ApiClient(configuration))

try:
    # Get User IPs
    api_response = api_instance.get_user_ips()
    print(api_response)
except ApiException as e:
    print("Exception when calling UserApi->get_user_ips: %s\n" % e)
```

## Update user IP

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.UserApi(upstox_client.ApiClient(configuration))

body = upstox_client.UpdateUserIpRequest(primary_ip="1.2.3.4")

try:
    # Update User IP
    api_response = api_instance.update_user_ip(body)
    print(api_response)
except ApiException as e:
    print("Exception when calling UserApi->update_user_ip: %s\n" % e)
```
