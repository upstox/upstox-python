## Get news by instrument keys

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.NewsApi(upstox_client.ApiClient(configuration))

try:
    api_response = api_instance.get_news('instrument_keys', instrument_keys='NSE_EQ|INE669E01016')
    print(api_response)
except ApiException as e:
    print("Exception when calling NewsApi->get_news: %s\n" % e)
```

## Get news by instrument keys with pagination

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.NewsApi(upstox_client.ApiClient(configuration))

try:
    api_response = api_instance.get_news(
        'instrument_keys',
        instrument_keys='NSE_EQ|INE669E01016',
        page_number=1,
        page_size=10
    )
    print(api_response)
except ApiException as e:
    print("Exception when calling NewsApi->get_news: %s\n" % e)
```

## Get news by positions

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.NewsApi(upstox_client.ApiClient(configuration))

try:
    api_response = api_instance.get_news('positions')
    print(api_response)
except ApiException as e:
    print("Exception when calling NewsApi->get_news: %s\n" % e)
```

## Get news by holdings

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

api_instance = upstox_client.NewsApi(upstox_client.ApiClient(configuration))

try:
    api_response = api_instance.get_news('holdings')
    print(api_response)
except ApiException as e:
    print("Exception when calling NewsApi->get_news: %s\n" % e)
```
