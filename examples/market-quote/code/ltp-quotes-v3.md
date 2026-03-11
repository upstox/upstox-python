## Get ltp (last traded price) market quotes

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

apiInstance = upstox_client.MarketQuoteV3Api(upstox_client.ApiClient(configuration))
try:
    # For a single instrument
    response = apiInstance.get_ltp(instrument_key="NSE_EQ|INE848E01016")
    print(response)
except ApiException as e:
    print("Exception when calling MarketQuoteV3Api->get_ltp: %s\n" % e)
```

## Get ltp (last traded price) market quotes for multiple instruments keys

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

apiInstance = upstox_client.MarketQuoteV3Api(upstox_client.ApiClient(configuration))
try:
    # For multiple instruments
    response = apiInstance.get_ltp(instrument_key="NSE_EQ|INE848E01016,NSE_EQ|INE669E01016")
    print(response)
except ApiException as e:
    print("Exception when calling MarketQuoteV3Api->get_ltp: %s\n" % e)
```
