## Get ltp (last traded price) market quotes

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'
api_version = '2.0'

symbol = 'NSE_EQ|INE669E01016'
api_instance = upstox_client.MarketQuoteApi(upstox_client.ApiClient(configuration))

try:
    api_response = api_instance.ltp(symbol,api_version)
    print(api_response)
except ApiException as e:
    print("Exception when calling MarketQuoteApi->get_full_market_quote: %s\n" % e)

```

## Get ltp (last traded price) market quotes for multiple instruments keys

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'
api_version = '2.0'

symbol = 'NSE_EQ|INE669E01016,NSE_EQ|INE848E01016'
api_instance = upstox_client.MarketQuoteApi(upstox_client.ApiClient(configuration))

try:
    api_response = api_instance.ltp(symbol,api_version)
    print(api_response)
except ApiException as e:
    print("Exception when calling MarketQuoteApi->get_full_market_quote: %s\n" % e)

```
