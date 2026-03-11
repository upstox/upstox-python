## Get trade history for equity segment

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = "{your_access_token}"
api_instance = upstox_client.PostTradeApi(upstox_client.ApiClient(configuration))

param = {
    'segment': "EQ"
}

try:
    api_response = api_instance.get_trades_by_date_range("2023-04-01", "2025-03-31",1,1000,**param)
    print(api_response)
except ApiException as e:
    print("Exception when calling OrderApi->get trades_by_date_range: %s\n" % e.body)
```

## Get trade history for futures and options segment

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = "{your_access_token}"
api_instance = upstox_client.PostTradeApi(upstox_client.ApiClient(configuration))

param = {
    'segment': "FO"
}

try:
    api_response = api_instance.get_trades_by_date_range("2023-04-01", "2025-03-31",1,1000,**param)
    print(api_response)
except ApiException as e:
    print("Exception when calling OrderApi->get trades_by_date_range: %s\n" % e.body)
```
