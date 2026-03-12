## Get access token using auth code

```python
import upstox_client
from upstox_client.rest import ApiException

api_instance = upstox_client.LoginApi()
api_version = '2.0'
code = '{your_auth_code}'
client_id = '{your_client_id}'
client_secret = '{your_client_secret}'
redirect_uri = '{your_redirect_url}'
grant_type = 'grant_type_example'

try:
    # Get token API
    api_response = api_instance.token(api_version, code=code, client_id=client_id, client_secret=client_secret,
                                      redirect_uri=redirect_uri, grant_type=grant_type)
    print(api_response)
except ApiException as e:
    print("Exception when calling LoginApi->token: %s\n" % e)
```
