## Get market holidays for current year

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()

api_instance = upstox_client.MarketHolidaysAndTimingsApi(upstox_client.ApiClient(configuration))

try:
    api_response = api_instance.get_holidays()
    print(api_response)
except ApiException as e:
    print("Exception when calling MarketHolidaysAndTimingsApi: %s\n" %e)

```

## Get market holiday status of a date

```python
import upstox_client
from upstox_client.rest import ApiException
configuration = upstox_client.Configuration()

api_instance = upstox_client.MarketHolidaysAndTimingsApi(upstox_client.ApiClient(configuration))

try:
    api_response = api_instance.get_holiday("2024-01-22")
    print(api_response)
except ApiException as e:
    print("Exception when calling MarketHolidaysAndTimingsApi: %s\n" %e)

```
