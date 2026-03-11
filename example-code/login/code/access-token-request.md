## Access token request

```python
import upstox_client

from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()

api_instance = upstox_client.LoginApi(upstox_client.ApiClient(configuration))
body = upstox_client.IndieUserTokenRequest(client_secret="****")
try:
    api_response = api_instance.init_token_request_for_indie_user(body,client_id="*****")
    print(api_response)
except ApiException as e:
    print("Exception when calling indie token request: %s\n" % e)
```
