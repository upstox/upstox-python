## Get Option Greek fields

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

apiInstance = upstox_client.MarketQuoteV3Api(upstox_client.ApiClient(configuration))
try:
    # For a single instrument
    response = apiInstance.get_market_quote_option_greek(instrument_key="NSE_FO|43885")
    print(response)
except ApiException as e:
    print("Exception when calling MarketQuoteV3Api->get_market_quote_option_greek: %s\n" % e)
```

## Get Option Greek fields for multiple instruments keys

```python
import upstox_client
from upstox_client.rest import ApiException

configuration = upstox_client.Configuration()
configuration.access_token = '{your_access_token}'

apiInstance = upstox_client.MarketQuoteV3Api(upstox_client.ApiClient(configuration))
try:
    # For multiple instruments
    response = apiInstance.get_market_quote_option_greek(instrument_key="NSE_FO|38604,NSE_FO|49210")
    print(response)
except ApiException as e:
    print("Exception when calling MarketQuoteV3Api->get_market_quote_option_greek: %s\n" % e)
```
