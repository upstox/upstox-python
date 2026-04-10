## Get kill switch status

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.UserApi(upstox_client.ApiClient(configuration))

try:
    # Get Kill Switch Status
    api_response = api_instance.get_kill_switch()
    print(api_response)
except ApiException as e:
    print("Exception when calling UserApi->get_kill_switch: %s\n" % e)
```

## Update kill switch

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.UserApi(upstox_client.ApiClient(configuration))

body = [
    upstox_client.KillSwitchSegmentUpdateRequest(segment="NSE_EQ", action="DISABLE"),
    upstox_client.KillSwitchSegmentUpdateRequest(segment="NSE_FO", action="DISABLE")
]

try:
    # Update Kill Switch
    api_response = api_instance.update_kill_switch(body)
    print(api_response)
except ApiException as e:
    print("Exception when calling UserApi->update_kill_switch: %s\n" % e)
```
